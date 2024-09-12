from datetime import date


import pytest


from hotel.operations.bookings import (
    BookingCreateData,
    InvalidDateError,
    create_booking,
)
from hotel.operations.rooms import check_room_availability, check_rooms_available
from hotel.operations.interface import DataObject
from hotel.tests.data_interface_stub import DataInterfaceStub


class RoomInterface(DataInterfaceStub):
    def read_by_id(self, id: int) -> DataObject:
        return {"id": id, "number": "101", "size": 10, "price": 150_00}

    def read_all(self) -> list[DataObject]:
        return [
            {"id": 1, "number": "101", "size": 10, "price": 150_00},
            {"id": 2, "number": "102", "size": 10, "price": 150_00},
            {"id": 3, "number": "103", "size": 20, "price": 250_00},
            {"id": 4, "number": "104", "size": 20, "price": 250_00},
            {"id": 5, "number": "105", "size": 30, "price": 350_00},
        ]


class BookingInterface(DataInterfaceStub):
    def create(self, data: DataObject) -> DataObject:
        booking = dict(data)
        booking["id"] = 1
        return booking

    def read_all(self) -> list[DataObject]:
        return [
            {
                "id": 1,
                "room_id": 1,
                "customer_id": 1,
                "from_date": date.fromisoformat("2021-12-24"),
                "to_date": date.fromisoformat("2021-12-25"),
            }
        ]


def test_price_one_day():
    """
    GIVEN:  A customer requests a one night reservation
    WHEN:   The booking is created
    THEN:   The calculated price equals the room rate
    """
    booking_data = BookingCreateData(
        # room_id=1,
        customer_id=1,
        from_date=date.fromisoformat("2021-12-24"),
        to_date=date.fromisoformat("2021-12-25"),
    )
    booking = create_booking(
        booking_data,
        BookingInterface(),
        RoomInterface(),
    )
    assert booking["price"] == 150_00


def test_date_error():
    """
    GIVEN:  Booking is given same start and end date
    WHEN:   Data is sent
    THEN:   An InvlaidDateError is raised
    """
    booking_data = BookingCreateData(
        # room_id=1,
        customer_id=1,
        from_date=date.fromisoformat("2021-12-24"),
        to_date=date.fromisoformat("2021-12-24"),
    )
    with pytest.raises(InvalidDateError):
        create_booking(booking_data, BookingInterface(), RoomInterface())


def test_check_room_availability():
    """
    GIVEN:  A given room is available on a given date
    WHEN:   A request is made to check the room availability on the given date
    THEN:   The availability request returns true
    """
    assert check_room_availability(
        1, date.fromisoformat("2024-12-23"), BookingInterface()
    )


def test_check_room_not_availability():
    """
    GIVEN:  A given room is not available on a given date
    WHEN:   A request is made to check the room availability on the given date
    THEN:   The availability request returns false
    """
    assert not check_room_availability(
        1, date.fromisoformat("2021-12-24"), BookingInterface()
    )


def test_check_rooms_available():
    """
    GIVEN:  A customer wants a room with a given date range
    WHEN:   Request for room availability with the given date range is made
    THEN:   The correct list of rooms is returned
    """
    assert check_rooms_available(
        date.fromisoformat("2021-12-24"),
        date.fromisoformat("2021-12-27"),
        RoomInterface(),
        BookingInterface(),
    ) == [2, 3, 4, 5]


def test_later_check_rooms_available():
    """
    GIVEN:  A customer wants a room with a given date range when no rooms are booked
    WHEN:   Request for room availability with the given date range is made
    THEN:   The correct list of rooms is returned
    """
    assert check_rooms_available(
        date.fromisoformat("2021-12-04"),
        date.fromisoformat("2021-12-07"),
        RoomInterface(),
        BookingInterface(),
    ) == [1, 2, 3, 4, 5]
