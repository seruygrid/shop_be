import json
from http import HTTPStatus

from fastapi import APIRouter

from shop_be.api.dependencies.paginate import paginate

router = APIRouter()


@router.get(
    '/products',
    summary='Get shop types',
    status_code=HTTPStatus.OK,
    response_model=dict,
)
async def get_products() -> dict:
    with open('shop_be/api/mocks/products.json', 'r') as settings_file:
        settings = json.loads(settings_file.read())
    return paginate(settings)


@router.get(
    '/products/{slug}',
    summary='Get shop types',
    status_code=HTTPStatus.OK,
    response_model=dict,
)
async def get_product(slug: str) -> dict:
    with open('shop_be/api/mocks/products.json', 'r') as settings_file:
        settings = json.loads(settings_file.read())
    return settings[0]
