from typing import Dict, Optional

from yandex_b2b_go import utils
from yandex_b2b_go.client import Client
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.request import Request
from yandex_b2b_go.typing import (
    User,
    UserCreateResponse,
    UserGetResponse,
    UserListResponse,
    UsersSpendingListRequest,
    UsersSpendingListResponse,
    UserUpdateResponse,
)


class SpendingManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def list(self, user_ids: UsersSpendingListRequest) -> UsersSpendingListResponse:
        if not isinstance(user_ids, UsersSpendingListRequest):
            raise ValidationError(utils.error_string('user_ids', user_ids, 'UsersSpendingListRequest'))
        request = Request(method='POST', endpoint='users-spending-details', data=user_ids.serialize())

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return UsersSpendingListResponse.new(json)

        raise ApiError.new(response.status, json)


class UserManager:
    _client: Client
    spending: SpendingManager

    def __init__(self, client: Client):
        self._client = client
        self.spending = SpendingManager(client)

    async def create(self, user: User) -> UserCreateResponse:
        if not isinstance(user, User):
            raise ValidationError(utils.error_string('user', user, 'User'))

        request = Request(method='POST', endpoint='users', data=user.serialize())
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return UserCreateResponse.new(json)

        raise ApiError.new(response.status, json)

    async def list(self, limit: Optional[int] = None, cursor: Optional[str] = None) -> UserListResponse:
        params: Dict[str, str] = {}

        if limit is not None:
            params['limit'] = utils.serialize_integer(limit, 'limit')
        if cursor is not None:
            if not isinstance(cursor, str):
                raise ValidationError(utils.error_string('cursor', cursor, 'str'))

            params['cursor'] = cursor

        request = Request(method='GET', endpoint='users', params=params)

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return UserListResponse.new(json)

        raise ApiError.new(response.status, json)

    async def get(self, user_id: str) -> UserGetResponse:
        if not isinstance(user_id, str):
            raise ValidationError(utils.error_string('user_id', user_id, 'str'))

        params: Dict[str, str] = {'user_id': user_id}

        request = Request(method='GET', endpoint='users', params=params)

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return UserGetResponse.new(json)

        raise ApiError.new(response.status, json)

    async def update(self, user_id: str, user: User) -> UserUpdateResponse:
        if not isinstance(user_id, str):
            raise ValidationError(utils.error_string('user_id', user_id, 'str'))
        if not isinstance(user, User):
            raise ValidationError(utils.error_string('user', user, 'User'))

        params: Dict[str, str] = {'user_id': user_id}

        request = Request(method='PUT', endpoint='users', params=params, data=user.serialize())

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return UserUpdateResponse.new(json)

        raise ApiError.new(response.status, json)

    async def archive(self, user_id: str) -> UserUpdateResponse:
        if not isinstance(user_id, str):
            raise ValidationError(utils.error_string('user_id', user_id, 'str'))

        params: Dict[str, str] = {'user_id': user_id}

        request = Request(method='POST', endpoint='users/archive', params=params)

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return UserUpdateResponse.new(json)

        raise ApiError.new(response.status, json)
