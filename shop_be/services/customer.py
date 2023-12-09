from datetime import datetime

from sqlalchemy.orm import selectinload

from db_models.db_models import Customer, CustomerAddress
from shop_be.clients import aws_client
from shop_be.services.base import BaseService
from shop_be.services.permission import PermissionService


class CustomerService(BaseService[Customer]):
    MODEL = Customer

    async def get_customer_by_cognito_sub(self, sub: str) -> 'Customer':
        return await self.fetch_one(filters=(self.MODEL.sub == sub,), options=(selectinload(self.MODEL.permissions),))

    async def create_customer_by_cognito(self, username: str, groups: list[str]) -> 'Customer':
        cognito_user = await aws_client.cognito_get_user(username)
        customer = self.MODEL(
            name=cognito_user.email,
            sub=cognito_user.sub,
            email=cognito_user.email,
            email_verified_at=datetime.now(),
            is_active=True,
        )
        permission_service = PermissionService(self.session)
        permissions = await permission_service.get_or_create(groups)
        for permission in permissions:
            customer.permissions.append(permission)
        return await self.insert_obj(customer)

    async def get_customer_info(self, customer: 'Customer') -> 'Customer':
        options = (
            selectinload(self.MODEL.profile),
            selectinload(self.MODEL.address).selectinload(CustomerAddress.address),
            selectinload(self.MODEL.permissions),
        )
        return await self.fetch_one(filters=(self.MODEL.id == customer.id,), options=options)
