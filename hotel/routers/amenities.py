from fastapi import APIRouter

from hotel.db.db_interface import DBInterface
from hotel.db.models import DBAmenity, DBRoom
from hotel.operations.amenities import (
    AmenityCreateData,
    AmenityUpdateData,
    delete_amenity,
    read_all_amenities,
    read_amenity,
    create_amenity,
    update_amenity,
)

router = APIRouter()


@router.get("/amenities")
def api_read_all_amenities():
    amenity_interface = DBInterface(DBAmenity)
    return read_all_amenities(amenity_interface)


@router.get("/amenity/{amenity_id}")
def api_read_amenity(amenity_id: int):
    amenity_interface = DBInterface(DBAmenity)
    return read_amenity(amenity_id, amenity_interface)


@router.post("/amenity")
def api_create_amenity(amenity: AmenityCreateData):
    amenity_interface = DBInterface(DBAmenity)
    return create_amenity(amenity, amenity_interface)


@router.post("/amenity/{amenity_id}")
def api_update_amenity(amenity_id: int, amenity: AmenityUpdateData):
    amenity_interface = DBInterface(DBAmenity)
    return update_amenity(amenity_id, amenity, amenity_interface)


@router.delete("/amenity/{amenity_id}")
def api_delete_amenity(amenity_id: int):
    room_interface = DBInterface(DBRoom)
    amenity_interface = DBInterface(DBAmenity)
    return delete_amenity(amenity_id, amenity_interface, room_interface)
