from typing import Dict, Optional

from yandex_b2b_go import utils
from yandex_b2b_go.client import Client
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.request import Request
from yandex_b2b_go.typing import TankerOrdersResponse


class TankerOrderManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def list(
        self,
        user_id: Optional[str] = None,
        limit: Optional[int] = None,
        since_datetime: Optional[str] = None,
        till_datetime: Optional[str] = None,
    ) -> TankerOrdersResponse:
        params: Dict[str, str] = {}

        if user_id is not None:
            if not isinstance(user_id, str):
                raise ValidationError(utils.error_string('user_id', user_id, 'str'))
            params['user_id'] = user_id
        if limit is not None:
            params['limit'] = utils.serialize_integer(limit, 'limit')
        if since_datetime is not None:
            if not isinstance(since_datetime, str):
                raise ValidationError(utils.error_string('since_datetime', since_datetime, 'str'))
            params['since_datetime'] = since_datetime
        if till_datetime is not None:
            if not isinstance(till_datetime, str):
                raise ValidationError(utils.error_string('till_datetime', till_datetime, 'str'))
            params['till_datetime'] = till_datetime

        request = Request(method='GET', endpoint='orders/tanker', params=params)
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return TankerOrdersResponse.new(json)

        raise ApiError.new(response.status, json)


class TankerManager:
    _client: Client
    order: TankerOrderManager

    def __init__(self, client: Client):
        self._client = client
        self.order = TankerOrderManager(client)
