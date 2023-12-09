from http import HTTPStatus

from fastapi import APIRouter, Depends

from db_models.db_models import Customer
from shop_be.api.dependencies.auth import auth_admin
from shop_be.api.dependencies.logger import LoggingRoute
from shop_be.api.dependencies.services import get_product_service
from shop_be.api.pagination.product import paginate_products
from shop_be.schemas.shop.product import ProductPaginationRequest, ProductSchema, PaginatedProduct, CreateProductRequest
from shop_be.services.product import ProductService

router = APIRouter(route_class=LoggingRoute)


@router.get(
    '/products',
    summary='Get list of products',
    status_code=HTTPStatus.OK,
    response_model=PaginatedProduct,
)
async def get_products(
        query_params: ProductPaginationRequest = Depends(),
        product_service: ProductService = Depends(get_product_service),
) -> PaginatedProduct:
    products = await product_service.get_list(query_params)
    total_count = await product_service.get_count(query_params)
    return paginate_products(products, total_count, query_params)


@router.get(
    '/products/{slug}',
    summary='Get product by slug',
    status_code=HTTPStatus.OK,
    response_model=ProductSchema,
)
async def get_product(
        slug: str,
        product_service: ProductService = Depends(get_product_service),
) -> ProductSchema:
    return await product_service.get_by_slug(slug)


@router.post(
    '/products',
    summary='Create a new product',
    status_code=HTTPStatus.CREATED,
    response_model=ProductSchema,
)
async def create_new_product(
        request_data: CreateProductRequest,
        customer: 'Customer' = Depends(auth_admin),
        product_service: ProductService = Depends(get_product_service),
) -> ProductSchema:
    return await product_service.create(request_data, customer)


@router.put(
    '/products/{_id}',
    summary='Create a new product',
    status_code=HTTPStatus.CREATED,
    response_model=ProductSchema,
)
async def update_product(
        _id: int,
        request_data: CreateProductRequest,
        customer: 'Customer' = Depends(auth_admin),
        product_service: ProductService = Depends(get_product_service),
) -> ProductSchema:
    return await product_service.update_product(_id, request_data, customer)
