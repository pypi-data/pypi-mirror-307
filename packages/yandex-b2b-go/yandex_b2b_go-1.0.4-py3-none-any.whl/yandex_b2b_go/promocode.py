import uuid
from typing import Dict, Optional

from yandex_b2b_go import utils
from yandex_b2b_go.client import Client
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.request import Request
from yandex_b2b_go.typing import (
    CodeListResponse,
    Promocode,
    PromocodeCreateResponse,
    PromocodeOrderCancelResponse,
    PromocodeOrderListResponse,
    PromocodeOrderResponse,
)


class CodeManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def list(self, order_id: str, limit: Optional[int] = None, cursor: Optional[str] = None) -> CodeListResponse:
        if not isinstance(order_id, str):
            raise ValidationError(utils.error_string('order_id', order_id, 'str'))
        params: Dict[str, str] = {'order_id': order_id}
        if limit is not None:
            params['limit'] = utils.serialize_integer(limit, 'limit')
        if cursor is not None:
            if not isinstance(cursor, str):
                raise ValidationError(utils.error_string('cursor', cursor, 'str'))
            params['cursor'] = cursor

        request = Request(method='GET', endpoint='promocodes/orders/codes/list', params=params)
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return CodeListResponse.new(json)

        raise ApiError.new(response.status, json)


class PromocodeOrderManager:
    _client: Client
    code: CodeManager

    def __init__(self, client: Client):
        self._client = client
        self.code = CodeManager(client)

    async def list(self, limit: int, cursor: Optional[str] = None) -> PromocodeOrderListResponse:
        params: Dict[str, str] = {
            'limit': utils.serialize_integer(limit, 'limit'),
        }

        if cursor is not None:
            if not isinstance(cursor, str):
                raise ValidationError(utils.error_string('cursor', cursor, 'str'))
            params['cursor'] = cursor

        request = Request(method='GET', endpoint='promocodes/orders/list', params=params)
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return PromocodeOrderListResponse.new(json)

        raise ApiError.new(response.status, json)

    async def get(self, order_id: str) -> PromocodeOrderResponse:
        if not isinstance(order_id, str):
            raise ValidationError(utils.error_string('order_id', order_id, 'str'))
        params: Dict[str, str] = {'order_id': order_id}

        request = Request(method='GET', endpoint='promocodes/orders/info', params=params)
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return PromocodeOrderResponse.new(json)

        raise ApiError.new(response.status, json)

    async def create(self, promocode: Promocode, idempotency_token: uuid.UUID) -> PromocodeCreateResponse:
        if not isinstance(promocode, Promocode):
            raise ValidationError(utils.error_string('promocode', promocode, 'Promocode'))
        if not isinstance(idempotency_token, uuid.UUID):
            raise ValidationError(utils.error_string('idempotency_token', idempotency_token, 'uuid.UUID'))
        headers = {'X-Idempotency-Token': str(idempotency_token)}
        request = Request(
            method='POST',
            endpoint='promocodes/orders/create',
            data=promocode.serialize(),
            headers=headers,
        )
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return PromocodeCreateResponse.new(json)

        raise ApiError.new(response.status, json)

    async def cancel(self, order_id: str) -> PromocodeOrderCancelResponse:
        if not isinstance(order_id, str):
            raise ValidationError(utils.error_string('order_id', order_id, 'str'))
        params: Dict[str, str] = {'order_id': order_id}

        request = Request(method='POST', endpoint='promocodes/orders/cancel', params=params)
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return PromocodeOrderCancelResponse.new(json)

        raise ApiError.new(response.status, json)


class PromocodeManager:
    _client: Client
    order: PromocodeOrderManager

    def __init__(self, client: Client):
        self._client = client
        self.order = PromocodeOrderManager(client)
