from http import HTTPStatus

from fastapi import APIRouter, Depends

from db_models.db_models import Category
from shop_be.api.dependencies.auth import auth_admin
from shop_be.api.dependencies.logger import LoggingRoute
from shop_be.api.dependencies.services import get_category_service
from shop_be.api.pagination.category import paginate_categories
from shop_be.schemas.category.category import (
    CategoryPaginationRequest,
    PaginatedCategory,
    CreateCategoryRequest,
    CategorySchema,
)
from shop_be.services.category import CategoryService

router = APIRouter(route_class=LoggingRoute)


@router.get(
    '/categories',
    summary='Get categories',
    status_code=HTTPStatus.OK,
    response_model=PaginatedCategory,
)
async def get_categories(
        query_params: CategoryPaginationRequest = Depends(),
        category_service: CategoryService = Depends(get_category_service),
) -> PaginatedCategory:
    products = await category_service.get_list(query_params)
    total_count = await category_service.get_count(query_params)
    return paginate_categories(products, total_count, query_params)


@router.get(
    '/categories/{slug}',
    summary='Get category by slug',
    status_code=HTTPStatus.OK,
    response_model=CategorySchema,
)
async def get_category_by_slug(
        slug: str,
        category_service: CategoryService = Depends(get_category_service),
) -> 'Category':
    return await category_service.get_by_slug(slug)


@router.post(
    '/categories',
    summary='Create new category',
    status_code=HTTPStatus.CREATED,
    response_model=CategorySchema,
    dependencies=[Depends(auth_admin)]
)
async def create_new_category(
        request_data: CreateCategoryRequest,
        category_service: CategoryService = Depends(get_category_service),
) -> 'Category':
    return await category_service.create_new(request_data)


@router.put(
    '/categories/{_id}',
    summary='Update category',
    status_code=HTTPStatus.OK,
    response_model=CategorySchema,
    dependencies=[Depends(auth_admin)],
)
async def update_category(
        _id: int,
        request_data: CreateCategoryRequest,
        category_service: CategoryService = Depends(get_category_service),
) -> 'Category':
    return await category_service.update_category(_id, request_data)
