from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from shop_be.api.dependencies.db import get_db_session
from shop_be.services.category import CategoryService
from shop_be.services.product import ProductService
from shop_be.services.product_type import ProductTypeService
from shop_be.services.shop import ShopService


def get_product_type_service(session: AsyncSession = Depends(get_db_session)) -> 'ProductTypeService':
    """Get ProductTypeService instance"""
    return ProductTypeService(session)


def get_product_service(session: AsyncSession = Depends(get_db_session)) -> 'ProductService':
    """Get ProductService instance"""
    return ProductService(session)


def get_category_service(session: AsyncSession = Depends(get_db_session)) -> 'CategoryService':
    """Get CategoryService instance"""
    return CategoryService(session)


def get_shop_service(session: AsyncSession = Depends(get_db_session)) -> 'ShopService':
    """Get ShopService instance"""
    return ShopService(session)
