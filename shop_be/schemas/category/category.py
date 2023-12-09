from typing import Sequence

from pydantic import BaseModel, Field
from sqlalchemy import Select, text

from db_models.db_models import Category
from shop_be.schemas.category.base import BaseCategorySchema
from shop_be.schemas.image import ImageSchema
from shop_be.schemas.paginate import Paginate


class ProductCategorySchema(BaseCategorySchema):
    parent: int | None = Field(None, alias='parent_id')


class ParentCategorySchema(BaseCategorySchema):
    parent_id: int | None = None


class ChildrenCategorySchema(BaseCategorySchema):
    parent: ParentCategorySchema
    products_count: int
    parent_id: int
    children: list = []
    products_count: int = 100


class CategorySchema(BaseCategorySchema):
    parent: None = None
    parent_id: int | None = None
    children: list[ChildrenCategorySchema]
    products_count: int = 100


class CategoryPaginationRequest(BaseModel):
    order_by: str | None = Field(None, alias='orderBy')
    sorted_by: str | None = Field(None, alias='sortedBy')
    search: str | None = None
    language: str | None = None
    first: int = 0
    limit: int = 15
    page: int = 1

    def filter_query(self, query: Select) -> Select:
        if self.search:
            params_keys = {
                'name': lambda value: (Category.name == value),
            }
            search_params = self.search.split(';')
            for param in search_params:
                param_key, param_value = param.split(':')
                if condition := params_keys.get(param_key):
                    query = query.filter(condition(param_value), )
        if self.language:
            query = query.filter(Category.language == self.language)
        if self.order_by and self.sorted_by:
            query = query.order_by(text(f'{self.order_by} {self.sorted_by}')).group_by(text(self.order_by), Category.id)
        return query


class PaginatedCategory(Paginate):
    data: Sequence[CategorySchema]


class CreateCategoryRequest(BaseModel):
    language: str
    name: str
    slug: str
    details: str
    image: ImageSchema
    icon: str
    parent: int | None
