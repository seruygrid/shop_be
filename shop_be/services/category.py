from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.sql.functions import count

from db_models.db_models import ProductType, Shop, Category
from shop_be.schemas.category.category import CategoryPaginationRequest
from shop_be.services.base import BaseService


class CategoryService(BaseService[Category]):
    MODEL = Category

    async def get_list(self, query_params: CategoryPaginationRequest) -> list['Category']:
        query = select(self.MODEL).options(
            selectinload(self.MODEL.type).selectinload(ProductType.promotional_sliders),
            selectinload(self.MODEL.shop).selectinload(Shop.cover_image),
            selectinload(self.MODEL.shop).selectinload(Shop.logo),
            joinedload(self.MODEL.rating_count),
            joinedload(self.MODEL.categories),
        )
        query = query_params.filter_query(query)
        return await self.fetch_all(query)

    async def get_count(self, query_params: CategoryPaginationRequest) -> int:
        query = query_params.filter_query(select(count(self.MODEL.id)), is_paginate=False)
        return await self.session.scalar(query)
