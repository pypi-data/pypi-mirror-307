from datetime import datetime, timedelta

import pandas as pd


def get_date_periods(created_date: datetime) -> list[tuple[datetime, datetime]]:
    """Function to split the age of an account into 3-month periods.

    Args:
        created_date (datetime): Date of account creation

    Returns:
        List[Tuple[datetime, datetime]]: List of tuples representing periods of 3 months
                                         from account creation to the end of the current quarter.
    """
    if not isinstance(created_date, datetime):
        raise ValueError("created_date must be a datetime object")

    created_date = created_date.date()
    today = datetime.today().date()
    if created_date > today:
        return []

    quarter_end = pd.to_datetime(today + pd.tseries.offsets.QuarterEnd(startingMonth=3)).date()

    date_ranges = pd.date_range(start=created_date, end=quarter_end, freq="3M").to_pydatetime()
    date_ranges = [d.date() for d in date_ranges]

    if created_date < date_ranges[0]:
        date_ranges.insert(0, created_date)
    if today > date_ranges[-1]:
        date_ranges.append(today)

    date_period_tuples = []
    for i in range(len(date_ranges) - 1):
        start_date = date_ranges[i]
        end_date = date_ranges[i + 1] - timedelta(days=1)
        date_period_tuples.append((start_date, end_date))

    return date_period_tuples
