import asyncio
import logging
from typing import Optional
from urllib import parse

import aiohttp

from yandex_b2b_go.errors import ValidationError
from yandex_b2b_go.request import Request
from yandex_b2b_go.utils import error_string
from yandex_b2b_go.version import __version__

logger = logging.getLogger(__name__)


class Client:
    token: str
    timeout: aiohttp.ClientTimeout
    log_level: int = logging.INFO
    log_request: bool = False
    log_response: bool = False

    def __init__(
        self,
        token: str,
        timeout: Optional[float] = None,
        log_level: int = logging.INFO,
        log_request: bool = False,
        log_response: bool = False,
    ):
        if not isinstance(token, str):
            raise ValidationError(error_string('token', token, 'str'))
        self._token = token
        self._session = aiohttp.ClientSession()
        self._base_url = 'https://b2b-api.go.yandex.ru/integration/2.0/'
        if timeout is not None:
            if not isinstance(timeout, float):
                raise ValidationError(error_string('timeout', timeout, 'float'))
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        if not isinstance(log_level, int):
            raise ValidationError(error_string('log_level', log_level, 'int'))
        self.log_level = log_level
        if not isinstance(log_request, bool):
            raise ValidationError(error_string('log_request', log_request, 'bool'))
        self.log_request = log_request
        if not isinstance(log_response, bool):
            raise ValidationError(error_string('log_response', log_response, 'bool'))
        self.log_response = log_response

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if not self._session.closed:
            await self._session.close()

    def __del__(self):
        if not self._session.closed:
            asyncio.create_task(self._session.close())

    def _build_url(self, request: Request) -> str:
        url = self._base_url + request.endpoint
        if request.params:
            params = '?' + parse.urlencode(request.params)
        else:
            params = ''
        full_url = url + params
        if self.log_request:
            logger.log(
                self.log_level,
                'Request=%s, for url=%s, params=%s, body=%s',
                request.method,
                full_url,
                request.params,
                request.data,
            )
        else:
            logger.log(self.log_level, 'Performing %s request to %s', request.method, url)
        return url

    async def request(self, request: Request) -> aiohttp.ClientResponse:
        url = self._build_url(request)
        headers = {
            **request.headers,
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json',
            'User-Agent': f'yandex_b2b_go_lib_{__version__}/python',
        }

        try:
            response = await self._session.request(
                method=request.method,
                url=url,
                params=request.params,
                json=request.data,
                headers=headers,
                timeout=self.timeout,
            )

            try:
                body = await response.json()
            except aiohttp.client_exceptions.ContentTypeError:
                body = {}

            if self.log_response and body:
                logger.log(
                    self.log_level,
                    '%s request %s success with status code %s, body=%s',
                    request.method,
                    url,
                    response.status,
                    str(body),
                )
            else:
                logger.log(
                    self.log_level,
                    '%s request %s success with status code %s',
                    request.method,
                    url,
                    response.status,
                )
            return response
        except Exception as exc:
            error_head = exc.__class__.__name__
            error_body = exc

            logger.warning('%s request %s fail with %s: %s', request.method, url, error_head, error_body)
            raise
