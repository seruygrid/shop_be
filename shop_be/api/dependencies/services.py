from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shop_be.api.dependencies.db import get_db_session
from shop_be.services.product_type import ProductTypeService


def get_product_type_service(session: AsyncSession = Depends(get_db_session)) -> 'ProductTypeService':
    """Get ProductTypeService instance"""
    return ProductTypeService(session)
