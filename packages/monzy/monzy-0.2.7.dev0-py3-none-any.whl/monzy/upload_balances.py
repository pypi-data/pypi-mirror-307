import numpy as np
import pandas as pd

from monzy.utils import sql_templates


def _get_uploaded_balances(db: object, table: str) -> pd.DataFrame:
    """Retrieve uploaded balances from the database.

    Args:
        db (object): Database connection object.
        table (str): Name of the table to query.

    Returns:
        pd.DataFrame: DataFrame containing the uploaded balances.
    """
    uploaded_balances = db.query(
        sql=sql_templates.exists_pots.format(table=table),
        return_data=True,
    )

    return uploaded_balances


def get_new_balances(db: object, table: str, balances: pd.DataFrame) -> pd.DataFrame:
    """Identify new balances that are not yet uploaded to the database.

    Args:
        db (object): Database connection object.
        table (str): Name of the table to check for existing balances.
        balances (pd.DataFrame): DataFrame containing the current balances.

    Returns:
        pd.DataFrame: DataFrame containing the new balances to be uploaded.
    """
    uploaded_balances = _get_uploaded_balances(db, table)

    uploaded_ids_lst = uploaded_balances["id"].tolist()

    new_pot_ids = []
    for item in balances["id"].tolist():
        if item not in uploaded_ids_lst:
            new_pot_ids.append(item)

    balances_to_upload = balances[balances["id"].isin(new_pot_ids)].reset_index(drop=True)

    return balances_to_upload


def get_changed_balances(db: object, table: str, balances: pd.DataFrame) -> pd.DataFrame:
    """Identify balances that have changed compared to the ones in the database.

    Args:
        db (object): Database connection object.
        table (str): Name of the table to check for existing balances.
        balances (pd.DataFrame): DataFrame containing the current balances.

    Returns:
        pd.DataFrame: DataFrame containing the balances that have changed.
    """
    uploaded_balances = _get_uploaded_balances(db, table)

    uploaded_ids_lst = uploaded_balances["id"].tolist()

    seen_balances = balances[balances["id"].isin(uploaded_ids_lst)]

    seen_balances = seen_balances.sort_values("id")
    seen_balances = seen_balances.reset_index(drop=True)
    seen_balances = seen_balances.replace({None: np.nan})
    seen_balances = seen_balances.fillna(0)
    seen_balances["balance"] = seen_balances["balance"].astype(float)
    seen_balances["balance"] = seen_balances["balance"].round(2)

    seen_balances_ids = seen_balances["id"].tolist()

    seen_uploaded_balances = uploaded_balances[uploaded_balances["id"].isin(seen_balances_ids)]
    seen_uploaded_balances = seen_uploaded_balances.sort_values("id")
    seen_uploaded_balances = seen_uploaded_balances.reset_index(drop=True)
    seen_uploaded_balances = seen_uploaded_balances.replace({None: np.nan})
    seen_uploaded_balances = seen_uploaded_balances.fillna(0)
    seen_uploaded_balances["balance"] = seen_uploaded_balances["balance"].astype(float)
    seen_uploaded_balances["balance"] = seen_uploaded_balances["balance"].round(2)

    changed_balances = seen_balances[seen_uploaded_balances.ne(seen_balances).any(axis=1)]

    return changed_balances


def update_changed_balances(
    db: object, table: str, balances: pd.DataFrame, changed_balances: pd.DataFrame
) -> None:
    """Update the balances in the database by deleting and reinserting the changed balances.

    Args:
        db (object): Database connection object.
        table (str): Name of the table to update balances.
        balances (pd.DataFrame): DataFrame containing the current balances.
        changed_balances (pd.DataFrame): DataFrame containing the balances that have changed.

    Returns:
        None
    """
    balances_to_delete_ids = changed_balances["id"].tolist()
    balances_to_delete_ids_str = str(changed_balances["id"].tolist()).strip("[").strip("]")

    db.delete(table, balances_to_delete_ids_str)

    balances_to_reinsert = balances[balances["id"].isin(balances_to_delete_ids)]

    db.insert(table, balances_to_reinsert)
