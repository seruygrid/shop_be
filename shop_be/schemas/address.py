from pydantic import BaseModel

from db_models.db_models import CustomerAddressType


class AddressSchema(BaseModel):
    zip: str
    city: str
    state: str
    country: str
    street_address: str

    class Config:
        from_attributes = True


class CustomerAddressSchema(BaseModel):
    customer_id: int
    title: str
    type: CustomerAddressType
    default: bool
    address: AddressSchema

    class Config:
        from_attributes = True
