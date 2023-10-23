from http import HTTPStatus
from typing import TYPE_CHECKING

from db_models.factories import ShopFactory

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from shop_be.conf.settings import Settings
    from httpx import AsyncClient


async def test_get_shops(client: 'AsyncClient', db_session: 'AsyncSession', test_settings: 'Settings') -> None:
    """Test get shops endpoint"""
    count = 20
    ShopFactory.create_batch(count)
    await db_session.commit()

    response = await client.get('/shops')

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert tuple(response_data.keys()) == (
        'data', 'total', 'current_page', 'count', 'last_page', 'firstItem', 'lastItem', 'per_page', 'first_page_url',
        'last_page_url', 'next_page_url', 'prev_page_url',
    )
    assert len(response_data['data']) == 15
    assert response_data['total'] == count
    assert response_data['current_page'] == 1
    assert response_data['count'] == 15
    assert response_data['last_page'] == 2
    assert response_data['firstItem'] == 0
    assert response_data['lastItem'] == 14
    assert response_data['per_page'] == 15
    assert response_data['first_page_url'] == str(test_settings.WEB_URL) + 'api/shops?first=0&limit=15&page=1'
    assert response_data['last_page_url'] == str(test_settings.WEB_URL) + 'api/shops?first=0&limit=15&page=2'
    assert response_data['next_page_url'] == str(test_settings.WEB_URL) + 'api/shops?first=0&limit=15&page=2'
    assert response_data['prev_page_url'] == str(test_settings.WEB_URL) + 'api/shops?first=0&limit=15&page=1'

    shop = response_data['data'][0]
    assert tuple(shop.keys()) == (
        'id', 'owner_id', 'name', 'slug', 'description', 'is_active', 'cover_image', 'logo', 'address', 'settings',
        'created_at', 'updated_at', 'orders_count', 'products_count', 'owner',
    )
    assert tuple(shop['logo'].keys()) == ('id', 'original', 'thumbnail')
    assert tuple(shop['cover_image'].keys()) == ('id', 'original', 'thumbnail')
    assert tuple(shop['address'].keys()) == ('zip', 'city', 'state', 'country', 'street_address')
    assert tuple(shop['settings'].keys()) == ('contact', 'socials', 'website', 'location')
    assert tuple(shop['owner'].keys()) == (
        'id', 'name', 'email', 'email_verified_at', 'created_at', 'updated_at', 'is_active', 'shop_id', 'profile',
    )
    assert tuple(shop['owner']['profile'].keys()) == (
        'id', 'avatar', 'bio', 'socials', 'contact', 'customer_id', 'created_at', 'updated_at',
    )


async def test_get_shops_with_sorting(client: 'AsyncClient', db_session: 'AsyncSession') -> None:
    """Test get shops endpoint"""
    count = 20
    ShopFactory.create_batch(count)
    await db_session.commit()

    response = await client.get('/shops', params={'orderBy': 'id', 'sortedBy': 'desc'})

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert tuple(response_data.keys()) == (
        'data', 'total', 'current_page', 'count', 'last_page', 'firstItem', 'lastItem', 'per_page', 'first_page_url',
        'last_page_url', 'next_page_url', 'prev_page_url',
    )
    assert len(response_data['data']) == 15
    assert response_data['data'][0]['id'] == 96
    assert response_data['data'][-1]['id'] == 110


async def test_get_shops_with_search(client: 'AsyncClient', db_session: 'AsyncSession') -> None:
    """Test get shops endpoint"""
    count = 20
    shops = ShopFactory.create_batch(count)
    await db_session.commit()

    response = await client.get('/shops', params={'search': shops[0].name})

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert tuple(response_data.keys()) == (
        'data', 'total', 'current_page', 'count', 'last_page', 'firstItem', 'lastItem', 'per_page', 'first_page_url',
        'last_page_url', 'next_page_url', 'prev_page_url',
    )
    assert len(response_data['data']) == 1
    assert response_data['data'][0]['name'] == shops[0].name
