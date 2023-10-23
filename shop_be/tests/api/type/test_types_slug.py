from http import HTTPStatus
from typing import TYPE_CHECKING

from db_models.factories import ProductTypeFactory
from shop_be.conf.constants import ErrorMessages

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from httpx import AsyncClient


async def test_get_types_by_slug(client: 'AsyncClient', db_session: 'AsyncSession') -> None:
    """Test get type endpoint"""
    my_type = ProductTypeFactory()
    await db_session.commit()

    response = await client.get(f'/types/{my_type.slug}')

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert tuple(response_data.keys()) == (
        'id', 'name', 'settings', 'slug', 'language', 'icon', 'promotional_sliders', 'created_at', 'updated_at',
        'translated_languages', 'banners',
    )


async def test_get_type_by_slug_not_exist(client: 'AsyncClient') -> None:
    """Test get types endpoint"""
    response = await client.get('/types/not_exist')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': ErrorMessages.PRODUCT_TYPE_DOES_NOT_EXIST}
