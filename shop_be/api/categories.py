from http import HTTPStatus

from fastapi import APIRouter, Depends

from shop_be.api.dependencies.services import get_category_service
from shop_be.api.pagination.category import paginate_categories
from shop_be.schemas.category.category import CategoryPaginationRequest, PaginatedCategory
from shop_be.services.category import CategoryService

router = APIRouter()


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
