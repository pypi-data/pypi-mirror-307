from hazbin_hotel.src.period import Period


class Schedule:
    """
    Represents a schedule for a client within a specific period.

    Attributes:
        client_name (str): The name of the client.
        period (Period): The period of the schedule.
        id (int): The unique identifier for the schedule.
    """

    instance_counter = 0

    def __init__(self, client_name: str, period: Period) -> None:
        """
        Initializes a Schedule object with a client name and period.

        Args:
            client_name (str): The name of the client.
            period (Period): The period of the schedule.
        """
        self._client_name = client_name
        self.period = period
        self.id = Schedule.instance_counter
        Schedule.instance_counter += 1

    @property
    def client_name(self) -> str:
        """
        Gets the client name.

        Returns:
            str: The name of the client.

        Examples:
            >>> from datetime import datetime
            >>> period = Period(datetime(2023, 1, 1), datetime(2023, 1, 2))
            >>> schedule = Schedule("Client A", period)
            >>> print(schedule.client_name)
            Client A
        """
        return self._client_name

    @client_name.setter
    def client_name(self, value: str) -> None:
        """
        Sets the client name.

        Args:
            value (str): The new client name.

        Examples:
            >>> from datetime import datetime
            >>> period = Period(datetime(2023, 1, 1), datetime(2023, 1, 2))
            >>> schedule = Schedule("Client A", period)
            >>> schedule.client_name = "Client B"
            >>> print(schedule.client_name)
            Client B
        """
        self._client_name = value
