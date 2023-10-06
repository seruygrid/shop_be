from pydantic import BaseModel, Field
from sqlalchemy import Select

from db_models.db_models import Category
from shop_be.schemas.image import ImageSchema
from shop_be.schemas.paginate import Paginate


class CategorySchema(BaseModel):
    id: int
    name: str
    slug: str
    language: str
    icon: str | None = None
    image: ImageSchema | None = None
    details: str | None = None
    parent: int
    type_id: int
    created_at: str
    updated_at: str
    deleted_at: str | None = None
    parent_id: int
    translated_languages: list[str]


class CategoryPaginationRequest(BaseModel):
    order_by: str | None = Field(None, alias='orderBy')
    sorted_by: str | None = Field(None, alias='sortedBy')
    search: str | None = None
    language: str | None = None
    first: int = 1
    limit: int = 30
    page: int = 1

    def filter_query(self, query: Select, is_paginate: bool = True) -> Select:
        if not self.search:
            query = query.filter(Category.name.like(f'%{self.search}%'))
        if self.language:
            query = query.filter(Category.language == self.language)
        if is_paginate:
            query = query.limit(self.limit).offset(self.first)
        return query


class PaginatedCategory(Paginate):
    data: list[CategorySchema]
