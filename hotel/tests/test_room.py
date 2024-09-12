from hotel.operations.rooms import string_room_amenities, read_all_rooms

from hotel.tests.test_room_amenity import RoomInterface1


def test_string_room_amenities():
    """
    GIVEN: A room object with an amenity list of amenity dictionaries
    WHEN:  The object is passed the string_room_amenities function
    THEN:  The returned dictionary contains the amenity names as a coma separated list
    """
    room_interface = RoomInterface1()
    input = room_interface.read_by_id(1)
    output = string_room_amenities(input)
    assert output["amenities"] == "Wi-Fi, Air Conditioning"


def test_string_no_room_amenities():
    """
    GIVEN: A room object with no amenities
    WHEN:  The object is passed the string_room_amenities function
    THEN:  The returned dictionary equals the input
    """
    room_interface = RoomInterface1()
    input = room_interface.read_by_id(1)
    output = string_room_amenities(input)
    assert input == output


def test_read_all_rooms_size():
    """
    GIVEN:  A defined number of rooms
    WHEN:   All room data is requested
    THEN:   The correct number of rooms is returned
    """
    room_list = read_all_rooms(RoomInterface1())
    assert len(room_list) == 5


def test_read_all_rooms_string_amenities():
    """
    GIVEN:  A defined number of rooms, some of which list amenities
    WHEN:   All room data is requested
    THEN:   The expected rooms have the correct amenity strings
    """
    room_list = read_all_rooms(RoomInterface1())
    assert room_list[0]["amenities"] == "Wi-Fi, Air Conditioning"
    assert room_list[1]["amenities"] == "Air Conditioning"
    assert room_list[3]["amenities"] == "Wi-Fi"
