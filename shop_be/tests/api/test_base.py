from http import HTTPStatus
from typing import TYPE_CHECKING

from shop_be import __version__

if TYPE_CHECKING:
    from httpx import AsyncClient


async def test_health_ok(client: 'AsyncClient') -> None:
    """Test health check endpoint"""
    response = await client.get('/health')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'db': True}


async def test_version(client: 'AsyncClient') -> None:
    """Test version endpoint"""
    response = await client.get('/version')
    assert response.status_code == HTTPStatus.OK
    assert response.json()['version'] == __version__
