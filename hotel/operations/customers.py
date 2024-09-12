from typing import Optional
from pydantic import BaseModel

from hotel.operations.interface import DataInterface, DataObject

"""
More fields

Currently, customers, rooms and bookings are relatively simple objects. Add a few fields to them 
and verify that you can read and update them via the API. Here are a few examples of fields you could add:

    Customer address information
    A boolean indicating whether a customer wants to receive marketing emails
    A list of amenities (represented by string values) in a room
    A boolean indicating whether a booking can be cancelled or not

"""


class CustomerCreateData(BaseModel):
    first_name: str
    last_name: str
    email_address: str
    street_number: str
    apartment_number: Optional[str] = None
    street: str
    attention: Optional[str] = None
    city: str
    state_province: Optional[str] = None
    post_zip_code: str
    country: Optional[str] = None
    marketing_emails: bool = False


class CustomerUpdateData(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email_address: Optional[str] = None
    apartment_number: Optional[str] = None
    street: Optional[str] = None
    attention: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    post_zip_code: Optional[str] = None
    country: Optional[str] = None
    marketing_emails: Optional[bool] = False


def read_all_customers(customer_interface: DataInterface) -> list[DataObject]:
    return customer_interface.read_all()


def read_customer(customer_id: int, customer_interface: DataInterface) -> DataObject:
    return customer_interface.read_by_id(customer_id)


def create_customer(
    data: CustomerCreateData, customer_interface: DataInterface
) -> DataObject:
    customer_dict = data.model_dump()
    return customer_interface.create(customer_dict)


def update_customer(
    customer_id: int, data: CustomerUpdateData, customer_interface: DataInterface
):
    update_data = data.model_dump(exclude_unset=True, exclude_none=True)
    return customer_interface.update(customer_id, update_data)


def delete_customer(customer_id: int, customer_interface: DataInterface) -> DataObject:
    return customer_interface.delete(customer_id)
