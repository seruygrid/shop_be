from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql.functions import count

from db_models.db_models import Product, ProductType, Shop
from shop_be.conf.constants import ErrorMessages
from shop_be.exceptions import DoesNotExistException
from shop_be.schemas.shop.product import ProductPaginationRequest
from shop_be.services.base import BaseService


class ProductService(BaseService[Product]):
    MODEL = Product

    async def get_list(self, query_params: ProductPaginationRequest) -> list['Product']:
        query = select(self.MODEL).options(
            selectinload(self.MODEL.type).selectinload(ProductType.promotional_sliders),
            selectinload(self.MODEL.shop).selectinload(Shop.cover_image),
            selectinload(self.MODEL.shop).selectinload(Shop.logo),
            joinedload(self.MODEL.rating_count),
            joinedload(self.MODEL.categories),
        )
        query = query_params.filter_query(query)
        return await self.fetch_all(query)

    async def get_count(self, query_params: ProductPaginationRequest) -> int:
        query = query_params.filter_query(select(count(self.MODEL.id)), is_paginate=False)
        return await self.session.scalar(query)

    async def get_by_slug(self, slug: str) -> 'Product':
        options = (
            selectinload(self.MODEL.type).selectinload(ProductType.promotional_sliders),
            selectinload(self.MODEL.shop).selectinload(Shop.cover_image),
            selectinload(self.MODEL.shop).selectinload(Shop.logo),
            joinedload(self.MODEL.rating_count),
            joinedload(self.MODEL.categories),
        )
        if obj := await self.fetch_one(filters=(self.MODEL.slug == slug,), options=options):
            return obj
        raise DoesNotExistException(ErrorMessages.PRODUCT_DOES_NOT_EXIST)
