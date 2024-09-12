from pydantic import BaseModel
from sqlite3 import IntegrityError

from hotel.operations.interface import DataInterface, DataObject
from hotel.operations.rooms import read_all_rooms


class RoomHasAmenityError(Exception):
    name: str


class DuplicateAmenityError(Exception):
    pass


class AmenityCreateData(BaseModel):
    name: str


class AmenityUpdateData(BaseModel):
    name: str


def read_all_amenities(amenity_interface: DataInterface) -> list[DataObject]:
    return amenity_interface.read_all()


def read_amenity(amenity_id: int, amenity_interface: DataInterface) -> DataObject:
    return amenity_interface.read_by_id(amenity_id)


def create_amenity(
    data: AmenityCreateData, amenity_interface: DataInterface
) -> DataObject:
    amenity_dict = data.model_dump()

    try:
        result = amenity_interface.create(amenity_dict)
    except IntegrityError:
        raise DuplicateAmenityError()

    return result


def update_amenity(
    amenity_id: int, data: AmenityUpdateData, amenity_interface: DataInterface
):
    update_data = data.model_dump(exclude_unset=True, exclude_none=True)

    try:
        result = amenity_interface.update(amenity_id, update_data)
    except IntegrityError:
        raise DuplicateAmenityError

    return result


def delete_amenity(
    amenity_id: int, amenity_interface: DataInterface, room_interface: DataInterface
) -> DataObject:
    room_list = read_all_rooms(room_interface)
    amenity = read_amenity(amenity_id, amenity_interface)

    for room in room_list:
        if "amenities" in room.keys():
            if amenity["name"] in room["amenities"]:
                raise RoomHasAmenityError()

    return amenity_interface.delete(amenity_id)
