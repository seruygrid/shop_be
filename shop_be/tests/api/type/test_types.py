from http import HTTPStatus
from typing import TYPE_CHECKING

from db_models.factories import ProductTypeFactory

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from httpx import AsyncClient


async def test_get_types(client: 'AsyncClient', db_session: 'AsyncSession') -> None:
    """Test get types endpoint"""
    count = 20
    ProductTypeFactory.create_batch(count)
    await db_session.commit()

    response = await client.get('/types')

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert len(response_data) == count
    assert tuple(response_data[0].keys()) == (
        'id', 'name', 'settings', 'slug', 'language', 'icon', 'promotional_sliders', 'created_at', 'updated_at',
        'translated_languages', 'banners',
    )
