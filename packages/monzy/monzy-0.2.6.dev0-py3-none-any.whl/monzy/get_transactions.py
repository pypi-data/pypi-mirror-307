from datetime import datetime, timedelta

import pandas as pd
from monzo.endpoints.transaction import Transaction

from monzy.utils.custom_logger import logger
from monzy.utils.date_utils import get_date_periods


def get_transactions_df(
    monzo_auth: object, account_id: str, account_name: str, days_lookback: int = 30
) -> pd.DataFrame:
    """Fetch recent transactions from Monzo API.

    Args:
        monzo_auth (object): Monzo authentication object.
        account_id (str): Monzo account ID.
        account_name (str): Monzo account name.
        days_lookback (int): Number of days to lookback, defaults to 30.

    Returns:
        pd.Dataframe: Dataframe of fetched transactions.
    """
    fetched_transactions_list = Transaction.fetch(
        auth=monzo_auth,
        account_id=account_id,
        since=datetime.today() - timedelta(days=days_lookback),
        expand=["merchant"],
    )
    logger.info(f"Fetched {len(fetched_transactions_list)} transactions from {account_name}")

    fetched_transactions = []
    for trn in fetched_transactions_list:
        fetched_transactions.append(
            {
                "id": trn.transaction_id,
                "date": trn.created,
                "description": trn.description,
                "amount": trn.amount,
                "category": trn.category,
                "decline_reason": trn.decline_reason,
                "meta": trn.metadata,
                "merchant": trn.merchant,
                "currency": trn.currency,
                "local_currency": trn.local_currency,
                "local_amount": trn.local_amount,
                "source": account_name,
            }
        )

    transactions_df = pd.DataFrame(fetched_transactions)

    transactions_df.rename(
        columns={"transaction_id": "id", "created": "date"},
        inplace=True,
    )

    return transactions_df


def get_historic_transactions(
    monzo_auth: object, account_id: str, created_date: datetime
) -> pd.DataFrame:
    """Fetch historical transactions from Monzo API.

    Args:
        monzo_auth (object): Monzo authentication object.
        account_id (str): Monzo account ID.
        created_date (datetime): The starting date to fetch transactions from.

    Returns:
        pd.DataFrame: DataFrame containing fetched transactions.
    """
    fetched_transactions_lst = []
    periods = get_date_periods(created_date)
    logger.info(f"Using date range: {periods}")

    try:
        for since, before in periods:
            fetched_transactions = Transaction.fetch(
                auth=monzo_auth,
                account_id=account_id,
                since=since,
                before=before,
                expand=["merchant"],
            )
            fetched_transactions_lst.append(fetched_transactions)
            num_of_transactions = len(fetched_transactions)
            logger.info(
                f"Fetched {num_of_transactions} transactions for dates: {since} to {before}"
            )
    except Exception:
        logger.error(
            "Failed to fetch transactions for some dates - make sure to trigger DAG immediately after refreshing permissions"
        )

    return [item for sublist in fetched_transactions_lst for item in sublist]
