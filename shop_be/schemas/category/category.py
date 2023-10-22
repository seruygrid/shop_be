from pydantic import BaseModel, Field
from sqlalchemy import Select, text

from db_models.db_models import Category
from shop_be.schemas.category.base import BaseCategorySchema
from shop_be.schemas.category.types import CategoryTypeSchema
from shop_be.schemas.paginate import Paginate


class ParentCategorySchema(BaseCategorySchema):
    parent_id: int | None = None

    class Config:
        from_attributes = True


class ChildrenCategorySchema(BaseCategorySchema):
    parent: ParentCategorySchema
    products_count: int
    parent_id: int
    children: list = []
    products_count: int = 100

    class Config:
        from_attributes = True


class CategorySchema(BaseCategorySchema):
    parent: None = None
    parent_id: int | None = None
    type: CategoryTypeSchema
    children: list[ChildrenCategorySchema]
    products_count: int = 100

    class Config:
        from_attributes = True


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
            query = query.filter(Category.name == self.search)
        if self.language:
            query = query.filter(Category.language == self.language)
        if self.order_by and self.sorted_by:
            query = query.order_by(text(f'{self.order_by} {self.sorted_by}')).group_by(text(self.order_by))
        return query


class PaginatedCategory(Paginate):
    data: list[CategorySchema]
