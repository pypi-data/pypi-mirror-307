from typing import Dict, Optional

from yandex_b2b_go import utils
from yandex_b2b_go.client import Client
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.request import Request
from yandex_b2b_go.typing import (
    EatOrderListResponse,
    EatsOrdersListRequest,
    SortingOrder,
)


class EatOrderManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def list(
        self,
        user_ids: EatsOrdersListRequest,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        since_datetime: Optional[str] = None,
        till_datetime: Optional[str] = None,
        since_date: Optional[str] = None,
        till_date: Optional[str] = None,
        sorting_order: Optional[SortingOrder] = None,
    ) -> EatOrderListResponse:
        params: Dict[str, str] = {}

        if limit is not None:
            params['limit'] = utils.serialize_integer(limit, 'limit')
        if cursor is not None:
            if not isinstance(cursor, str):
                raise ValidationError(utils.error_string('cursor', cursor, 'str'))
            params['cursor'] = cursor
        if since_datetime is not None:
            if not isinstance(since_datetime, str):
                raise ValidationError(utils.error_string('since_datetime', since_datetime, 'str'))
            params['since_datetime'] = since_datetime
        if till_datetime is not None:
            if not isinstance(till_datetime, str):
                raise ValidationError(utils.error_string('till_datetime', till_datetime, 'str'))
            params['till_datetime'] = till_datetime
        if since_date is not None:
            if not isinstance(since_date, str):
                raise ValidationError(utils.error_string('since_date', since_date, 'str'))
            params['since_date'] = since_date
        if till_date is not None:
            if not isinstance(till_date, str):
                raise ValidationError(utils.error_string('till_date', till_date, 'str'))
            params['till_date'] = till_date
        if sorting_order is not None:
            if not isinstance(sorting_order, SortingOrder):
                raise ValidationError(utils.error_string('sorting_order', sorting_order, 'SortingOrder'))
            params['sorting_order'] = sorting_order.value

        request = Request(method='POST', endpoint='orders/eats/list', params=params, data=user_ids.serialize())
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return EatOrderListResponse.new(json)

        raise ApiError.new(response.status, json)


class EatManager:
    _client: Client
    order: EatOrderManager

    def __init__(self, client: Client):
        self._client = client
        self.order = EatOrderManager(client)
