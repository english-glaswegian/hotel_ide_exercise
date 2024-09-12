from hotel.operations.rooms import create_room_amenity, delete_room_amenity

from hotel.operations.interface import DataObject
from hotel.tests.data_interface_stub import DataInterfaceStub


class RoomInterface1(DataInterfaceStub):
    def read_by_id(self, id: int) -> DataObject:
        data = self.read_all()
        return data[id - 1]

    def update(self, id: int, data: DataObject):
        return {
            "id": 1,
            "number": "101",
            "size": 10,
            "price": 150_00,
            "amenities": [{"id": 1, "name": "Wi-Fi"}],
        }

    def read_all(self) -> list[DataObject]:
        return [
            {
                "id": 1,
                "number": "101",
                "size": 10,
                "price": 15000,
                "amenities": [
                    {"id": 1, "name": "Wi-Fi"},
                    {"id": 2, "name": "Air Conditioning"},
                ],
            },
            {
                "id": 2,
                "number": "102",
                "size": 10,
                "price": 15000,
                "amenities": [{"id": 2, "name": "Air Conditioning"}],
            },
            {"id": 3, "number": "103", "size": 20, "price": 25000},
            {
                "id": 4,
                "number": "104",
                "size": 20,
                "price": 25000,
                "amenities": [{"id": 1, "name": "Wi-Fi"}],
            },
            {"id": 5, "number": "105", "size": 30, "price": 35000},
        ]


class RoomInterface2(DataInterfaceStub):
    def read_by_id(self, id: int) -> DataObject:
        return {"id": id, "number": "101", "size": 10, "price": 150_00}

    def update(self, id: int, data: DataObject):
        return {"id": 1, "number": "101", "size": 10, "price": 150_00}


class AmenityInterface(DataInterfaceStub):
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


def test_add_room_amenity():
    """
    GIVEN:  An amenity needs to be added to a room
    WHEN:   The amenity and room ids are sent
    THEN:   The room data with the added amenity is returned
    """
    out = create_room_amenity(4, 1, RoomInterface1(), AmenityInterface())
    assert out["amenities"] == "Wi-Fi"


def test_delete_room_amenity():
    """
    GIVEN:  An amenity needs to be removed from a room
    WHEN:   The amenity and room ids are sent
    THEN:   The room data with the amenity removed is returned
    """
    out = delete_room_amenity(1, 2, RoomInterface1(), AmenityInterface())
    assert out["amenities"] == "Wi-Fi"


def test_delete_room_amenity_zero():
    """
    GIVEN:  An amenity needs to be removed from a room and it's the only amenity
            associated with the room
    WHEN:   The amenity and room ids are sent
    THEN:   The room data is returned with no 'amenities' key
    """
    out = delete_room_amenity(1, 1, RoomInterface2(), AmenityInterface())
    assert "amenities" not in out.keys()
