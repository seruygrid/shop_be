from http import HTTPStatus

from fastapi import APIRouter, Depends, UploadFile

from shop_be.api.dependencies.auth import auth_admin
from shop_be.api.dependencies.logger import LoggingRoute
from shop_be.api.dependencies.services import get_image_service
from shop_be.schemas.image import ImageSchema
from shop_be.services.image import ImageService

router = APIRouter(route_class=LoggingRoute)


@router.post(
    '/attachments',
    summary='Create new image',
    status_code=HTTPStatus.CREATED,
    response_model=list[ImageSchema],
    dependencies=[Depends(auth_admin)],
)
async def create_image(
        attachment: UploadFile,
        image_service: ImageService = Depends(get_image_service),
) -> list[ImageSchema]:
    return [await image_service.create_new(attachment)]
