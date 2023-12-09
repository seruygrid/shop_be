from typing import Sequence

from slugify import slugify
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count

from db_models.db_models import Shop, ShopSetting, Profile, Customer, Address, Location
from shop_be.conf.constants import ErrorMessages
from shop_be.exceptions import DoesNotExistException, ValidationException
from shop_be.schemas.shop.shop import ShopPaginationRequest, CreateShopSchema
from shop_be.services.base import BaseService


class ShopService(BaseService[Shop]):
    MODEL = Shop

    async def get_list(self, query_params: ShopPaginationRequest) -> Sequence['Shop']:
        query = query_params.filter_query(select(self.MODEL)).options(
            selectinload(self.MODEL.cover_image),
            selectinload(self.MODEL.logo),
            selectinload(self.MODEL.address),
            selectinload(self.MODEL.settings).selectinload(ShopSetting.location),
            selectinload(self.MODEL.owner).selectinload(Customer.profile).selectinload(Profile.avatar),
        ).limit(query_params.limit).offset(query_params.first)
        return await self.fetch_all(query)

    async def get_count(self, query_params: ShopPaginationRequest) -> int:
        query = query_params.filter_query(select(count(self.MODEL.id)))
        return await self.session.scalar(query)

    async def get_by_slug(self, slug: str) -> 'Shop':
        options = (
            selectinload(self.MODEL.cover_image),
            selectinload(self.MODEL.logo),
            selectinload(self.MODEL.address),
            selectinload(self.MODEL.settings).selectinload(ShopSetting.location),
            selectinload(self.MODEL.owner).selectinload(Customer.profile).selectinload(Profile.avatar),
        )
        if obj := await self.fetch_one(filters=(self.MODEL.slug == slug,), options=options):
            return obj
        raise DoesNotExistException(ErrorMessages.SHOP_DOES_NOT_EXIST)

    async def validate_slug(self, slug: str) -> None:
        if await self.exist(filters=(self.MODEL.slug == slug,)):
            raise ValidationException(ErrorMessages.SHOP_SLUG_ALREADY_EXIST)

    async def create(self, data: CreateShopSchema, customer: 'Customer') -> 'Shop':
        shop_slug = slugify(data.name)
        await self.validate_slug(shop_slug)

        address = Address(**data.address.model_dump())
        await self.insert_obj(address, commit=False)
        if data.settings.location:
            location = Location(**data.settings.location)
            await self.insert_obj(location, commit=False)
            settings = ShopSetting(
                contact=data.settings.contact,
                socials=data.settings.socials,
                website=data.settings.website,
                location_id=location.id,
            )
            await self.insert_obj(settings, commit=False)

        shop = self.MODEL(
            name=data.name,
            slug=shop_slug,
            description=data.description,
            logo_id=data.logo.id,
            cover_image_id=data.cover_image.id,
            owner_id=customer.id,
            address_id=address.id,
        )
        await self.insert_obj(shop, commit=True)
        return await self.get_by_slug(shop_slug)

    async def update_shop(self, _id: int, data: CreateShopSchema) -> 'Shop':
        slug = slugify(data.name)
        shop = await self.fetch_one(
            filters=(self.MODEL.id == _id),
            options=(
                selectinload(self.MODEL.cover_image),
                selectinload(self.MODEL.logo),
                selectinload(self.MODEL.address),
                selectinload(self.MODEL.settings).selectinload(ShopSetting.location),
            ))

        if shop.slug != slug:
            await self.validate_slug(slug)
            shop.slug = slug

        shop.name = data.name
        shop.description = data.description
        await self.update_obj(shop.address, values=data.address.model_dump())
        await self.update_obj(shop.cover_image, values=data.cover_image.model_dump())
        await self.update_obj(shop.settings, values=data.settings.model_dump())
        await self.update_obj(shop.settings.location, values=data.settings.location.model_dump())
        return await self.get_by_slug(slug)

    async def change_shop_status(self, _id: int, value: bool) -> None:
        await self.update(filters=(self.MODEL.id == _id, ), values={'is_active': value})
        await self.session.commit()
