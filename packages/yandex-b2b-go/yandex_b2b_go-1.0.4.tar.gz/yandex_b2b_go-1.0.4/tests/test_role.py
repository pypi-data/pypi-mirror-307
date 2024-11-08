from typing import Any, Dict
from unittest.mock import AsyncMock

import pytest

from yandex_b2b_go import Client, RoleManager
from yandex_b2b_go.errors import ApiError
from yandex_b2b_go.typing import Manager, Role

BASE_ROLE_REQUEST = {
    'fullname': 'fullname',
    'phone': 'phone',
    'email': 'email@yandex.ru',
    'yandex_login': 'yandex_login',
    'role': Role.department_manager,
    'department_id': 'department_id1',
}
ROLE_1 = {
    **BASE_ROLE_REQUEST,
    'id': 'manager_id1',
    'role': Role.department_manager.value,
}
ROLE_2 = {
    **BASE_ROLE_REQUEST,
    'id': 'manager_id2',
    'department_id': 'department_id2',
    'role': Role.department_secretary.value,
}
ROLE_3 = {
    **BASE_ROLE_REQUEST,
    'id': 'manager_id3',
    'role': Role.client_manager.value,
}
RESPONSE_200 = {'id': 'manager_id1'}
RESPONSE_400 = {
    'code': 'BadRequest',
    'message': 'Unknown username (yandex_login)',
}
RESPONSE_LIST_400 = {
    'code': 'INVALID_QUERY',
    'message': 'handle v2_response failed withbad cursor',
}
RESPONSE_401 = {'code': 'unauthorized', 'message': 'Not authorized request'}
RESPONSE_403 = {'code': 'FORBIDDEN', 'message': 'Acl check have not passed'}
RESPONSE_404 = {'code': 'NOT_FOUND', 'message': 'Manager not found'}
RESPONSE_LIST_404 = {'code': 'NOT_FOUND', 'message': 'Not found'}


def mock_role_create(json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if json['yandex_login'] == 'invalid_login':
        response.status = 400
        response.json.return_value = RESPONSE_400
    elif json['department_id'] == 'other_department_id':
        response.status = 403
        response.json.return_value = RESPONSE_403
    else:
        response.status = 200
        response.json.return_value = RESPONSE_200

    return response


def mock_role_update(params, json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params['id'] == 'invalid_manager_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    elif json['yandex_login'] == 'invalid_login':
        response.status = 400
        response.json.return_value = RESPONSE_400
    elif json['department_id'] == 'other_department_id':
        response.status = 403
        response.json.return_value = RESPONSE_403
    else:
        response.status = 200
        response.json.return_value = RESPONSE_200

    return response


def mock_role_delete(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params['id'] == 'other_manager_id':
        response.status = 403
        response.json.return_value = RESPONSE_403
    elif params['id'] == 'invalid_manager_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    else:
        response.status = 200
        response.json.return_value = RESPONSE_200

    return response


def mock_role_list(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params.get('cursor') == 'invalid_cursor':
        response.status = 400
        response.json.return_value = RESPONSE_LIST_400
    elif params.get('cursor') == 'other_cursor':
        response.status = 403
        response.json.return_value = RESPONSE_403
    elif params.get('department_id') == 'invalid_department_id':
        response.status = 404
        response.json.return_value = RESPONSE_LIST_404
    else:
        items = [ROLE_1, ROLE_2, ROLE_3]

        if params.get('roles'):
            items = [item for item in items if item['role'] in params['roles']]
        if params.get('department_id'):
            items = [item for item in items if item['department_id'] == params['department_id']]

        return_value = {
            'total_amount': len(items),
            'next_cursor': 'next_cursor',
        }
        if 'cursor' in params:
            return_value['cursor'] = params['cursor']
            return_value['next_cursor'] = 'next_cursor2'
            items = items[1:]
        if 'limit' in params:
            limit = int(params['limit'])
            items = items[:limit]
        return_value['items'] = items
        return_value['limit'] = len(items)
        response.status = 200
        response.json.return_value = return_value

    return response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'role_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            BASE_ROLE_REQUEST,
            RESPONSE_200,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            {**BASE_ROLE_REQUEST, 'yandex_login': 'invalid_login'},
            RESPONSE_400,
            id='400 Unknown username',
        ),
        pytest.param(
            'invalid_token',
            BASE_ROLE_REQUEST,
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            {**BASE_ROLE_REQUEST, 'department_id': 'other_department_id'},
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
    ],
)
async def test_role_create(
    token: str,
    role_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        role_manager = RoleManager(client)
        manager = Manager(**role_params)
        try:
            resp = await role_manager.create(manager=manager)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'manager_id', 'role_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'manager_id1',
            BASE_ROLE_REQUEST,
            RESPONSE_200,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            'manager_id1',
            {**BASE_ROLE_REQUEST, 'yandex_login': 'invalid_login'},
            RESPONSE_400,
            id='400 Unknown username',
        ),
        pytest.param(
            'invalid_token',
            'manager_id1',
            BASE_ROLE_REQUEST,
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'manager_id1',
            {**BASE_ROLE_REQUEST, 'department_id': 'other_department_id'},
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
        pytest.param(
            'valid_token',
            'invalid_manager_id',
            BASE_ROLE_REQUEST,
            RESPONSE_404,
            id='404 Role not found',
        ),
    ],
)
async def test_role_update(
    token: str,
    manager_id: str,
    role_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        role_manager = RoleManager(client)
        manager = Manager(**role_params)
        try:
            resp = await role_manager.update(
                manager_id=manager_id,
                manager=manager,
            )
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'manager_id', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'manager_id1',
            RESPONSE_200,
            id='200 success',
        ),
        pytest.param(
            'invalid_token',
            'manager_id1',
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'other_manager_id',
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
        pytest.param(
            'valid_token',
            'invalid_manager_id',
            RESPONSE_404,
            id='404 Role not found',
        ),
    ],
)
async def test_role_delete(
    token: str,
    manager_id: str,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        role_manager = RoleManager(client)
        try:
            resp = await role_manager.delete(manager_id=manager_id)
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
                'items': [ROLE_1, ROLE_2, ROLE_3],
                'limit': 3,
                'total_amount': 3,
                'next_cursor': 'next_cursor',
            },
            id='200 success without params',
        ),
        pytest.param(
            'valid_token',
            {'limit': 2},
            {
                'items': [ROLE_1, ROLE_2],
                'limit': 2,
                'total_amount': 3,
                'next_cursor': 'next_cursor',
            },
            id='200 success with limit',
        ),
        pytest.param(
            'valid_token',
            {'cursor': 'cursor'},
            {
                'items': [ROLE_2, ROLE_3],
                'limit': 2,
                'total_amount': 3,
                'cursor': 'cursor',
                'next_cursor': 'next_cursor2',
            },
            id='200 success with cursor',
        ),
        pytest.param(
            'valid_token',
            {'roles': [Role.department_manager]},
            {
                'items': [ROLE_1],
                'limit': 1,
                'total_amount': 1,
                'next_cursor': 'next_cursor',
            },
            id='200 success with roles',
        ),
        pytest.param(
            'valid_token',
            {'department_id': 'department_id2'},
            {
                'items': [ROLE_2],
                'limit': 1,
                'total_amount': 1,
                'next_cursor': 'next_cursor',
            },
            id='200 success with department_id',
        ),
        pytest.param(
            'valid_token',
            {'cursor': 'invalid_cursor'},
            RESPONSE_LIST_400,
            id='400 invalid params cursor',
        ),
        pytest.param('invalid_token', {}, RESPONSE_401, id='401 unauthorized'),
        pytest.param(
            'valid_token',
            {'cursor': 'other_cursor'},
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
        pytest.param(
            'valid_token',
            {'department_id': 'invalid_department_id'},
            RESPONSE_LIST_404,
            id='404 Role not found',
        ),
    ],
)
async def test_role_list(
    token: str,
    params: Dict[str, str],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        role_manager = RoleManager(client)
        try:
            resp = await role_manager.list(**params)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
