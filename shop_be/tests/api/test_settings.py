from http import HTTPStatus
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from httpx import AsyncClient


async def test_get_categories(client: 'AsyncClient') -> None:
    """Test get categories endpoint"""
    response = await client.get('/settings')

    assert response.status_code == HTTPStatus.OK
    response_data = response.json()
    assert tuple(response_data.keys()) == ('id', 'options', 'language', 'created_at', 'updated_at')
    assert tuple(response_data['options'].keys()) == (
        'seo', 'logo', 'useAi', 'currency', 'smsEvent', 'taxClass', 'dark_logo', 'defaultAi', 'siteTitle', 'emailEvent',
        'server_info', 'signupPoints', 'siteSubtitle', 'useGoogleMap', 'StripeCardOnly', 'contactDetails',
        'paymentGateway', 'currencyOptions', 'isProductReview', 'useEnableGateway', 'minimumOrderAmount',
        'maximumQuestionLimit', 'currencyToWalletRatio', 'defaultPaymentGateway',
    )
