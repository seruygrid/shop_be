from http import HTTPStatus
from typing import TYPE_CHECKING

from db_models.factories import ChildCategoryFactory

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from shop_be.conf.settings import Settings
    from httpx import AsyncClient


async def test_get_categories(client: 'AsyncClient', db_session: 'AsyncSession', test_settings: 'Settings') -> None:
    """Test get categories endpoint"""
    count = 50
    ChildCategoryFactory.create_batch(count)
    await db_session.commit()
    response = await client.get('/categories')
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
    assert response_data['last_page'] == 4
    assert response_data['firstItem'] == 0
    assert response_data['lastItem'] == 14
    assert response_data['per_page'] == 15
    assert response_data['first_page_url'] == str(test_settings.WEB_URL) + 'api/categories?first=0&limit=15&page=1'
    assert response_data['last_page_url'] == str(test_settings.WEB_URL) + 'api/categories?first=0&limit=15&page=4'
    assert response_data['next_page_url'] == str(test_settings.WEB_URL) + 'api/categories?first=0&limit=15&page=2'
    assert response_data['prev_page_url'] == str(test_settings.WEB_URL) + 'api/categories?first=0&limit=15&page=1'

    category = response_data['data'][0]
    assert tuple(category.keys()) == (
        'id', 'name', 'slug', 'icon', 'image', 'details', 'language', 'translated_languages', 'type_id', 'created_at',
        'updated_at', 'deleted_at', 'parent_id', 'parent', 'type', 'children', 'products_count',
    )
    assert tuple(category['type'].keys()) == (
        'id', 'name', 'language', 'translated_languages', 'settings', 'slug', 'icon', 'promotional_sliders',
        'created_at', 'updated_at'
    )
    assert len(category['children']) == 1
    assert tuple(category['children'][0].keys()) == (
        'id', 'name', 'slug', 'icon', 'image', 'details', 'language', 'translated_languages', 'type_id', 'created_at',
        'updated_at', 'deleted_at', 'parent_id', 'parent', 'products_count', 'children',
    )


async def test_get_categories_with_sorting(client: 'AsyncClient', db_session: 'AsyncSession') -> None:
    """Test get categories endpoint"""
    count = 50
    ChildCategoryFactory.create_batch(count)
    await db_session.commit()
    response = await client.get('/categories', params={'orderBy': 'id', 'sortedBy': 'desc'})
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert tuple(response_data.keys()) == (
        'data', 'total', 'current_page', 'count', 'last_page', 'firstItem', 'lastItem', 'per_page', 'first_page_url',
        'last_page_url', 'next_page_url', 'prev_page_url',
    )
    assert len(response_data['data']) == 15
    assert response_data['data'][0]['id'] == 99
    assert response_data['data'][-1]['id'] == 85


async def test_get_categories_with_search(client: 'AsyncClient', db_session: 'AsyncSession') -> None:
    """Test get categories endpoint"""
    count = 10
    child = ChildCategoryFactory.create_batch(count)
    await db_session.commit()
    response = await client.get('/categories', params={'search': child[0].parent.name})
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert tuple(response_data.keys()) == (
        'data', 'total', 'current_page', 'count', 'last_page', 'firstItem', 'lastItem', 'per_page', 'first_page_url',
        'last_page_url', 'next_page_url', 'prev_page_url',
    )
    assert len(response_data['data']) == 1
    assert response_data['data'][0]['name'] == child[0].parent.name


async def test_get_categories_with_language(client: 'AsyncClient', db_session: 'AsyncSession') -> None:
    """Test get categories endpoint"""
    count = 10
    child = ChildCategoryFactory.create_batch(count)
    await db_session.commit()
    response = await client.get('/categories', params={'language': child[0].parent.language})
    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert tuple(response_data.keys()) == (
        'data', 'total', 'current_page', 'count', 'last_page', 'firstItem', 'lastItem', 'per_page', 'first_page_url',
        'last_page_url', 'next_page_url', 'prev_page_url',
    )
    assert len(response_data['data']) == count
    assert response_data['data'][0]['language'] == child[0].parent.language
