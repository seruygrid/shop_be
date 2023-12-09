from fastapi import UploadFile

from db_models.db_models import Image
from shop_be.clients import aws_client
from shop_be.services.base import BaseService


class ImageService(BaseService[Image]):
    MODEL = Image

    async def create_new(self, file: UploadFile) -> 'Image':
        image_url = await aws_client.save_image(file)
        obj = self.MODEL(original=str(image_url), thumbnail=str(image_url))
        return await self.insert_obj(obj)
