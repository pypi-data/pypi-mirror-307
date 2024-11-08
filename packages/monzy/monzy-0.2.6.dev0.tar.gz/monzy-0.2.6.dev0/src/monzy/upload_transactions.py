import pandas as pd

from monzy.utils import sql_templates
from monzy.utils.custom_logger import logger


def _get_db_transactions(db: object, table: str) -> pd.DataFrame:
    """Fetch transactions from the database.

    Args:
        db (object): Database connection object.
        table (str): Name of the table to fetch transactions from.

    Returns:
        pd.DataFrame: DataFrame containing the transactions fetched from the database.
    """
    db_transactions = db.query(
        sql=sql_templates.exists.format(table=table),
        return_data=True,
    )

    return db_transactions


def get_new_transactions(db: object, table: str, fetched_transactions: pd.DataFrame):
    """Identify new transactions that are not present in the database.

    Args:
        db (object): Database connection object.
        table (str): Name of the table to check transactions against.
        fetched_transactions (pd.DataFrame): DataFrame containing fetched transactions.

    Returns:
        pd.DataFrame: DataFrame containing new transactions to be uploaded.
    """
    db_transactions = _get_db_transactions(db, table)

    db_ids_lst = db_transactions["id"].tolist()

    new_transaction_ids = []
    for item in fetched_transactions["id"].tolist():
        if item not in db_ids_lst:
            new_transaction_ids.append(item)

    transactions_to_upload = fetched_transactions[
        fetched_transactions["id"].isin(new_transaction_ids)
    ].reset_index(drop=True)

    return transactions_to_upload


def get_changed_transaction_ids(
    db: object, table: str, fetched_transactions: pd.DataFrame
) -> pd.DataFrame:
    """Identify transactions that have changed based on a set of columns.

    Args:
        db (object): Database connection object.
        table (str): Name of the table to check transactions against.
        fetched_transactions (pd.DataFrame): DataFrame containing fetched transactions.

    Returns:
        pd.DataFrame: DataFrame containing IDs of changed transactions.
    """
    compare_transaction_cols = ["id", "description", "amount", "category", "notes", "timestamp"]

    logger.info("Getting existing transactions from database")
    db_transactions = _get_db_transactions(db, table)

    logger.info("Converting columns: date, amount")
    db_transactions["date"] = pd.to_datetime(db_transactions["date"])
    db_transactions["amount"] = db_transactions["amount"].round(2)

    logger.info("Creating subset of database transactions with comparable columns only")
    db_transactions_subset = db_transactions[compare_transaction_cols]

    logger.info("Creating subset of fetched transactions with comparable columns only")
    fetched_transactions_subset = fetched_transactions[compare_transaction_cols]
    fetched_transactions_subset = fetched_transactions_subset.reset_index(drop=True).sort_values(
        "timestamp"
    )

    logger.info("Getting fetched transactions ids in a list")
    fetched_transactions_subset_ids = fetched_transactions["id"].tolist()

    logger.info("Getting transactions from db filtered by ids from fetched transactions")
    filtered_db_transactions_subset = (
        db_transactions_subset[db_transactions_subset["id"].isin(fetched_transactions_subset_ids)]
        .reset_index(drop=True)
        .sort_values("timestamp")
    )

    logger.info("Merging dataframes to compare columns to check if data changed")
    # Merge the DataFrames on 'id'
    merged_transactions = pd.merge(
        fetched_transactions_subset,
        filtered_db_transactions_subset,
        on="id",
        suffixes=("_fetched", "_db"),
    )

    # Initialize a DataFrame for differences
    differences = pd.DataFrame()

    for col in compare_transaction_cols:
        if col != "id":
            # For each column, check if the values in the merged DataFrame are different
            differences[col] = merged_transactions[f"{col}_fetched"].ne(
                merged_transactions[f"{col}_db"]
            )

    # Use 'any(axis=1)' to check each row - if any column is different, the row will be included
    logger.info("Checking each row if any column is different to include the id in the output")
    merged_transactions = merged_transactions[differences.any(axis=1)]

    changed_transactions_ids = merged_transactions["id"].to_list()

    return changed_transactions_ids
