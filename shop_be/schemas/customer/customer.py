from datetime import datetime

from pydantic import BaseModel, EmailStr

from shop_be.schemas.address import CustomerAddressSchema
from shop_be.schemas.image import ImageSchema


class CognitoCustomerSchema(BaseModel):
    sub: str
    email: EmailStr | None


class BaseProfileSchema(BaseModel):
    avatar: ImageSchema
    bio: str
    socials: dict | list | None
    contact: str

    class Config:
        from_attributes = True


class ProfileSchema(BaseProfileSchema):
    id: int
    customer_id: int
    created_at: datetime
    updated_at: datetime


class CustomerProfile(BaseProfileSchema):
    customer: dict


class BaseCustomerSchema(BaseModel):
    id: int
    name: str
    email: EmailStr
    email_verified_at: datetime | None
    created_at: datetime
    updated_at: datetime
    is_active: int
    shop_id: int | None = None
    profile: ProfileSchema | None

    class Config:
        from_attributes = True


class PermissionSchema(BaseModel):
    id: int
    name: str
    guard_name: str
    created_at: datetime
    updated_at: datetime
    pivot: dict

    class Config:
        from_attributes = True


class CreateCustomerResponse(BaseCustomerSchema):
    address: list[CustomerAddressSchema] | None
    permissions: list[PermissionSchema] | None
