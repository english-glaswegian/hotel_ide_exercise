from hotel.operations.interface import DataObject


class DataInterfaceStub:
    def read_by_id(self, id: int) -> DataObject:
        raise NotImplementedError()

    def read_all(self) -> list[DataObject]:
        raise NotImplementedError()

    def create(self, data: DataObject) -> DataObject:
        raise NotImplementedError()

    def update(self, id: int, data: DataObject) -> DataObject:
        raise NotImplementedError()

    def delete(self, id: int) -> DataObject:
        raise NotImplementedError()
