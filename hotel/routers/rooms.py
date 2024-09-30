from datetime import date

from fastapi import APIRouter

from hotel.db.db_interface import DBInterface
from hotel.db.models import DBAmenity, DBBooking, DBRoom
from hotel.operations.rooms import (
    delete_room_amenity,
    read_all_rooms,
    read_room,
    check_room_availability,
    check_rooms_available,
    create_room_amenity,
)


router = APIRouter()


@router.get("/rooms")
def api_read_all_rooms():
    room_interface = DBInterface(DBRoom)
    return read_all_rooms(room_interface)


@router.get("/rooms/{room_id}")
def api_read_room(room_id: int):
    room_interface = DBInterface(DBRoom)
    return read_room(room_id, room_interface)


# TODO: Check room availability
# Create an API endpoint for checking whether a room is available. The endpointshould
# should receive a room id and a date and that returns whether the room with
# the id is available at that date. Extend the various layers in the
# application as needed to achieve this.
@router.get("/rooms/{room_id}/{date}")
def api_check_room_availability(room_id: int, date: date):
    booking_interface = DBInterface(DBBooking)
    return check_room_availability(room_id, date, booking_interface)


# TODO: Check room availability (advanced)
# Create an API endpoint that retrieves the rooms that are available within a
# given date range. The endpoint should receive a start date and end date and
# then return a list of rooms that are available within the date range. Only
# include rooms that are fully available within the date range.
@router.get("/rooms_available/{start}/{end}")
def api_check_rooms_available(start: date, end: date):
    booking_interface = DBInterface(DBBooking)
    room_interface = DBInterface(DBRoom)
    return check_rooms_available(start, end, room_interface, booking_interface)


@router.post("/rooms/{room_id}/{amenity_id}")
def api_create_room_amenity(room_id, amenity_id):
    room_interface = DBInterface(DBRoom)
    amenity_interface = DBInterface(DBAmenity)
    return create_room_amenity(room_id, amenity_id, room_interface, amenity_interface)


@router.delete("/rooms/{room_id}/{amenity_id}")
def api_delete_room_amenity(room_id, amenity_id):
    room_interface = DBInterface(DBRoom)
    amenity_interface = DBInterface(DBAmenity)
    return delete_room_amenity(room_id, amenity_id, room_interface, amenity_interface)
