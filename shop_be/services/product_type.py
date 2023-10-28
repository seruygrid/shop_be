from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db_models.db_models import Type, Banner
from shop_be.conf.constants import ErrorMessages
from shop_be.exceptions import DoesNotExistException
from shop_be.services.base import BaseService


class TypeService(BaseService[Type]):
    MODEL = Type

    async def get_list(self) -> list[Type]:
        query = select(self.MODEL).options(
            selectinload(self.MODEL.banners).selectinload(Banner.image),
            selectinload(self.MODEL.promotional_sliders),
        )
        return await self.fetch_all(query)

    async def get_by_slug(self, slug: str) -> Type:
        options = (
            selectinload(self.MODEL.banners).selectinload(Banner.image),
            selectinload(self.MODEL.promotional_sliders),
        )
        obj = await self.fetch_one(filters=(self.MODEL.slug == slug,), options=options)
        if not obj:
            raise DoesNotExistException(ErrorMessages.PRODUCT_TYPE_DOES_NOT_EXIST)
        return obj
