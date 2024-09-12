from datetime import date
from hotel.operations.interface import DataInterface, DataObject


def string_room_amenities(room: DataObject) -> DataObject:
    if "amenities" in room:
        room["amenities"] = ", ".join([c["name"] for c in room["amenities"]])

    return room


def read_all_rooms(room_interface: DataInterface) -> list[DataObject]:
    all_rooms = [string_room_amenities(room) for room in room_interface.read_all()]
    return all_rooms


def read_room(room_id: int, room_interface: DataInterface) -> DataObject:
    room = room_interface.read_by_id(room_id)
    room = string_room_amenities(room)

    return room


def check_room_availability(
    room_id: int, query_date: date, booking_interface: DataInterface
) -> bool:
    room_bookings = booking_interface.read_all()

    for booking in room_bookings:
        if (
            booking["room_id"] == room_id
            and query_date >= booking["from_date"]
            and query_date <= booking["to_date"]
        ):
            return False
    return True


def check_rooms_available(
    start: date,
    end: date,
    room_interface: DataInterface,
    booking_interface: DataInterface,
) -> list[int]:
    rooms = room_interface.read_all()
    rooms_available = [room["id"] for room in rooms]
    room_bookings = booking_interface.read_all()

    for booking in room_bookings:
        if (booking["from_date"] <= start <= booking["to_date"]) or (
            booking["from_date"] <= end <= booking["to_date"]
        ):
            if booking["room_id"] in rooms_available:
                rooms_available.remove(booking["room_id"])
    return rooms_available


def create_room_amenity(
    room_id: int,
    amenity_id: int,
    room_interface: DataInterface,
    amenity_interface: DataInterface,
):
    room = room_interface.read_by_id(room_id)
    amenity = amenity_interface.read_by_id(amenity_id)
    room["amenities"] = room.setdefault("amenities", list())
    room["amenities"].append(amenity)
    updated_room = room_interface.update(room_id, room)
    updated_room = string_room_amenities(updated_room)

    return updated_room


def delete_room_amenity(
    room_id: int,
    amenity_id: int,
    room_interface: DataInterface,
    amenity_interface: DataInterface,
):
    room = room_interface.read_by_id(room_id)
    amenity = amenity_interface.read_by_id(amenity_id)

    if "amenities" in room.keys():
        room["amenities"].remove(amenity)

    updated_room = room_interface.update(room_id, room)
    updated_room = string_room_amenities(updated_room)

    return updated_room
