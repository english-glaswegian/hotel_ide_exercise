import pytest

from hotel.operations.amenities import (
    RoomHasAmenityError,
    delete_amenity,
    read_all_amenities,
    read_amenity,
    AmenityCreateData,
    AmenityUpdateData,
    create_amenity,
    update_amenity,
)

from hotel.operations.interface import DataObject
from hotel.tests.data_interface_stub import DataInterfaceStub

from hotel.tests.test_room_amenity import RoomInterface1


class AmenityInterface(DataInterfaceStub):
    def create(self, data: DataObject) -> DataObject:
        amenity = dict(data)
        amenity["id"] = 2
        return amenity

    def read_by_id(self, id: int) -> DataObject:
        data = self.read_all()
        return data[id - 1]

    def read_all(self) -> list[DataObject]:
        return [
            {"id": 1, "name": "Wi-Fi"},
            {"id": 2, "name": "Air Conditioning"},
            {"id": 3, "name": "Bath Tub"},
        ]

    def update(self, id: int, data: DataObject) -> DataObject:
        return {"id": id, "name": data["name"]}

    def delete(self, id: int) -> DataObject:
        return {"id": id, "name": "Spa Bathtub"}


def test_read_all():
    """
    GIVEN: A defined set of amenities
    WHEN:  A request is made to list all amenities
    THEN:  The correct set is returned
    """
    assert read_all_amenities(AmenityInterface()) == [
        {"id": 1, "name": "Wi-Fi"},
        {"id": 2, "name": "Air Conditioning"},
        {"id": 3, "name": "Bath Tub"},
    ]


def test_read_by_id():
    """
    GIVEN: A defined set of amenities
    WHEN:  A request is made to list a particular amenity by id
    THEN:  The correct data is returned
    """
    assert read_amenity(3, AmenityInterface()) == {"id": 3, "name": "Bath Tub"}


def test_create_data():
    """
    GIVEN:  A pre-existing set of amenities
    WHEN:   Data for a new amenity is sent
    THEN:   The amenity data is returned with an assigned id
    """
    amenity_data = AmenityCreateData(name="Coffee Maker")
    assert create_amenity(amenity_data, AmenityInterface()) == {
        "id": 2,
        "name": "Coffee Maker",
    }


def test_update_data():
    """
    GIVEN: A pre-existing set of amenities
    WHEN:  Updated data is sent for a particular id
    THEN:  The amenity data is returned for the id with the updates applied
    """
    amenity_data = AmenityUpdateData(name="Alarm Radio")
    assert update_amenity(3, amenity_data, AmenityInterface()) == {
        "id": 3,
        "name": "Alarm Radio",
    }


def test_delete_used_amenity():
    """
    GIVEN: An amenity is assigned to a room
    WHEN:  A request is made to delete the amenity
    THEN:  A RoomHasAmenityError error is raised
    """
    with pytest.raises(RoomHasAmenityError):
        delete_amenity(1, AmenityInterface(), RoomInterface1())
