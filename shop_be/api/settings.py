import json
from http import HTTPStatus

from fastapi import APIRouter

router = APIRouter()


@router.get(
    '/settings',
    summary='Get general settings',
    status_code=HTTPStatus.OK,
    response_model=dict,
)
async def get_settings() -> dict:
    with open('shop_be/api/mocks/settings.json', 'r') as settings_file:
        settings = json.loads(settings_file.read())
    return settings
