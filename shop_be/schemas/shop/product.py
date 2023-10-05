from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field

from db_models.db_models import Product
from shop_be.schemas.category.category import CategorySchema
from shop_be.schemas.image import ImageSchema
from shop_be.schemas.paginate import Paginate
from shop_be.schemas.rating.rating import RatingCount
from shop_be.schemas.shop.shop import ShopSchema


class ProductSchema(BaseModel):
    id: int
    name: str
    slug: str
    description: str
    type_id: int
    price: float
    shop_id: int
    sale_price: float
    language: str
    min_price: float
    max_price: float
    sku: str
    quantity: int
    in_stock: int
    is_taxable: int
    shipping_class_id: int | None = None
    status: str
    product_type: str
    unit: str
    height: float | None = None
    width: float | None = None
    length: float | None = None
    image: ImageSchema
    video: str | None = None
    gallery: list[ImageSchema]
    deleted_at: str | None = None
    created_at: str
    updated_at: str
    author_id: int | None = None
    manufacturer_id: int | None = None
    is_digital: int
    is_external: int
    external_product_url: str | None = None
    external_product_button_text: str | None = None
    ratings: float
    total_reviews: int
    rating_count: list[RatingCount]
    my_review: str | None = None
    in_wishlist: bool
    blocked_dates: list[str]
    translated_languages: list[str]
    categories: list[CategorySchema]
    shop: ShopSchema
    type: dict
    related_products: list | None = []


class ProductPaginationRequest(BaseModel):
    order_by: str | None = Field(None, alias='orderBy')
    sorted_by: str | None = Field(None, alias='sortedBy')
    search_join: str | None = Field(None, alias='searchJoin')
    search: str | None = None
    date_range: datetime | None = None
    language: str | None = None
    first: int = 1
    limit: int = 30
    page: int = 1

    def filter_query(self, query: Query, is_paginate: bool = True) -> Query:
        if not self.search:
            query = query.filter(Product.name.like(f'%{self.search}%'))
        if self.language:
            query = query.filter(Product.language == self.language)
        if is_paginate:
            query = query.limit(self.limit).offset(self.first)
        return query


class PaginatedProduct(Paginate):
    data: list[ProductSchema]
