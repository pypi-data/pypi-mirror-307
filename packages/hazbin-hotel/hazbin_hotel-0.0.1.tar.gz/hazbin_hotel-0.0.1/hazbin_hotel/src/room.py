from typing import List

from colorama import Fore, Style

from hazbin_hotel.src.enums.types import ROOM_MULTIPLIERS, RoomTypeEnum
from hazbin_hotel.src.exceptions import InvalidRoomType, ScheduleCannotBeOverwritten
from hazbin_hotel.src.period import Period
from hazbin_hotel.src.schedule import Schedule


class Room:
    """Represents a room in a hotel with specific attributes, price, type, and scheduling availability.

    Attributes:
        instance_count (int): Counter to assign unique room numbers.
        number (int): The unique identifier of the room instance.
        _type (RoomTypeEnum): Type of the room, defined by RoomTypeEnum.
        _price (float): Base price for the room.
        _multiplier_factor_price (float): Multiplier for the room rate based on room type.
        _schedules (List[Schedule]): List of scheduled bookings for the room.
    """

    instance_count = 1

    def __init__(self, room_type: RoomTypeEnum, price: float, schedules: List[Schedule]) -> None:
        """Initializes the Room with a type, price, and existing schedules.

        Args:
            room_type (RoomTypeEnum): Type of the room.
            price (float): Base price of the room.
            schedules (List[Schedule]): Initial list of schedules associated with the room.

        Raises:
            InvalidRoomType: If the room type is invalid.
            ValueError: If the price is negative.
        """
        self._validate_room_type(room_type)
        self._validate_room_price(price)

        self.number = Room.instance_count
        self._type = room_type
        self._price = price
        self._multiplier_factor_price = 0
        self._schedules = schedules

        self._set_multiplier_factor(room_type)
        Room.instance_count += 1

    @property
    def price(self) -> float:
        """float: Gets or sets the base price of the room."""
        return self._price

    @price.setter
    def price(self, new_price: float):
        self.update_price(new_price)

    @property
    def type(self) -> RoomTypeEnum:
        """RoomTypeEnum: Gets or sets the type of the room."""
        return self._type

    @type.setter
    def type(self, new_type: RoomTypeEnum):
        self._validate_room_type(new_type)
        if self._type == new_type:
            print(f"{Fore.YELLOW}[WARNING]: Same type was set!!{Style.RESET_ALL}")
        self._type = new_type

    @property
    def multiplier_factor_price(self) -> float:
        """float: Gets the multiplier factor for the room price based on room type."""
        return self._multiplier_factor_price

    @property
    def schedules(self) -> List[Schedule]:
        """List[Schedule]: Gets the list of schedules associated with the room."""
        return self._schedules

    def add_schedule(self, schedule: Schedule):
        """Adds a schedule to the room if the period is available.

        Args:
            schedule (Schedule): The schedule to add.

        Raises:
            ValueError: If the period is not available.
        """
        if not self.is_period_available(schedule.period):
            raise ValueError("The period is not available.")
        self._schedules.append(schedule)

    def is_period_available(
        self,
        period: Period,
        *,
        ignore_schedule: bool = False,
        schedule_id: int = None,
    ) -> bool:
        """Checks if a given period is available for scheduling.

        Args:
            period (Period): The period to check.
            ignore_schedule (bool, optional): Whether to ignore a specific schedule. Defaults to False.
            schedule_id (int, optional): ID of the schedule to ignore if `ignore_schedule` is True.

        Returns:
            bool: True if the period is available, False otherwise.

        Raises:
            ValueError: If `ignore_schedule` is True but `schedule_id` is None.
        """
        if ignore_schedule and schedule_id is None:
            raise ValueError("Schedule ID is missing")

        for scheduled in self._schedules:
            if ignore_schedule and scheduled.id == schedule_id:
                continue

            if (
                (scheduled.period.start <= period.start <= scheduled.period.end)
                or (scheduled.period.start <= period.end <= scheduled.period.end)
                or (period.start <= scheduled.period.start <= period.end)
            ):
                return False
        return True

    def update_price(self, new_price: float):
        """Updates the room price.

        Args:
            new_price (float): The new price to set.

        Raises:
            ValueError: If the new price is negative.
        """
        self._validate_room_price(new_price)
        self._price = new_price

    def update_schedule(self, schedule: Schedule, schedule_id: int):
        """Updates an existing schedule if the period is available.

        Args:
            schedule (Schedule): New schedule details.
            schedule_id (int): ID of the schedule to update.

        Raises:
            ScheduleCannotBeOverwritten: If the period is not available for update.
        """
        if not self.is_period_available(schedule.period, ignore_schedule=True, schedule_id=schedule_id):
            raise ScheduleCannotBeOverwritten("The schedule cannot be overwritten")

        schedule_index_to_update = -1
        for schedule_index, scheduled in enumerate(self._schedules):
            if scheduled.id == schedule_id:
                schedule_index_to_update = schedule_index

        self._schedules[schedule_index_to_update] = schedule

    def _set_multiplier_factor(self, room_type: RoomTypeEnum) -> None:
        """Sets the multiplier factor for room price based on the room type.

        Args:
            room_type (RoomTypeEnum): The type of the room.

        Raises:
            InvalidRoomType: If the room type is invalid.
        """
        if room_type in ROOM_MULTIPLIERS:
            self._multiplier_factor_price = ROOM_MULTIPLIERS[room_type]
            return
        raise InvalidRoomType(f'Invalid room type, please check type "{room_type.value}"')

    @staticmethod
    def _validate_room_type(room_type: RoomTypeEnum) -> None:
        """Validates if the room type is recognized.

        Args:
            room_type (RoomTypeEnum): The room type to validate.

        Raises:
            InvalidRoomType: If the room type is invalid.
        """
        if room_type not in RoomTypeEnum:
            raise InvalidRoomType(f'Invalid room type, please check type "{room_type.value}"')

    @staticmethod
    def _validate_room_price(price: float) -> None:
        """Validates the room price.

        Args:
            price (float): The room price to validate.

        Raises:
            ValueError: If the price is negative.
        """
        if price < 0:
            raise ValueError("Price cannot be negative.")
