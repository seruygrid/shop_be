from typing import Sequence

from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count

from db_models.db_models import Category, ChildCategory
from shop_be.schemas.category.category import CategoryPaginationRequest, CreateCategoryRequest
from shop_be.services.base import BaseService


class CategoryService(BaseService[Category]):
    MODEL = Category

    async def get_list(self, query_params: CategoryPaginationRequest) -> Sequence['Category']:
        query = query_params.filter_query(
            select(self.MODEL)
        ).options(
            selectinload(self.MODEL.image),
            selectinload(self.MODEL.children).selectinload(ChildCategory.parent),
        ).limit(query_params.limit).offset(query_params.first)
        return await self.fetch_all(query)

    async def get_count(self, query_params: CategoryPaginationRequest) -> int:
        query = query_params.filter_query(select(count(self.MODEL.id)))
        return await self.session.scalar(query) or 0

    async def get_by_slug(self, slug: str) -> Category:
        options = (
            selectinload(self.MODEL.image),
            selectinload(self.MODEL.children).selectinload(ChildCategory.parent),
        )
        return await self.fetch_one(filters=(self.MODEL.slug == slug,), options=options)

    async def create_new(self, data: CreateCategoryRequest) -> Category:
        obj = self.MODEL(
            name=data.name,
            slug=slugify(data.name),
            icon=data.icon,
            image_id=data.image.id,
            details=data.details,
            language=data.language,
            translated_languages=[data.language],
        )
        await self.insert_obj(obj)
        return await self.get_by_slug(obj.slug)

    async def update_category(self, _id: int, data: CreateCategoryRequest) -> Category:
        update_values = dict(
            name=data.name,
            slug=slugify(data.name),
            icon=data.icon,
            iamge_id=data.image.id,
            detaild=data.details,
            language=data.language,
            translated_languages=[data.language],
        )
        await self.update(filters=(self.MODEL.id == _id,), values=update_values)
        return await self.get_by_slug(update_values['slug'])
