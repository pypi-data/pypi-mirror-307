from typing import Dict, Optional

from yandex_b2b_go import utils
from yandex_b2b_go.client import Client
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.request import Request
from yandex_b2b_go.typing import (
    Department,
    DepartmentBudget,
    DepartmentBudgetResponse,
    DepartmentCreateResponse,
    DepartmentDeleteResponse,
    DepartmentListResponse,
    DepartmentUpdateRequest,
    DepartmentUpdateResponse,
)


class DepartmentTaxiLimitManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def update(self, department_id: str, limit: DepartmentBudget) -> DepartmentUpdateResponse:
        if not isinstance(department_id, str):
            raise ValidationError(utils.error_string('department_id', department_id, 'str'))
        if not isinstance(limit, DepartmentBudget):
            raise ValidationError(utils.error_string('limit', limit, 'DepartmentBudget'))

        params: Dict[str, str] = {'department_id': department_id}

        request = Request(
            method='POST',
            endpoint='departments/limits/taxi/update',
            params=params,
            data=limit.serialize(),
        )

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return DepartmentUpdateResponse.new()

        raise ApiError.new(response.status, json)

    async def get(self, department_id: str) -> DepartmentBudgetResponse:
        if not isinstance(department_id, str):
            raise ValidationError(utils.error_string('department_id', department_id, 'str'))

        params: Dict[str, str] = {'department_id': department_id}

        request = Request(method='GET', endpoint='departments/limits/taxi', params=params)

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return DepartmentBudgetResponse.new(json)

        raise ApiError.new(response.status, json)


class DepartmentLimitManager:
    _client: Client
    taxi: DepartmentTaxiLimitManager

    def __init__(self, client: Client):
        self._client = client
        self.taxi = DepartmentTaxiLimitManager(client)


class DepartmentManager:
    _client: Client
    limit: DepartmentLimitManager

    def __init__(self, client: Client):
        self._client = client
        self.limit = DepartmentLimitManager(client)

    async def create(self, department: Department) -> DepartmentCreateResponse:
        request = Request(method='POST', endpoint='departments/create', data=department.serialize())
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return DepartmentCreateResponse.new(json)

        raise ApiError.new(response.status, json)

    async def list(self, limit: Optional[int] = None, offset: Optional[int] = None) -> DepartmentListResponse:
        params: Dict[str, str] = {}

        if limit is not None:
            params['limit'] = utils.serialize_integer(limit, 'limit')
        if offset is not None:
            params['offset'] = utils.serialize_integer(offset, 'offset')

        request = Request(method='GET', endpoint='departments/list', params=params)

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return DepartmentListResponse.new(json)

        raise ApiError.new(response.status, json)

    async def update(self, department_id: str, department: DepartmentUpdateRequest) -> DepartmentUpdateResponse:
        if not isinstance(department_id, str):
            raise ValidationError(utils.error_string('department_id', department_id, 'str'))
        if not isinstance(department, DepartmentUpdateRequest):
            raise ValidationError(utils.error_string('department', department, 'DepartmentUpdateRequest'))

        params: Dict[str, str] = {'department_id': department_id}

        request = Request(method='PUT', endpoint='departments/update', params=params, data=department.serialize())

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return DepartmentUpdateResponse.new()

        raise ApiError.new(response.status, json)

    async def delete(self, department_id: str) -> DepartmentDeleteResponse:
        if not isinstance(department_id, str):
            raise ValidationError(utils.error_string('department_id', department_id, 'str'))
        params: Dict[str, str] = {'department_id': department_id}
        request = Request(method='POST', endpoint='departments/archive', params=params)
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return DepartmentDeleteResponse.new(json)

        raise ApiError.new(response.status, json)
