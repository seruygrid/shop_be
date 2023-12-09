from http import HTTPStatus

from fastapi import APIRouter, Depends

from db_models.db_models import Shop, Customer
from shop_be.api.dependencies.auth import auth_admin
from shop_be.api.dependencies.logger import LoggingRoute
from shop_be.api.dependencies.services import get_shop_service
from shop_be.api.pagination.shops import paginate_shops
from shop_be.schemas.base import OKSchema
from shop_be.schemas.shop.shop import (
    ShopPaginationRequest,
    PaginatedShops,
    ShopSchema,
    CreateShopSchema,
    ApproveShopRequest,
)
from shop_be.services.shop import ShopService

router = APIRouter(route_class=LoggingRoute)


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


@router.post(
    '/shops',
    summary='Create shop',
    status_code=HTTPStatus.CREATED,
    response_model=ShopSchema,
)
async def create_new_shop(
        request_data: CreateShopSchema,
        customer: 'Customer' = Depends(auth_admin),
        shop_service: ShopService = Depends(get_shop_service),
) -> 'Shop':
    return await shop_service.create(request_data, customer)


@router.put(
    '/shops/{_id}',
    summary='Update shop info',
    status_code=HTTPStatus.OK,
    response_model=ShopSchema,
    dependencies=[Depends(auth_admin)],
)
async def update_shop(
        _id: int,
        request_data: CreateShopSchema,
        shop_service: ShopService = Depends(get_shop_service),
) -> Shop:
    return await shop_service.update_shop(_id, request_data)


@router.post(
    '/shops/approve',
    summary='Update shop approve status',
    status_code=HTTPStatus.OK,
    response_model=OKSchema,
    dependencies=[Depends(auth_admin)],
)
async def approve_shop(
        request_data: ApproveShopRequest,
        shop_service: ShopService = Depends(get_shop_service),
) -> OKSchema:
    await shop_service.change_shop_status(request_data.id, value=True)
    return OKSchema()


@router.post(
    '/shops/disapprove',
    summary='Update shop approve status',
    status_code=HTTPStatus.OK,
    response_model=OKSchema,
    dependencies=[Depends(auth_admin)],
)
async def disapprove_shop(
        request_data: ApproveShopRequest,
        shop_service: ShopService = Depends(get_shop_service),
) -> OKSchema:
    await shop_service.change_shop_status(request_data.id, value=False)
    return OKSchema()


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
