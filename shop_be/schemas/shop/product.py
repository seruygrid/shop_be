from datetime import datetime

from fastapi import Query
from pydantic import BaseModel, Field
from sqlalchemy import text

from db_models.db_models import Product
from shop_be.schemas.category.category import ProductCategorySchema
from shop_be.schemas.category.types import BaseProductTypeSchema
from shop_be.schemas.image import ImageSchema
from shop_be.schemas.paginate import Paginate
from shop_be.schemas.rating.rating import RatingCount
from shop_be.schemas.shop.shop import BaseShopSchema


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
    created_at: datetime
    updated_at: datetime
    author_id: int | None = None
    manufacturer_id: int | None = None
    is_digital: int
    is_external: int
    external_product_url: str | None = None
    external_product_button_text: str | None = None
    ratings: float | None
    total_reviews: int | None = None
    rating_count: list[RatingCount]
    my_review: str | None = None
    in_wishlist: bool
    blocked_dates: list[str] | None = None
    translated_languages: list[str]
    categories: list[ProductCategorySchema]
    shop: BaseShopSchema
    type: BaseProductTypeSchema
    variations: list = []
    metas: list = []
    manufacturer: None = None
    variation_options: list = []
    tags: list = []

    class Config:
        from_attributes = True


class ProductPaginationRequest(BaseModel):
    order_by: str | None = Field(None, alias='orderBy')
    sorted_by: str | None = Field(None, alias='sortedBy')
    search_join: str | None = Field(None, alias='searchJoin')
    search: str | None = None
    date_range: datetime | None = None
    language: str | None = None
    first: int = 0
    limit: int = 15
    page: int = 1

    def filter_query(self, query: Query) -> Query:
        # if self.search:
        #     query = query.filter(Product.name == self.search)
        if self.language:
            query = query.filter(Product.language == self.language)
        if self.order_by and self.sorted_by:
            query = query.order_by(text(f'{self.order_by} {self.sorted_by}')).group_by(text(self.order_by))
        return query


class PaginatedProduct(Paginate):
    data: list[ProductSchema]
