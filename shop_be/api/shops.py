from http import HTTPStatus

from fastapi import APIRouter, Depends

from db_models.db_models import Shop
from shop_be.api.dependencies.services import get_shop_service
from shop_be.api.pagination.shops import paginate_shops
from shop_be.schemas.shop.shop import ShopPaginationRequest, PaginatedShops, ShopSchema
from shop_be.services.shop import ShopService

router = APIRouter()


@router.get(
    '/shops',
    summary='Get shops list',
    status_code=HTTPStatus.OK,
    response_model=PaginatedShops,
)
async def get_shops(
        query_params: ShopPaginationRequest = Depends(),
        shop_service: ShopService = Depends(get_shop_service),
) -> PaginatedShops:
    products = await shop_service.get_list(query_params)
    total_count = await shop_service.get_count(query_params)
    return paginate_shops(products, total_count, query_params)


@router.get(
    '/shops/{slug}',
    summary='Get shop by slug',
    status_code=HTTPStatus.OK,
    response_model=ShopSchema,
)
async def get_shop_by_slug(
        slug: str,
        shop_service: ShopService = Depends(get_shop_service),
) -> Shop:
    return await shop_service.get_by_slug(slug)
