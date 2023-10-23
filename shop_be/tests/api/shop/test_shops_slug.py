from http import HTTPStatus
from typing import TYPE_CHECKING

from db_models.factories import ShopFactory
from shop_be.conf.constants import ErrorMessages

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from httpx import AsyncClient


async def test_get_shop_by_slug(client: 'AsyncClient', db_session: 'AsyncSession') -> None:
    """Test get shops endpoint"""
    shop = ShopFactory()
    await db_session.commit()

    response = await client.get(f'/shops/{shop.slug}')

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert tuple(response_data.keys()) == (
        'id', 'owner_id', 'name', 'slug', 'description', 'is_active', 'cover_image', 'logo', 'address', 'settings',
        'created_at', 'updated_at', 'orders_count', 'products_count', 'owner',
    )
    assert tuple(response_data['logo'].keys()) == ('id', 'original', 'thumbnail')
    assert tuple(response_data['cover_image'].keys()) == ('id', 'original', 'thumbnail')
    assert tuple(response_data['address'].keys()) == ('zip', 'city', 'state', 'country', 'street_address')
    assert tuple(response_data['settings'].keys()) == ('contact', 'socials', 'website', 'location')
    assert tuple(response_data['owner'].keys()) == (
        'id', 'name', 'email', 'email_verified_at', 'created_at', 'updated_at', 'is_active', 'shop_id', 'profile',
    )
    assert tuple(response_data['owner']['profile'].keys()) == (
        'id', 'avatar', 'bio', 'socials', 'contact', 'customer_id', 'created_at', 'updated_at',
    )


async def test_get_shop_by_slug_not_exist(client: 'AsyncClient') -> None:
    """Test get shops endpoint"""
    response = await client.get('/shops/not_exist')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': ErrorMessages.SHOP_DOES_NOT_EXIST}
