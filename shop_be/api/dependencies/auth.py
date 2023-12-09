import logging
from http import HTTPStatus
from typing import Dict, Any, Optional

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from db_models.db_models import Customer
from shop_be.api.dependencies.services import get_customer_service
from shop_be.conf.constants import JWK_URL, JWT_ACCESS_TOKEN_ALGORITHMS, AWS_COGNITO_URL
from shop_be.services.customer import CustomerService

logger = logging.getLogger(__name__)

oauth2_scheme = HTTPBearer()
jwk_client = jwt.PyJWKClient(JWK_URL, cache_keys=True)
unauthorized_exc = HTTPException(
    status_code=HTTPStatus.UNAUTHORIZED,
    detail='Invalid authentication credentials',
    headers={'WWW-Authenticate': 'Bearer'},
)


def get_access_token(authorization: Optional[HTTPAuthorizationCredentials] = Depends(oauth2_scheme)) -> str:
    if not authorization:
        raise unauthorized_exc
    return authorization.credentials


def get_jwk_key(token: str = Depends(get_access_token)) -> jwt.PyJWK:
    try:
        return jwk_client.get_signing_key_from_jwt(token)
    except jwt.PyJWTError:
        raise unauthorized_exc


def validate_access_token(
        token: str = Depends(get_access_token),
        jwk_key: jwt.PyJWK = Depends(get_jwk_key),
) -> Dict[str, Any]:
    try:
        token_data = jwt.decode(
            token,
            jwk_key.key,
            algorithms=JWT_ACCESS_TOKEN_ALGORITHMS,
            options={
                'verify_signature': True,
                'verify_exp': True,
                'require': ['sub', 'exp', 'iss', 'token_use'],
            }
        )
        if token_data.get('iss') != AWS_COGNITO_URL:
            logger.warning('Invalid "iss" claim')
            raise unauthorized_exc
        if token_data.get('token_use') != 'access':
            logger.warning('Invalid "token_use" claim')
            raise unauthorized_exc

    except jwt.InvalidTokenError as err:
        logger.warning(err)
        raise unauthorized_exc

    else:
        return token_data


async def auth_customer(
        token_payload: Dict[str, Any] = Depends(validate_access_token),
        user_service: CustomerService = Depends(get_customer_service),
) -> 'Customer':
    sub = token_payload['sub']

    if user := await user_service.get_customer_by_cognito_sub(sub):
        return user

    return await user_service.create_customer_by_cognito(
        token_payload['username'],
        token_payload['cognito:groups'],
    )


async def auth_admin(
        token_payload: Dict[str, Any] = Depends(validate_access_token),
        user_service: CustomerService = Depends(get_customer_service),
) -> 'Customer':
    sub = token_payload['sub']
    customer = await user_service.get_customer_by_cognito_sub(sub)

    if not customer:
        customer = await user_service.create_customer_by_cognito(
            token_payload['username'],
            token_payload['cognito:groups'],
        )

    if 'SUPER_ADMIN' in token_payload['cognito:groups']:
        return customer

    raise HTTPException(
        status_code=HTTPStatus.FORBIDDEN,
        detail='Invalid authentication credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
