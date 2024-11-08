from typing import Any, Dict
from unittest.mock import AsyncMock

import pytest

from yandex_b2b_go import Client, DepartmentManager
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.typing import (
    Department,
    DepartmentBudget,
    DepartmentLimitsResponse,
    DepartmentUpdateRequest,
)

BASE_DEPARTMENT_REQUEST = {
    'name': 'department_name1',
    'parent_id': 'department_id',
}
BASE_LIMIT_PARAMS = {'budget': 12.5}
DEPARTMENT_1 = {
    'id': 'department_id1',
    'name': 'department_name1',
    'limits': DepartmentLimitsResponse(
        taxi=DepartmentBudget(1000),
        eats=DepartmentBudget(1000),
        tanker=DepartmentBudget(1000),
        cargo=DepartmentBudget(1000),
    ).serialize(),
    'parent_id': None,
}
DEPARTMENT_2 = {**DEPARTMENT_1, 'id': 'department_id2'}
DEPARTMENT_3 = {**DEPARTMENT_1, 'id': 'department_id3'}
RESPONSE_200 = {'_id': 'department_id1'}
RESPONSE_400 = {
    'code': 'REQUEST_VALIDATION_ERROR',
    'message': 'Some parameters are invalid',
}
RESPONSE_401 = {'code': 'unauthorized', 'message': 'Not authorized request'}
RESPONSE_403 = {'code': 'FORBIDDEN', 'message': 'Acl check have not passed'}
RESPONSE_404 = {'code': 'DEPARTMENT_NOT_FOUND', 'message': 'Not found'}
RESPONSE_LIST_404 = {'code': 'NOT_FOUND', 'message': 'Not found'}
RESPONSE_LIST_400 = {
    'code': 'BadRequest',
    'message': 'has incorrect offset',
    'reason': 'offset should be greater than 0, got -5',
}
RESPONSE_UPDATE_200 = {}
RESPONSE_DELETE_200 = {'deleted_ids': ['department_id1']}
RESPONSE_TAXI_LIMIT_200 = {'budget': 1000}


def mock_department_create(json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if json['parent_id'] == 'invalid_id':
        response.status = 400
        response.json.return_value = RESPONSE_400
    elif json['parent_id'] == 'other_department_id':
        response.status = 403
        response.json.return_value = RESPONSE_403
    elif json['parent_id'] == 'unknown_department_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    else:
        response.status = 200
        response.json.return_value = RESPONSE_200

    return response


def mock_department_list(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    items = [DEPARTMENT_1, DEPARTMENT_2, DEPARTMENT_3]

    if params.get('offset') == '-5':
        response.status = 400
        response.json.return_value = RESPONSE_LIST_400
    else:
        return_value = {'total_amount': len(items), 'limit': 100, 'offset': 0}
        if 'offset' in params:
            offset = int(params['offset'])
            items = items[offset:]
            return_value['offset'] = offset
        if 'limit' in params:
            limit = int(params['limit'])
            items = items[:limit]
            return_value['limit'] = limit

        return_value['items'] = items
        response.status = 200
        response.json.return_value = return_value
    return response


def mock_department_update(params, json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if json['name'] == 'invalid_name':
        response.status = 400
        response.json.return_value = RESPONSE_400
    elif params['department_id'] == 'invalid_department_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    elif params['department_id'] == 'other_department_id':
        response.status = 403
        response.json.return_value = RESPONSE_403
    else:
        response.status = 200
        response.json.return_value = RESPONSE_UPDATE_200

    return response


def mock_department_delete(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params['department_id'] == 'invalid_department_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    elif params['department_id'] == 'other_department_id':
        response.status = 403
        response.json.return_value = RESPONSE_403
    else:
        response.status = 200
        response.json.return_value = RESPONSE_DELETE_200

    return response


def mock_department_taxi_limit_get(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params['department_id'] == 'department_id1':
        response.status = 200
        response.json.return_value = RESPONSE_TAXI_LIMIT_200
    elif params['department_id'] == 'invalid_department_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    elif params['department_id'] == 'other_department_id':
        response.status = 403
        response.json.return_value = RESPONSE_403

    return response


def mock_department_taxi_limit_update(params, json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if json['budget'] == 'invalid_budget':
        response.status = 400
        response.json.return_value = RESPONSE_400
    elif params['department_id'] == 'department_id':
        response.status = 200
        response.json.return_value = RESPONSE_UPDATE_200
    elif params['department_id'] == 'invalid_department_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    elif params['department_id'] == 'other_department_id':
        response.status = 403
        response.json.return_value = RESPONSE_403

    return response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'department_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            BASE_DEPARTMENT_REQUEST,
            RESPONSE_200,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            {**BASE_DEPARTMENT_REQUEST, 'parent_id': 'invalid_id'},
            RESPONSE_400,
            id='400 Invalid parent_id',
        ),
        pytest.param(
            'valid_token',
            {**BASE_DEPARTMENT_REQUEST, 'parent_id': 'unknown_department_id'},
            RESPONSE_404,
            id='400 Unknown parent_id',
        ),
        pytest.param(
            'invalid_token',
            BASE_DEPARTMENT_REQUEST,
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            {**BASE_DEPARTMENT_REQUEST, 'parent_id': 'other_department_id'},
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
    ],
)
async def test_department_create(
    token: str,
    department_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        department_manager = DepartmentManager(client)
        department = Department(**department_params)
        try:
            resp = await department_manager.create(department=department)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            {},
            {
                'items': [DEPARTMENT_1, DEPARTMENT_2, DEPARTMENT_3],
                'limit': 100,
                'total_amount': 3,
                'offset': 0,
            },
            id='200 success without params',
        ),
        pytest.param(
            'valid_token',
            {'limit': 2},
            {
                'items': [DEPARTMENT_1, DEPARTMENT_2],
                'limit': 2,
                'total_amount': 3,
                'offset': 0,
            },
            id='200 success with limit',
        ),
        pytest.param(
            'valid_token',
            {'offset': 1},
            {
                'items': [DEPARTMENT_2, DEPARTMENT_3],
                'limit': 100,
                'total_amount': 3,
                'offset': 1,
            },
            id='200 success with offset',
        ),
        pytest.param(
            'valid_token',
            {'limit': 1, 'offset': 1},
            {
                'items': [DEPARTMENT_2],
                'limit': 1,
                'total_amount': 3,
                'offset': 1,
            },
            id='200 success with limit and offset',
        ),
        pytest.param(
            'valid_token',
            {'offset': -5},
            RESPONSE_LIST_400,
            id='400 invalid params offset',
        ),
    ],
)
async def test_department_list(
    token: str,
    params: Dict[str, str],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        department_manager = DepartmentManager(client)
        try:
            resp = await department_manager.list(**params)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
        except ValidationError as validation_error:
            assert validation_error.args[0] == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'department_id', 'department_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'department_id1',
            BASE_DEPARTMENT_REQUEST,
            RESPONSE_UPDATE_200,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            'department_id1',
            {**BASE_DEPARTMENT_REQUEST, 'name': 'invalid_name'},
            RESPONSE_400,
            id='400 Invalid name',
        ),
        pytest.param(
            'invalid_token',
            'department_id1',
            BASE_DEPARTMENT_REQUEST,
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'other_department_id',
            BASE_DEPARTMENT_REQUEST,
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
        pytest.param(
            'valid_token',
            'invalid_department_id',
            BASE_DEPARTMENT_REQUEST,
            RESPONSE_404,
            id='404 Department not found',
        ),
    ],
)
async def test_department_update(
    token: str,
    department_id: str,
    department_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        department_manager = DepartmentManager(client)
        department = DepartmentUpdateRequest(**department_params)
        try:
            resp = await department_manager.update(
                department_id=department_id,
                department=department,
            )
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'department_id', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'department_id1',
            RESPONSE_DELETE_200,
            id='200 success',
        ),
        pytest.param(
            'invalid_token',
            'department_id1',
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'other_department_id',
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
        pytest.param(
            'valid_token',
            'invalid_department_id',
            RESPONSE_404,
            id='404 Department not found',
        ),
    ],
)
async def test_department_delete(
    token: str,
    department_id: str,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        department_manager = DepartmentManager(client)
        try:
            resp = await department_manager.delete(department_id=department_id)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'department_id', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'department_id1',
            RESPONSE_TAXI_LIMIT_200,
            id='200 success',
        ),
        pytest.param(
            'invalid_token',
            'department_id1',
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'other_department_id',
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
        pytest.param(
            'valid_token',
            'invalid_department_id',
            RESPONSE_404,
            id='404 Department not found',
        ),
    ],
)
async def test_department_taxi_limit_get(
    token: str,
    department_id: str,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        department_manager = DepartmentManager(client)
        try:
            resp = await department_manager.limit.taxi.get(
                department_id=department_id,
            )
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'department_id', 'limit_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'department_id',
            BASE_LIMIT_PARAMS,
            RESPONSE_UPDATE_200,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            'department_id1',
            {**BASE_LIMIT_PARAMS, 'budget': 'invalid_budget'},
            "Invalid value for budget: 'invalid_budget' is not instance of Union[float, int, Decimal]",
            id='400 invalid budget',
        ),
        pytest.param(
            'invalid_token',
            'department_id1',
            BASE_LIMIT_PARAMS,
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'other_department_id',
            BASE_LIMIT_PARAMS,
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
        pytest.param(
            'valid_token',
            'invalid_department_id',
            BASE_LIMIT_PARAMS,
            RESPONSE_404,
            id='404 Department not found',
        ),
    ],
)
async def test_department_taxi_limit_update(
    token: str,
    department_id: str,
    limit_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        department_manager = DepartmentManager(client)
        try:
            limit = DepartmentBudget(**limit_params)
            resp = await department_manager.limit.taxi.update(
                department_id=department_id,
                limit=limit,
            )
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
        except ValidationError as validation_error:
            assert validation_error.args[0] == expected_response
