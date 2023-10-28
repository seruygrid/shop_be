from http import HTTPStatus

from fastapi import APIRouter, Depends

from shop_be.api.dependencies.services import get_type_service
from shop_be.schemas.category.types import ProductTypeSchema
from shop_be.services.product_type import TypeService

router = APIRouter()


@router.get(
    '/types',
    summary='Get category types',
    status_code=HTTPStatus.OK,
    response_model=list[ProductTypeSchema],
)
async def get_types(
        type_service: TypeService = Depends(get_type_service),
) -> list[ProductTypeSchema]:
    return await type_service.get_list()


@router.get(
    '/types/{slug}',
    summary='Get category types by slug',
    status_code=HTTPStatus.OK,
    response_model=ProductTypeSchema,
)
async def get_type_by_slug(
        slug: str,
        type_service: TypeService = Depends(get_type_service),
) -> ProductTypeSchema:
    return await type_service.get_by_slug(slug)
