import json
from http import HTTPStatus

from fastapi import APIRouter

router = APIRouter()


@router.get(
    '/types',
    summary='Get shop types',
    status_code=HTTPStatus.OK,
    response_model=list,
)
async def get_types() -> dict:
    with open('shop_be/api/mocks/types.json', 'r') as settings_file:
        settings = json.loads(settings_file.read())
    return settings


@router.get(
    '/types/{slug}',
    summary='Get shop types',
    status_code=HTTPStatus.OK,
    response_model=dict,
)
async def get_type_by_slug(slug: str) -> dict:
    with open('shop_be/api/mocks/types.json', 'r') as settings_file:
        settings = json.loads(settings_file.read())
    return settings[0]
