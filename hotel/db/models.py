from typing import Any, List

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.types import Boolean


Base = declarative_base()


def to_dict(obj: Base) -> dict[str, Any]:
    out = {c.name: getattr(obj, c.name) for c in obj.__table__.columns}

    if isinstance(obj, DBRoom) and obj.amenities:
        out["amenities"] = [{"id": c.id, "name": c.name} for c in obj.amenities]

    return out


class DBCustomer(Base):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(250), nullable=False)
    last_name = Column(String(250), nullable=False)
    email_address = Column(String(250), nullable=False)
    street_number = Column(String(50), nullable=False)
    apartment_number = Column(String(50), nullable=True)
    street = Column(String(250), nullable=False)
    attention = Column(String(250), nullable=True)
    city = Column(String(200), nullable=False)
    state_province = Column(String(200), nullable=True)
    post_zip_code = Column(String(200), nullable=False)
    country = Column(String(200), nullable=True)
    marketing_emails = Column(Boolean, nullable=False)


class DBAmenity(Base):
    __tablename__ = "amenity"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=True)


room_amenities = Table(
    "room_amenities",
    Base.metadata,
    Column("id", ForeignKey("room.id"), primary_key=True),
    Column("amenity_id", ForeignKey("amenity.id"), primary_key=True),
    Column("name", String(200), nullable=False),
)


class DBRoom(Base):
    __tablename__ = "room"
    # id = Column(Integer, primary_key=True, autoincrement=True)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number = Column(String(250), nullable=False)
    size = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    amenities: Mapped[List[DBAmenity]] = relationship(secondary=room_amenities)


class DBBooking(Base):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, autoincrement=True)
    from_date = Column(Date, nullable=False)
    to_date = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    can_be_cancelled = Column(Boolean, default=True, nullable=False)
    customer_id = Column(Integer, ForeignKey("customer.id"))
    customer = relationship(DBCustomer)
    room_id = Column(Integer, ForeignKey("room.id"))
    room = relationship(DBRoom)


# TODO: A list of amenities (represented by string values) in a room
