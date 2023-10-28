from http import HTTPStatus

from fastapi import APIRouter, Depends

from db_models.db_models import Order
from shop_be.api.dependencies.services import get_order_service, get_product_service
from shop_be.schemas.order.order import OrderVerifyRequest, OrderVerifyResponse, CreateOrderRequest, OrderInfo
from shop_be.services.order import OrderService
from shop_be.services.product import ProductService

router = APIRouter()


@router.post(
    '/orders',
    summary='Create new order',
    response_model=OrderInfo,
)
async def create_new_order(
        request_data: CreateOrderRequest,
        order_service: OrderService = Depends(get_order_service),
        product_service: ProductService = Depends(get_product_service),
) -> Order:
    """Create new order"""
    products = await product_service.get_for_order(request_data.products)
    return await order_service.create(request_data, products)


@router.get(
    '/orders/<order_id>',
    summary='Get order info',
    response_model=OrderInfo,
)
async def get_order(
        order_id: str,
        order_service: OrderService = Depends(get_order_service),
) -> Order:
    """Get order info"""
    return await order_service.get_by_tracking_id(order_id)


@router.post(
    '/orders/checkout/verify',
    summary='Verify order',
    status_code=HTTPStatus.OK,
    response_model=OrderVerifyResponse,
)
async def verify_order(_: OrderVerifyRequest) -> OrderVerifyResponse:
    """Check if order is valid"""
    return OrderVerifyResponse()
