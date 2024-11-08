import uuid
from typing import Dict, Optional

import aiohttp

from yandex_b2b_go import utils
from yandex_b2b_go.client import Client
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.request import Request
from yandex_b2b_go.typing import (
    Feedback,
    Order,
    OrderCreateResponse,
    OrderRequest,
    OrdersCancelRequest,
    SortingDirection,
    SortingField,
    TaxiActiveOrderListResponse,
    TaxiFeedbackCreateResponse,
    TaxiOrderCancelResponse,
    TaxiOrderDestinationsUpdateRequest,
    TaxiOrderDestinationsUpdateResponse,
    TaxiOrderGetResponse,
    TaxiOrderListResponse,
    TaxiOrderRoutestatsGetResponse,
    TaxiOrderStatusGetResponse,
)


class TaxiActiveOrderManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def list(self, user_id: str) -> TaxiActiveOrderListResponse:
        if not isinstance(user_id, str):
            raise ValidationError(utils.error_string('user_id', user_id, 'str'))
        params: Dict[str, str] = {'user_id': user_id}

        request = Request(method='GET', endpoint='orders/active', params=params)
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return TaxiActiveOrderListResponse.new(json)

        raise ApiError.new(response.status, json)


class TaxiOrderRoutestatsManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def get(self, order: OrderRequest) -> TaxiOrderRoutestatsGetResponse:
        if not isinstance(order, OrderRequest):
            raise ValidationError(utils.error_string('order', order, 'OrderRequest'))

        request = Request(method='POST', endpoint='orders/routestats', data=order.serialize())

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return TaxiOrderRoutestatsGetResponse.new(json)

        raise ApiError.new(response.status, json)


class TaxiOrderFeedbackManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def create(self, order_id: str, feedback: Feedback) -> TaxiFeedbackCreateResponse:
        if not isinstance(order_id, str):
            raise ValidationError(utils.error_string('order_id', order_id, 'str'))
        if not isinstance(feedback, Feedback):
            raise ValidationError(utils.error_string('feedback', feedback, 'Feedback'))
        params: Dict[str, str] = {'order_id': order_id}

        request = Request(method='POST', endpoint='orders/feedback', params=params, data=feedback.serialize())
        response = await self._client.request(request=request)
        try:
            json = await response.json()
        except aiohttp.client_exceptions.ContentTypeError:
            json = {}
        if response.status == 200:
            return TaxiFeedbackCreateResponse.new()

        raise ApiError.new(response.status, json)


class TaxiOrderDestinationsManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def update(
        self,
        order_id: str,
        destinations: TaxiOrderDestinationsUpdateRequest,
    ) -> TaxiOrderDestinationsUpdateResponse:
        if not isinstance(order_id, str):
            raise ValidationError(utils.error_string('order_id', order_id, 'str'))
        if not isinstance(destinations, TaxiOrderDestinationsUpdateRequest):
            raise ValidationError(utils.error_string('rote', destinations, 'TaxiOrderRoteUpdateRequest'))

        params: Dict[str, str] = {'order_id': order_id}

        request = Request(
            method='POST',
            endpoint='orders/change-destinations',
            params=params,
            data=destinations.serialize(),
        )

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return TaxiOrderDestinationsUpdateResponse.new(json)

        raise ApiError.new(response.status, json)


class TaxiOrderStatusManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def get(self, order_id: str) -> TaxiOrderStatusGetResponse:
        if not isinstance(order_id, str):
            raise ValidationError(utils.error_string('order_id', order_id, 'str'))

        params: Dict[str, str] = {'order_id': order_id}

        request = Request(method='GET', endpoint='orders/progress', params=params)

        response = await self._client.request(
            request=request,
        )

        json = await response.json()

        if response.status == 200:
            return TaxiOrderStatusGetResponse.new(json)

        raise ApiError.new(response.status, json)


class TaxiOrderManager:
    _client: Client
    active: TaxiActiveOrderManager
    routestats: TaxiOrderRoutestatsManager
    feedback: TaxiOrderFeedbackManager
    destinations: TaxiOrderDestinationsManager
    status: TaxiOrderStatusManager

    def __init__(self, client: Client):
        self._client = client
        self.active = TaxiActiveOrderManager(client)
        self.routestats = TaxiOrderRoutestatsManager(client)
        self.feedback = TaxiOrderFeedbackManager(client)
        self.destinations = TaxiOrderDestinationsManager(client)
        self.status = TaxiOrderStatusManager(client)

    async def get(self, order_id: str) -> TaxiOrderGetResponse:
        if not isinstance(order_id, str):
            raise ValidationError(
                utils.error_string('order_id', order_id, 'str'),
            )

        params: Dict[str, str] = {'order_id': order_id}

        request = Request(method='GET', endpoint='orders/info', params=params)

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return TaxiOrderGetResponse.new(json)

        raise ApiError.new(response.status, json)

    async def create(self, order: Order, idempotency_token: uuid.UUID) -> OrderCreateResponse:
        if not isinstance(order, Order):
            raise ValidationError(utils.error_string('order', order, 'Order'))
        if not isinstance(idempotency_token, uuid.UUID):
            raise ValidationError(utils.error_string('idempotency_token', idempotency_token, 'uuid.UUID'))
        headers = {'X-Idempotency-Token': str(idempotency_token)}
        request = Request(
            method='POST',
            endpoint='orders/create',
            data=order.serialize(),
            headers=headers,
        )
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return OrderCreateResponse.new(json)

        raise ApiError.new(response.status, json)

    async def list(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        since_datetime: Optional[str] = None,
        till_datetime: Optional[str] = None,
        sorting_field: Optional[SortingField] = None,
        sorting_direction: Optional[SortingDirection] = None,
    ) -> TaxiOrderListResponse:
        params: Dict[str, str] = {}

        if limit is not None:
            params['limit'] = utils.serialize_integer(limit, 'limit')
        if offset is not None:
            params['offset'] = utils.serialize_integer(offset, 'offset')
        if since_datetime is not None:
            if not isinstance(since_datetime, str):
                raise ValidationError(utils.error_string('since_datetime', since_datetime, 'str'))
            params['since_datetime'] = since_datetime
        if till_datetime is not None:
            if not isinstance(till_datetime, str):
                raise ValidationError(utils.error_string('till_datetime', till_datetime, 'str'))
        if sorting_field is not None:
            if not isinstance(sorting_field, SortingField):
                raise ValidationError(utils.error_string('sorting_field', sorting_field, 'SortingField'))
            params['sorting_field'] = sorting_field.value
        if sorting_direction is not None:
            if not isinstance(sorting_direction, SortingDirection):
                raise ValidationError(utils.error_string('sorting_direction', sorting_direction, 'SortingDirection'))
            params['sorting_direction'] = utils.serialize_integer(sorting_direction.value, 'sorting_direction')

        request = Request(method='GET', endpoint='orders/list', params=params)
        response = await self._client.request(request=request)

        json = await response.json()
        if response.status == 200:
            return TaxiOrderListResponse.new(json)

        raise ApiError.new(response.status, json)

    async def cancel(self, order_id: str, cancel_state: OrdersCancelRequest) -> TaxiOrderCancelResponse:
        if not isinstance(order_id, str):
            raise ValidationError(utils.error_string('order_id', order_id, 'str'))

        params: Dict[str, str] = {'order_id': order_id}
        data = cancel_state.serialize()
        request = Request(
            method='POST',
            endpoint='orders/cancel',
            params=params,
            data=data,
        )

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return TaxiOrderCancelResponse.new(json)

        raise ApiError.new(response.status, json)


class TaxiManager:
    _client: Client
    order: TaxiOrderManager

    def __init__(self, client: Client):
        self._client = client
        self.order = TaxiOrderManager(client)
