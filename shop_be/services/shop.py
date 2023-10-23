from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.functions import count

from db_models.db_models import Shop, ShopSetting, ShopOwner, OwnerProfile
from shop_be.conf.constants import ErrorMessages
from shop_be.exceptions import DoesNotExistException
from shop_be.schemas.shop.shop import ShopPaginationRequest
from shop_be.services.base import BaseService


class ShopService(BaseService[Shop]):
    MODEL = Shop

    async def get_list(self, query_params: ShopPaginationRequest) -> list['Shop']:
        query = query_params.filter_query(select(self.MODEL)).options(
            selectinload(self.MODEL.cover_image),
            selectinload(self.MODEL.logo),
            selectinload(self.MODEL.address),
            selectinload(self.MODEL.settings).selectinload(ShopSetting.location),
            selectinload(self.MODEL.owner).selectinload(ShopOwner.profile).selectinload(OwnerProfile.avatar),
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
            selectinload(self.MODEL.owner).selectinload(ShopOwner.profile).selectinload(OwnerProfile.avatar),
        )
        if obj := await self.fetch_one(filters=(self.MODEL.slug == slug,), options=options):
            return obj
        raise DoesNotExistException(ErrorMessages.SHOP_DOES_NOT_EXIST)
