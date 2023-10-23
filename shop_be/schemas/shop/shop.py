from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, HttpUrl, Field

from db_models.db_models import Shop
from shop_be.schemas.image import ImageSchema
from shop_be.schemas.paginate import Paginate
from shop_be.schemas.shop.owner import ShopOwnerSchema


class LocationSchema(BaseModel):
    lat: str
    lng: str
    city: str
    state: str
    country: str
    formattedAddress: str

    class Config:
        from_attributes = True


class ShopSettingsSchema(BaseModel):
    contact: str
    socials: list
    website: HttpUrl
    location: LocationSchema

    class Config:
        from_attributes = True


class AddressSchema(BaseModel):
    zip: str
    city: str
    state: str
    country: str
    street_address: str

    class Config:
        from_attributes = True


class BaseShopSchema(BaseModel):
    id: int
    owner_id: int
    name: str
    slug: str
    description: str
    is_active: bool
    cover_image: ImageSchema
    logo: ImageSchema
    address: AddressSchema
    settings: ShopSettingsSchema
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ShopSchema(BaseShopSchema):
    orders_count: int = 100
    products_count: int = 100
    owner: ShopOwnerSchema


class ShopPaginationRequest(BaseModel):
    order_by: str | None = Field(None, alias='orderBy')
    sorted_by: str | None = Field(None, alias='sortedBy')
    search: str | None = None
    first: int = 0
    limit: int = 15
    page: int = 1

    def filter_query(self, query: Query) -> Query:
        if self.search:
            query = query.filter(Shop.name == self.search)
        return query


class PaginatedShops(Paginate):
    data: list[ShopSchema]
