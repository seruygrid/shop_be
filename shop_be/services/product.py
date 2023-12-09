from http import HTTPStatus
from typing import Sequence

from fastapi import HTTPException
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count

from db_models.db_models import Product, Shop, ShopSetting, Customer
from shop_be.conf.constants import ErrorMessages
from shop_be.exceptions import DoesNotExistException, ValidationException
from shop_be.schemas.order.order import ProductItem
from shop_be.schemas.shop.product import ProductPaginationRequest, CreateProductRequest
from shop_be.services.base import BaseService


class ProductService(BaseService[Product]):
    MODEL = Product

    async def get_list(self, query_params: ProductPaginationRequest) -> Sequence['Product']:
        query = query_params.filter_query(select(self.MODEL)).options(
            selectinload(self.MODEL.shop).selectinload(Shop.cover_image),
            selectinload(self.MODEL.shop).selectinload(Shop.logo),
            selectinload(self.MODEL.shop).selectinload(Shop.address),
            selectinload(self.MODEL.gallery),
            selectinload(self.MODEL.rating_count),
            selectinload(self.MODEL.categories),
            selectinload(self.MODEL.image),
        ).limit(query_params.limit).offset(query_params.first)
        return await self.fetch_all(query)

    async def get_count(self, query_params: ProductPaginationRequest) -> int:
        query = query_params.filter_query(select(count(self.MODEL.id)))
        return await self.session.scalar(query) or 0

    async def get_by_slug(self, slug: str) -> 'Product':
        options = (
            selectinload(self.MODEL.shop).selectinload(Shop.cover_image),
            selectinload(self.MODEL.shop).selectinload(Shop.logo),
            selectinload(self.MODEL.shop).selectinload(Shop.address),
            selectinload(self.MODEL.shop).selectinload(Shop.settings).selectinload(ShopSetting.location),
            selectinload(self.MODEL.gallery),
            selectinload(self.MODEL.rating_count),
            selectinload(self.MODEL.categories),
            selectinload(self.MODEL.image),
        )
        if obj := await self.fetch_one(filters=(self.MODEL.slug == slug,), options=options):
            return obj
        raise DoesNotExistException(ErrorMessages.PRODUCT_DOES_NOT_EXIST)

    async def get_for_order(self, products: list[ProductItem]) -> Sequence[Product]:
        ids = [product.id for product in products]
        query = select(self.MODEL).where(self.MODEL.id.in_(ids))
        return await self.fetch_all(query)

    async def validate_slug(self, slug: str) -> None:
        if await self.exist(filters=(self.MODEL.slug == slug,)):
            raise ValidationException(ErrorMessages.PRODUCT_SLUG_ALREADY_EXIST)

    async def create(self, data: CreateProductRequest, customer: 'Customer') -> 'Product':
        slug = slugify(data.name)
        await self.validate_slug(slug)

        obj = self.MODEL(
            name=data.name,
            slug=slug,
            description=data.description,
            language=data.language,
            price=data.price,
            min_price=data.min_price,
            max_price=data.max_price,
            status=data.status,
            unit=data.unit,
            image_id=data.image.id,
            shop_id=data.shop_id,
        )
        await self.insert_obj(obj)
        return await self.get_by_slug(slug)

    async def update_product(self, _id: int, data: CreateProductRequest, customer: 'Customer') -> 'Product':
        product = await self.fetch_one(filters=(self.MODEL.id == _id,))

        if product.author_id != customer.id:
            raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=ErrorMessages.PRODUCT_PERMISSION_NOT_FOUND)

        slug = product.slug
        if data.name != product.name:
            slug = slugify(data.name)
            await self.validate_slug(slug)

        await self.update_obj(product, values={'slug': slug, **data.model_dump()})
        return await self.get_by_slug(slug)
