import datetime


def format_date(date: datetime) -> str:
    """Formats a datetime object to a string in 'YYYY-MM-DD' format.

    Args:
        date (datetime): The datetime object to format.

    Returns:
        str: The formatted date string in 'YYYY-MM-DD' format.

    Example:
        >>> from datetime import datetime
        >>> date = datetime(2023, 11, 8)
        >>> format_date(date)
        '2023-11-08'
    """

    return date.strftime("%Y-%m-%d")
