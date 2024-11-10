from datetime import datetime
from typing import List

from hazbin_hotel.src.enums.types import RoomTypeEnum
from hazbin_hotel.src.exceptions import (
    RoomHasSchedule,
    RoomNotAvailable,
    RoomTypeNotAvailable,
)
from hazbin_hotel.src.period import Period
from hazbin_hotel.src.room import Room
from hazbin_hotel.src.schedule import Schedule
from hazbin_hotel.src.utils import format_date


class Hotel:
    """Represents a hotel that manages room bookings and availability.

    Attributes:
        rooms (List[Room]): List of Room objects representing the rooms in the hotel.
    """

    def __init__(self, rooms: List[Room]):
        """Initializes the Hotel with a list of rooms.

        Args:
            rooms (List[Room]): A list of Room objects available in the hotel.
        """
        self._rooms = rooms

    @property
    def rooms(self) -> List[Room]:
        """List[Room]: Gets the list of rooms in the hotel."""
        return self._rooms

    def add_room(self, room: Room):
        """Adds a new room to the hotel.

        Args:
            room (Room): The room to add to the hotel.

        """
        self._rooms.append(room)

    def remove_room(self, room: Room):
        """Removes a room from the hotel if it has no schedules.

        Args:
            room (Room): The room to be removed.

        Raises:
            RoomHasSchedule: If the room has scheduled bookings.

        """
        if len(room.schedules) > 0:
            raise RoomHasSchedule(f'Room "{room.type.value}-{room.number}" cannot be removed because it has schedules.')
        self._rooms.remove(room)

    def check_room_type_availability(self, room_type: RoomTypeEnum) -> Room | None:
        """Checks if there is a room of the specified type available.

        Args:
            room_type (RoomTypeEnum): The type of room to check availability for.

        Returns:
            Room | None: An available room of the specified type.

        Raises:
            RoomTypeNotAvailable: If no room of the specified type is available.

        """
        for room in self._rooms:
            if room_type == room.type:
                return room
        raise RoomTypeNotAvailable(f'Room "{room_type.value}" is not available in this hotel')

    def schedule_a_room(
        self,
        client_name: str,
        room_type: RoomTypeEnum,
        start_date: datetime,
        end_date: datetime,
    ):
        """Schedules a room for a client if available.

        Args:
            client_name (str): The name of the client making the booking.
            room_type (RoomTypeEnum): The type of room requested.
            start_date (datetime): The start date of the booking period.
            end_date (datetime): The end date of the booking period.

        Returns:
            bool: True if the booking was successful.

        Raises:
            RoomNotAvailable: If no room is available for the specified period.

        """
        room = self.check_room_type_availability(room_type)
        period = Period(start_date, end_date)

        if room.is_period_available(period):
            schedule = Schedule(client_name, period)
            room.add_schedule(schedule)
            return True
        raise RoomNotAvailable(
            f'"{room.type.value}" is not available from {format_date(start_date)} to {format_date(end_date)}'
        )
