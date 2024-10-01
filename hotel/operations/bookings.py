from datetime import date
from typing import Optional
from pydantic import BaseModel

from hotel.operations.interface import DataInterface, DataObject
from hotel.operations.rooms import check_rooms_available


class InvalidDateError(Exception):
    """A base error for invalid booking dates."""

    pass


class ZeroNightStayError(InvalidDateError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.from_date = kwargs.get("from_date")
        self.to_date = kwargs.get("to_date")
        self.message = f"From date {self.from_date} to {self.to_date} would create a zero night stay."


class BookingCreateData(BaseModel):
    # room_id: int
    customer_id: int
    from_date: date
    to_date: date


class BookingUpdateData(BaseModel):
    room_id: Optional[int] = None
    from_date: Optional[date] = None
    to_date: Optional[date] = None


def read_all_bookings(booking_interface: DataInterface) -> list[DataObject]:
    return booking_interface.read_all()


def read_booking(booking_id: int, booking_interface: DataInterface) -> DataObject:
    return booking_interface.read_by_id(booking_id)


def create_booking(
    data: BookingCreateData,
    booking_interface: DataInterface,
    room_interface: DataInterface,
) -> DataObject:
    booking_dict = data.model_dump()
    rooms_available = check_rooms_available(
        booking_dict["from_date"],
        booking_dict["to_date"],
        room_interface,
        booking_interface,
    )
    room = room_interface.read_by_id(rooms_available[0])
    booking_dict["room_id"] = room["id"]
    booking_dict["price"] = get_new_booking_price(booking_dict, room["price"])

    return booking_interface.create(booking_dict)


def delete_booking(booking_id: int, booking_interface: DataInterface) -> DataObject:
    return booking_interface.delete(booking_id)


def update_booking(
    booking_id: int,
    data: BookingUpdateData,
    booking_interface: DataInterface,
    room_interface: DataInterface,
) -> DataObject:
    old_data = read_booking(booking_id, booking_interface)
    update_data = data.model_dump(exclude_unset=True)
    booking_dict = old_data | update_data
    room_data = room_interface.read_by_id(booking_dict["room_id"])
    update_data["price"] = get_new_booking_price(booking_dict, room_data["price"])

    return booking_interface.update(booking_id, update_data)


def get_new_booking_price(booking_dict: dict, room_price: int) -> int:
    days = (booking_dict["to_date"] - booking_dict["from_date"]).days

    if days <= 0:
        raise ZeroNightStayError(
            from_date=booking_dict["from_date"], to_date=booking_dict["to_date"]
        )

    return room_price * days


# Check availability when booking a room (advanced)
#
# When a customer books a room, extend the operation to validate whether the
# room is actually available. If you want to go all in here, you can even
# change the create_booking endpoint to not receive a room number, but simply
# pick the first available room depending on availability.
