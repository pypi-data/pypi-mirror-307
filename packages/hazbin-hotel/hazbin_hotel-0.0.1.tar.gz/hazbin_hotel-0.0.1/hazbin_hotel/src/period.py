from datetime import datetime

from hazbin_hotel.src.exceptions.room.invalid_period_error import InvalidPeriodError


class Period:
    """
    Represents a period with a start and end date.

    Attributes:
        start (datetime): The start date of the period.
        end (datetime): The end date of the period.
    """

    def __init__(self, start: datetime, end: datetime):
        """
        Initializes a Period object with a start and end date.

        Args:
            start (datetime): The start date of the period.
            end (datetime): The end date of the period.

        Raises:
            ValueError: If the start date is after the end date.
        """
        if start > end:
            raise InvalidPeriodError("Start date must be before end date.")
        self._start = start
        self._end = end

    def change_start(self, start: datetime) -> bool:
        """
        Changes the start date of the period.

        Args:
            start (datetime): The new start date.

        Returns:
            bool: True if the start date was successfully changed, False otherwise.

        Examples:
            >>> from datetime import datetime
            >>> period = Period(datetime(2023, 1, 1), datetime(2023, 1, 2))
            >>> period.change_start(datetime(2023, 1, 3))
            False
            >>> period.change_start(datetime(2023, 1, 2))
            True
            >>> print(period.start)
            2023-01-02 00:00:00
        """
        if start > self._end:
            return False
        self._start = start
        return True

    def change_end(self, end: datetime) -> bool:
        """
        Changes the end date of the period.

        Args:
            end (datetime): The new end date.

        Returns:
            bool: True if the end date was successfully changed, False otherwise.

        Examples:
            >>> from datetime import datetime
            >>> period = Period(datetime(2023, 1, 2), datetime(2023, 1, 3))
            >>> period.change_end(datetime(2023, 1, 1))
            False
            >>> period.change_end(datetime(2023, 1, 4))
            True
            >>> print(period.end)
            2023-01-04 00:00:00
        """
        if self._start > end:
            return False
        self._end = end
        return True

    @property
    def start(self) -> datetime:
        """
        Gets the start date of the period.

        Returns:
            datetime: The start date of the period.

        Examples:
            >>> from datetime import datetime
            >>> period = Period(datetime(2023, 1, 1), datetime(2023, 1, 2))
            >>> print(period.start)
            2023-01-01 00:00:00
        """
        return self._start

    @property
    def end(self) -> datetime:
        """
        Gets the end date of the period.

        Returns:
            datetime: The end date of the period.

        Examples:
            >>> from datetime import datetime
            >>> period = Period(datetime(2023, 1, 1), datetime(2023, 1, 2))
            >>> print(period.end)
            2023-01-02 00:00:00
        """
        return self._end

    def __str__(self) -> str:
        return f"START: {self.start} | END: {self.end}"
