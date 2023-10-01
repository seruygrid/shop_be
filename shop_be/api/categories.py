import json
from http import HTTPStatus

from fastapi import APIRouter

from shop_be.api.dependencies.paginate import paginate

router = APIRouter()


@router.get(
    '/categories',
    summary='Get shop types',
    status_code=HTTPStatus.OK,
    response_model=dict,
)
async def get_types() -> dict:
    with open('shop_be/api/mocks/categories.json', 'r') as settings_file:
        settings = json.loads(settings_file.read())
    return paginate(settings)
