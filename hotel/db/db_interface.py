from typing import List, Any


from hotel.db.models import Base, to_dict, DBAmenity
from hotel.db.engine import DBSession

DataObject = dict[str, Any]


class DBInterface:
    def __init__(self, db_class: type[Base]):
        self.db_class = db_class

    def read_by_id(self, id: int) -> DataObject:
        session = DBSession()
        result = session.query(self.db_class).get(id)
        return to_dict(result)

    def read_all(self) -> List[DataObject]:
        session = DBSession()
        results = session.query(self.db_class).all()
        return [to_dict(r) for r in results]

    def create(self, data: DataObject) -> DataObject:
        session = DBSession()
        result = self.db_class(**data)
        session.add(result)
        session.commit()
        return to_dict(result)

    def update(self, id: int, data: DataObject) -> DataObject:
        session = DBSession()
        item: Base | None = session.query(self.db_class).get(id)

        for key, value in data.items():
            if key == "amenities":
                # and value:
                new_value = list()

                for amenity in value:
                    new_value.append(session.query(DBAmenity).get(amenity["id"]))
                setattr(item, key, new_value)
            elif key != "amenities":
                setattr(item, key, value)

        session.commit()
        return to_dict(item)

    def delete(self, id: int) -> DataObject:
        session = DBSession()
        result = session.query(self.db_class).get(id)
        session.delete(result)
        session.commit()
        session.close()
        return to_dict(result)
