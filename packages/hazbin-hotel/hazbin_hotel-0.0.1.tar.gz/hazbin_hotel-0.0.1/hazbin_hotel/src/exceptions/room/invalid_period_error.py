class InvalidPeriodError(Exception):
    """Exception raised for errors in the period format.

    Attributes:
        period (str): The invalid period that caused the error.
        message (str): Explanation of the error.
    """

    def __init__(self, period: str):
        """Initializes InvalidPeriodError with the invalid period.

        Args:
            period (str): The period string that is invalid.
        """
        self.period = period
        self.message = f"Invalid period: {period}"
        super().__init__(self.message)
