from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count

from db_models.db_models import Category, CategoryType, ChildCategory
from shop_be.schemas.category.category import CategoryPaginationRequest
from shop_be.services.base import BaseService


class CategoryService(BaseService[Category]):
    MODEL = Category

    async def get_list(self, query_params: CategoryPaginationRequest) -> list['Category']:
        query = query_params.filter_query(
            select(self.MODEL)
        ).options(
            selectinload(self.MODEL.type).selectinload(CategoryType.promotional_sliders),
            selectinload(self.MODEL.children).selectinload(ChildCategory.parent),
        ).limit(query_params.limit).offset(query_params.first)
        return await self.fetch_all(query)

    async def get_count(self, query_params: CategoryPaginationRequest) -> int:
        query = query_params.filter_query(select(count(self.MODEL.id)))
        return await self.session.scalar(query)
