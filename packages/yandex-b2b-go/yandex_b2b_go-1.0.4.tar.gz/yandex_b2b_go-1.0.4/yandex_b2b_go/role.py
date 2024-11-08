from typing import Dict, List, Optional

from yandex_b2b_go import utils
from yandex_b2b_go.client import Client
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.request import Request
from yandex_b2b_go.typing import Manager, ManagerResponse, ManagersListResponse, Role


class RoleManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def list(
        self,
        roles: Optional[List[Role]] = None,
        department_id: Optional[str] = None,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
    ) -> ManagersListResponse:
        params: Dict[str, str] = {}

        if roles is not None:
            params['roles'] = utils.serialize_list([role.value for role in roles], 'roles')
        if department_id is not None:
            if not isinstance(department_id, str):
                raise ValidationError(utils.error_string('department_id', department_id, 'str'))
            params['department_id'] = department_id
        if limit is not None:
            params['limit'] = utils.serialize_integer(limit, 'limit')
        if cursor is not None:
            if not isinstance(cursor, str):
                raise ValidationError(utils.error_string('cursor', cursor, 'int'))
            params['cursor'] = cursor

        request = Request(method='GET', endpoint='managers/list', params=params)
        response = await self._client.request(request=request)
        json = await response.json()

        if response.status == 200:
            return ManagersListResponse.new(json)

        raise ApiError.new(response.status, json)

    async def create(self, manager: Manager) -> ManagerResponse:
        if not isinstance(manager, Manager):
            raise ValidationError(utils.error_string('manager', manager, 'Manager'))
        request = Request(method='POST', endpoint='managers/create', data=manager.serialize())
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return ManagerResponse.new(json)

        raise ApiError.new(response.status, json)

    async def update(self, manager_id: str, manager: Manager) -> ManagerResponse:
        if not isinstance(manager, Manager):
            raise ValidationError(utils.error_string('manager', manager, 'Manager'))
        if not isinstance(manager_id, str):
            raise ValidationError(utils.error_string('manager_id', manager_id, 'str'))
        params: Dict[str, str] = {'id': manager_id}

        request = Request(method='POST', endpoint='managers/update', data=manager.serialize(), params=params)
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return ManagerResponse.new(json)

        raise ApiError.new(response.status, json)

    async def delete(self, manager_id: str) -> ManagerResponse:
        if not isinstance(manager_id, str):
            raise ValidationError(utils.error_string('manager_id', manager_id, 'str'))
        params: Dict[str, str] = {'id': manager_id}
        request = Request(method='POST', endpoint='managers/delete', params=params)
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return ManagerResponse.new(json)

        raise ApiError.new(response.status, json)
