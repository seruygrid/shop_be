from shop_be.conf.settings import settings

JWT_ALGORITHM = 'HS256'

BASE_HTTP_CLIENT_TIMEOUT = 2.0
JWT_ACCESS_TOKEN_ALGORITHMS = ['RS256']
AWS_COGNITO_URL = f'https://cognito-idp.{settings.AWS_DEFAULT_REGION}.amazonaws.com/{settings.COGNITO_POOL_ID}'
JWK_URL = '/'.join([AWS_COGNITO_URL.rstrip('/'), '.well-known/jwks.json'])


class ErrorMessages:
    SHOP_DOES_NOT_EXIST = 'Shop does not exist.'
    ORDER_DOES_NOT_EXIST = 'Order does not exist.'
    PRODUCT_DOES_NOT_EXIST = 'Product does not exist.'
    SHOP_SLUG_ALREADY_EXIST = 'Shop slug already exist.'
    PRODUCT_SLUG_ALREADY_EXIST = 'Product slug already exist.'
    PRODUCT_TYPE_DOES_NOT_EXIST = 'Product type does not exist.'
    PRODUCT_PERMISSION_NOT_FOUND = 'Product permission not found.'
