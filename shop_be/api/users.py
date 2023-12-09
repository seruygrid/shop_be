from http import HTTPStatus

from fastapi import APIRouter, Depends

from db_models.db_models import Customer
from shop_be.api.dependencies.auth import auth_customer
from shop_be.api.dependencies.logger import LoggingRoute
from shop_be.api.dependencies.services import get_customer_service
from shop_be.schemas.customer.customer import CreateCustomerResponse
from shop_be.services.customer import CustomerService

router = APIRouter(route_class=LoggingRoute)


@router.get(
    '/me',
    summary='Get current user info',
    status_code=HTTPStatus.OK,
    response_model=CreateCustomerResponse,
)
async def create_customer(
        customer: 'Customer' = Depends(auth_customer),
        customer_service: CustomerService = Depends(get_customer_service),
) -> 'Customer':
    return await customer_service.get_customer_info(customer)
