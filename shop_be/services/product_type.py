from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db_models.db_models import ProductType, Banner
from shop_be.exceptions import DoesNotExistException
from shop_be.services.base import BaseService


class ProductTypeService(BaseService[ProductType]):
    MODEL = ProductType

    async def get_list(self) -> list[ProductType]:
        query = select(self.MODEL).options(selectinload(self.MODEL.banners).selectinload(Banner.image), )
        return await self.fetch_all(query)

    async def get_by_slug(self, slug: str) -> ProductType:
        options = (selectinload(self.MODEL.banners).selectinload(Banner.image),)
        obj = await self.fetch_one(filters=(self.MODEL.slug == slug,), options=options)
        if not obj:
            raise DoesNotExistException('Product type does not exist.')
        return obj
