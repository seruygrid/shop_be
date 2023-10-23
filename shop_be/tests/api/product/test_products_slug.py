from http import HTTPStatus
from typing import TYPE_CHECKING

from db_models.factories import ProductFactory, RatingFactory, CategoryFactory
from shop_be.conf.constants import ErrorMessages

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from httpx import AsyncClient


async def test_get_product_by_slug(client: 'AsyncClient', db_session: 'AsyncSession') -> None:
    """Test get products endpoint"""
    category = CategoryFactory()
    product = ProductFactory(categories=[category])
    RatingFactory(product=product)
    await db_session.commit()

    response = await client.get(f'/products/{product.slug}')

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert tuple(response_data.keys()) == (
        'id', 'name', 'slug', 'description', 'type_id', 'price', 'shop_id', 'sale_price', 'language', 'min_price',
        'max_price', 'sku', 'quantity', 'in_stock', 'is_taxable', 'shipping_class_id', 'status', 'product_type', 'unit',
        'height', 'width', 'length', 'image', 'video', 'gallery', 'deleted_at', 'created_at', 'updated_at', 'author_id',
        'manufacturer_id', 'is_digital', 'is_external', 'external_product_url', 'external_product_button_text',
        'ratings', 'total_reviews', 'rating_count', 'my_review', 'in_wishlist', 'blocked_dates', 'translated_languages',
        'categories', 'shop', 'type', 'variations', 'metas', 'manufacturer', 'variation_options', 'tags',
    )
    assert tuple(response_data['rating_count'][0].keys()) == (
        'rating', 'total', 'positive_feedbacks_count', 'negative_feedbacks_count', 'my_feedback',
        'abusive_reports_count',
    )
    assert tuple(response_data['categories'][0].keys()) == (
        'id', 'name', 'slug', 'icon', 'image', 'details', 'language', 'translated_languages', 'type_id', 'created_at',
        'updated_at', 'deleted_at', 'parent_id',
    )
    assert tuple(response_data['shop'].keys()) == (
        'id', 'owner_id', 'name', 'slug', 'description', 'is_active', 'cover_image', 'logo', 'address', 'settings',
        'created_at', 'updated_at',
    )
    assert tuple(response_data['type'].keys()) == (
        'id', 'name', 'settings', 'slug', 'language', 'icon', 'promotional_sliders', 'created_at', 'updated_at',
        'translated_languages',
    )


async def test_get_product_by_slug_not_exist(client: 'AsyncClient') -> None:
    """Test get products endpoint"""
    response = await client.get('/products/not_exist')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': ErrorMessages.PRODUCT_DOES_NOT_EXIST}
