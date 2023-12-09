from typing import Union, Any

import ujson


class DoesNotExistException(Exception):
    pass


class ValidationException(Exception):
    pass


class HTTPClientException(Exception):
    def __init__(self, url: str, status_code: int | None, response_text: str):
        self.url = url
        self.status_code = status_code
        self.response_text = response_text

    def json(self) -> Union[dict[str, Any], None]:
        try:
            return ujson.loads(self.response_text)

        except ValueError:
            return None

    def __str__(self) -> str:
        return f'URL {self.url} responded with {self.status_code}. RESPONSE: {self.response_text}'

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} status_code={self.status_code}>'
