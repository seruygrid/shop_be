from http import HTTPStatus
from typing import TYPE_CHECKING

from db_models.factories import ProductFactory, RatingFactory, CategoryFactory

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from shop_be.conf.settings import Settings
    from httpx import AsyncClient


async def test_get_products(client: 'AsyncClient', db_session: 'AsyncSession', test_settings: 'Settings') -> None:
    """Test get products endpoint"""
    count = 20
    category = CategoryFactory()
    products = ProductFactory.create_batch(count, categories=[category])
    for product in products:
        RatingFactory(product=product)
    await db_session.commit()

    response = await client.get('/products')

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
    assert response_data['first_page_url'] == str(test_settings.WEB_URL) + 'api/products?first=0&limit=15&page=1'
    assert response_data['last_page_url'] == str(test_settings.WEB_URL) + 'api/products?first=0&limit=15&page=2'
    assert response_data['next_page_url'] == str(test_settings.WEB_URL) + 'api/products?first=0&limit=15&page=2'
    assert response_data['prev_page_url'] == str(test_settings.WEB_URL) + 'api/products?first=0&limit=15&page=1'

    product = response_data['data'][0]
    assert tuple(product.keys()) == (
        'id', 'name', 'slug', 'description', 'type_id', 'price', 'shop_id', 'sale_price', 'language', 'min_price',
        'max_price', 'sku', 'quantity', 'in_stock', 'is_taxable', 'shipping_class_id', 'status', 'product_type', 'unit',
        'height', 'width', 'length', 'image', 'video', 'gallery', 'deleted_at', 'created_at', 'updated_at', 'author_id',
        'manufacturer_id', 'is_digital', 'is_external', 'external_product_url', 'external_product_button_text',
        'ratings', 'total_reviews', 'rating_count', 'my_review', 'in_wishlist', 'blocked_dates', 'translated_languages',
        'categories', 'shop', 'type', 'variations', 'metas', 'manufacturer', 'variation_options', 'tags',
    )
    assert tuple(product['rating_count'][0].keys()) == (
        'rating', 'total', 'positive_feedbacks_count', 'negative_feedbacks_count', 'my_feedback',
        'abusive_reports_count',
    )
    assert tuple(product['categories'][0].keys()) == (
        'id', 'name', 'slug', 'icon', 'image', 'details', 'language', 'translated_languages', 'type_id', 'created_at',
        'updated_at', 'deleted_at', 'parent_id',
    )
    assert tuple(product['shop'].keys()) == (
        'id', 'owner_id', 'name', 'slug', 'description', 'is_active', 'cover_image', 'logo', 'address', 'settings',
        'created_at', 'updated_at',
    )
    assert tuple(product['type'].keys()) == (
        'id', 'name', 'settings', 'slug', 'language', 'icon', 'promotional_sliders', 'created_at', 'updated_at',
        'translated_languages',
    )


async def test_get_product_with_sorting(client: 'AsyncClient', db_session: 'AsyncSession') -> None:
    """Test get products endpoint"""
    count = 20
    category = CategoryFactory()
    products = ProductFactory.create_batch(count, categories=[category])
    for product in products:
        RatingFactory(product=product)
    await db_session.commit()

    response = await client.get('/products', params={'orderBy': 'id', 'sortedBy': 'desc'})

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert tuple(response_data.keys()) == (
        'data', 'total', 'current_page', 'count', 'last_page', 'firstItem', 'lastItem', 'per_page', 'first_page_url',
        'last_page_url', 'next_page_url', 'prev_page_url',
    )
    assert len(response_data['data']) == 15
    assert response_data['data'][0]['id'] == 39
    assert response_data['data'][-1]['id'] == 25


async def test_get_products_with_search(client: 'AsyncClient', db_session: 'AsyncSession') -> None:
    """Test get products endpoint"""
    count = 20
    category = CategoryFactory()
    products = ProductFactory.create_batch(count, categories=[category])
    for product in products:
        RatingFactory(product=product)
    await db_session.commit()

    response = await client.get('/products', params={'search': products[0].name})

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert tuple(response_data.keys()) == (
        'data', 'total', 'current_page', 'count', 'last_page', 'firstItem', 'lastItem', 'per_page', 'first_page_url',
        'last_page_url', 'next_page_url', 'prev_page_url',
    )
    assert len(response_data['data']) == 1
    assert response_data['data'][0]['name'] == products[0].name


async def test_get_products_with_language(client: 'AsyncClient', db_session: 'AsyncSession') -> None:
    """Test get products endpoint"""
    count = 15
    category = CategoryFactory()
    products = ProductFactory.create_batch(count, categories=[category], language='en')
    for product in products:
        RatingFactory(product=product)
    await db_session.commit()

    response = await client.get('/products', params={'language': products[0].language})

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert tuple(response_data.keys()) == (
        'data', 'total', 'current_page', 'count', 'last_page', 'firstItem', 'lastItem', 'per_page', 'first_page_url',
        'last_page_url', 'next_page_url', 'prev_page_url',
    )
    assert len(response_data['data']) == count
    assert response_data['data'][0]['language'] == products[0].language
