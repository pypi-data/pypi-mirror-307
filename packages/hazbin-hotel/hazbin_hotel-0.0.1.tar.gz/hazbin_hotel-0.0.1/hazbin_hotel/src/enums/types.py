from enum import Enum


class RoomTypeEnum(Enum):
    """
    Enumeration of room types in a hotel, each representing a specific type of room setup and amenity level.

    Attributes:
        SINGLE (str): Single bed for one guest.
        DOUBLE (str): Room with a double bed for two guests.
        TWIN (str): Two single beds for two guests.
        SUITE (str): Larger room with luxury amenities.
        FAMILY (str): Larger room for families, often with extra beds.
        DELUXE (str): Higher-end room with added comfort or space.
        STUDIO (str): Open-plan room with combined living and sleeping area.
        PRESIDENTIAL_SUITE (str): Top-tier suite with premium amenities.
        BUNGALOW (str): Stand-alone unit, often with private outdoor space.
        PENTHOUSE (str): Luxurious top-floor suite with exclusive views.
    """

    SINGLE = "SINGLE"  # Single bed for one guest.
    DOUBLE = "DOUBLE"  # Room with a double bed for two guests.
    TWIN = "TWIN"  # Two single beds for two guests.
    SUITE = "SUITE"  # Larger room with luxury amenities.
    FAMILY = "FAMILY"  # Larger room for families, often with extra beds.
    DELUXE = "DELUXE"  # Higher-end room with added comfort or space.
    STUDIO = "STUDIO"  # Open-plan room with living and sleeping area.
    PRESIDENTIAL_SUITE = "PRESIDENTIAL_SUITE"  # Top-tier suite with premium amenities.
    BUNGALOW = "BUNGALOW"  # Stand-alone unit, often with private outdoor space.
    PENTHOUSE = "PENTHOUSE"  # Luxurious top-floor suite with exclusive views.


ROOM_MULTIPLIERS = {
    RoomTypeEnum.SINGLE: 1.0,  # Base rate for single occupancy.
    RoomTypeEnum.DOUBLE: 1.5,  # Moderate rate for two guests.
    RoomTypeEnum.TWIN: 1.4,  # Slightly lower rate for twin beds.
    RoomTypeEnum.SUITE: 2.0,  # Higher rate for luxury.
    RoomTypeEnum.FAMILY: 1.8,  # Larger room for families.
    RoomTypeEnum.DELUXE: 1.6,  # Enhanced comfort or space.
    RoomTypeEnum.STUDIO: 1.3,  # Open-plan living space.
    RoomTypeEnum.PRESIDENTIAL_SUITE: 3.0,  # Premium rate for top suite.
    RoomTypeEnum.BUNGALOW: 2.2,  # Private unit with outdoor area.
    RoomTypeEnum.PENTHOUSE: 3.5,  # Highest rate for exclusive amenities.
}
"""dict: Multipliers for room pricing based on room type.

Each key is a RoomTypeEnum member representing a type of room, and the corresponding
value is a float multiplier applied to the base price to calculate the final rate for
that room type.

Keys:
    - **RoomTypeEnum.SINGLE** (float): `1.0` - Base rate for single occupancy.
    - **RoomTypeEnum.DOUBLE** (float): `1.5` - Moderate rate for two guests.
    - **RoomTypeEnum.TWIN** (float): `1.4` - Slightly lower rate for twin beds.
    - **RoomTypeEnum.SUITE** (float): `2.0` - Higher rate for luxury.
    - **RoomTypeEnum.FAMILY** (float): `1.8` - Larger room for families.
    - **RoomTypeEnum.DELUXE** (float): `1.6` - Enhanced comfort or space.
    - **RoomTypeEnum.STUDIO** (float): `1.3` - Open-plan living space.
    - **RoomTypeEnum.PRESIDENTIAL_SUITE** (float): `3.0` - Premium rate for top suite.
    - **RoomTypeEnum.BUNGALOW** (float): `2.2` - Private unit with outdoor area.
    - **RoomTypeEnum.PENTHOUSE** (float): `3.5` - Highest rate for exclusive amenities.

Examples:
    >>> ROOM_MULTIPLIERS[RoomTypeEnum.SUITE]
    2.0
"""
