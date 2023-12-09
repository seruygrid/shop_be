import logging
from typing import Type, Optional
from urllib.parse import urljoin

import httpx

from shop_be.conf.constants import BASE_HTTP_CLIENT_TIMEOUT
from shop_be.exceptions import HTTPClientException

logger = logging.getLogger(__name__)


class BaseHTTPClient:
    """Base HTTP client"""
    EXC_CLASS: Type[HTTPClientException]

    def __init__(self, base_url: str, timeout: float = BASE_HTTP_CLIENT_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout

    def get_url(self, url: str) -> str:
        """Build the url for request"""
        return urljoin(self.base_url, url)

    async def get(
            self,
            url: str,
            user_id: Optional[int] = None,
            **kwargs,
    ) -> httpx.Response:
        """Make GET request"""
        return await self._request('GET', url, user_id=user_id, **kwargs)

    async def post(
            self,
            url: str,
            user_id: Optional[int] = None,
            **kwargs,
    ) -> httpx.Response:
        """Make POST request"""
        return await self._request('POST', url, user_id=user_id, **kwargs)

    async def _request(
            self,
            method: str,
            url: str,
            user_id: Optional[int] = None,
            raise_exc: bool = True,
            **kwargs,
    ) -> httpx.Response:
        """Make an HTTP request"""
        url = self.get_url(url)
        self._before_request_log(url, method, user_id=user_id)

        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(method, url, timeout=self.timeout, **kwargs)
        except httpx.HTTPError as err:
            logger.exception({'message': str(err), 'user_id': user_id})
            raise self.EXC_CLASS(url=url, status_code=None, response_text=str(err))

        self._after_response_log(url=url, status_code=response.status_code, user_id=user_id)
        self._check_response(response, raise_exc=raise_exc)
        return response

    @staticmethod
    def _before_request_log(url: str, method: str, user_id: Optional[int] = None) -> None:
        """Log message before request started"""
        logger.info({
            'message': f'External {method} request to {url}',
            'user_id': user_id,
        })

    @staticmethod
    def _after_response_log(
            url: str,
            status_code: int,
            user_id: Optional[int] = None,
    ) -> None:
        """Log message ofter receiving response"""
        logger.info({
            'message': f'Received response from {url} with status code {status_code}',
            'user_id': user_id,
        })

    def _check_response(self, response: httpx.Response, raise_exc: bool = True) -> None:
        if response.is_error and raise_exc:
            raise self.EXC_CLASS(
                status_code=response.status_code,
                response_text=response.text,
                url=str(response.url),
            )
