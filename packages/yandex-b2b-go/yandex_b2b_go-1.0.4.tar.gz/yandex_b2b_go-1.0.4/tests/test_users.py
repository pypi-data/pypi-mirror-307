from typing import Any, Dict
from unittest.mock import AsyncMock

import pytest

from yandex_b2b_go import Client, UserManager
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.typing import Limit, Service, User

BASE_USER_REQUEST = {
    'fullname': 'fullname4',
    'phone': 'phone4',
    'is_active': True,
    'limits': [Limit(limit_id='limit_id1', service=Service.taxi)],
}
USER_RESPONSE = {
    'fullname': 'FullName',
    'phone': 'phone',
    'is_active': True,
    'id': 'user_id1',
    'is_deleted': False,
    'client_id': 'client_id',
    'email': 'email',
    'cost_center': 'cost_center',
    'cost_centers_id': 'cost_centers_id',
    'nickname': 'nickname',
    'department_id': 'department_id',
    'limits': [
        {'limit_id': 'limit_id1', 'service': 'taxi'},
        {'limit_id': 'limit_id2', 'service': 'drive'},
    ],
}
USER_2 = {
    'fullname': 'FullName2',
    'phone': 'phone2',
    'is_active': True,
    'id': 'user_id2',
    'is_deleted': False,
    'client_id': 'client_id',
}
USER_3 = {
    'fullname': 'FullName3',
    'phone': 'phone3',
    'is_active': True,
    'id': 'user_id3',
    'is_deleted': False,
    'client_id': 'client_id',
    'cost_centers_id': 'cost_centers_id',
    'limits': [{'limit_id': 'limit_id1', 'service': 'taxi'}],
}
USER_SUCCESS_UPDATE = {'status': 'OK'}
RESPONSE_GENERAL_401 = {
    'code': 'unauthorized',
    'message': 'Not authorized request',
}
RESPONSE_USER_403 = {
    'code': 'FORBIDDEN',
    'message': 'Acl check have not passed',
}
RESPONSE_USER_404 = {'code': 'NOT_FOUND', 'message': 'No such user'}
RESPONSE_USER_LIST_400 = {
    'code': 'INVALID_QUERY',
    'message': 'handle v2_response failed withbad cursor',
}
RESPONSE_USER_CREATE_400_DUPLICATE = {
    'code': 'DUPLICATE_USER_PHONE',
    'message': 'client already has user with same phone',
    'extra': {'conflict_user_id': 'conflict_user_id'},
}
RESPONSE_USER_CREATE_400 = {
    'code': 'VALIDATION_ERROR',
    'message': 'client did not send cost_centers_id whilst having them',
}
RESPONSE_USER_UPDATE_400 = {
    'code': 'VALIDATION_ERROR',
    'message': 'client does not have such cost_centers_id',
}


def mock_users(method, params, json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_GENERAL_401
        return response

    if method == 'GET':
        if 'user_id' in params:
            if params['user_id'] == 'user_id1':
                response.status = 200
                response.json.return_value = USER_RESPONSE
            elif params['user_id'] == 'other_user_id1':
                response.status = 403
                response.json.return_value = RESPONSE_USER_403
            else:
                response.status = 404
                response.json.return_value = RESPONSE_USER_404
        else:
            if params.get('cursor') == 'invalid_cursor':
                response.status = 400
                response.json.return_value = RESPONSE_USER_LIST_400
            elif params.get('cursor') == 'other_cursor':
                response.status = 403
                response.json.return_value = RESPONSE_USER_403
            else:
                items = [USER_RESPONSE, USER_2, USER_3]
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
    elif method == 'POST':
        if json['phone'] == 'other_phone':
            response.status = 400
            response.json.return_value = RESPONSE_USER_CREATE_400_DUPLICATE
        elif json['fullname'] == 'fullname5':
            response.status = 400
            response.json.return_value = RESPONSE_USER_CREATE_400
        elif json.get('cost_centers_id') == 'other_cost_centers_id1':
            response.status = 403
            response.json.return_value = RESPONSE_USER_403
        else:
            response.status = 200
            response.json.return_value = {'id': 'user_id4'}
    elif method == 'PUT':
        if json.get('cost_centers_id') == 'invalid_cost_centers_id1':
            response.status = 400
            response.json.return_value = RESPONSE_USER_UPDATE_400
        elif params['user_id'] == 'other_user_id1':
            response.status = 403
            response.json.return_value = RESPONSE_USER_403
        elif params['user_id'] == 'invalid_user_id1':
            response.status = 404
            response.json.return_value = RESPONSE_USER_404
        else:
            response.status = 200
            response.json.return_value = USER_SUCCESS_UPDATE
    else:
        response.status = 500

    return response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'user_id', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'user_id1',
            USER_RESPONSE,
            id='200 success',
        ),
        pytest.param(
            'invalid_token',
            'user_id1',
            RESPONSE_GENERAL_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'other_user_id1',
            RESPONSE_USER_403,
            id='403 Acl check have not passed',
        ),
        pytest.param(
            'valid_token',
            'user_invalid',
            RESPONSE_USER_404,
            id='404 not such user',
        ),
    ],
)
async def test_user_get(
    token: str,
    user_id: str,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        user_manager = UserManager(client)
        try:
            resp = await user_manager.get(user_id)
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
                'items': [USER_RESPONSE, USER_2, USER_3],
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
                'items': [USER_RESPONSE, USER_2],
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
                'items': [USER_2, USER_3],
                'limit': 2,
                'total_amount': 3,
                'cursor': 'cursor',
                'next_cursor': 'next_cursor2',
            },
            id='200 success with cursor',
        ),
        pytest.param(
            'valid_token',
            {'limit': 1, 'cursor': 'cursor'},
            {
                'items': [USER_2],
                'limit': 1,
                'total_amount': 3,
                'cursor': 'cursor',
                'next_cursor': 'next_cursor2',
            },
            id='200 success with limit and cursor',
        ),
        pytest.param(
            'valid_token',
            {'limit': 'abc'},
            "Invalid value for limit: 'abc' is not instance of int",
            id='400 invalid params limit',
        ),
        pytest.param(
            'valid_token',
            {'cursor': 'invalid_cursor'},
            RESPONSE_USER_LIST_400,
            id='400 invalid params cursor',
        ),
        pytest.param(
            'invalid_token',
            {'limit': 10},
            RESPONSE_GENERAL_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            {'cursor': 'other_cursor'},
            RESPONSE_USER_403,
            id='403 Acl check have not passed',
        ),
    ],
)
async def test_users_list(
    token: str,
    params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        user_manager = UserManager(client)
        try:
            resp = await user_manager.list(**params)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
        except ValidationError as validation_error:
            assert validation_error.args[0] == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'user_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            BASE_USER_REQUEST,
            {'id': 'user_id4'},
            id='200 success without cost_centers_id',
        ),
        pytest.param(
            'valid_token',
            {**BASE_USER_REQUEST, 'cost_centers_id': 'cost_centers_id1'},
            {'id': 'user_id4'},
            id='200 success with cost_centers_id',
        ),
        pytest.param(
            'valid_token',
            {**BASE_USER_REQUEST, 'fullname': 'fullname5'},
            RESPONSE_USER_CREATE_400,
            id='400 validation error without cost_centers_id',
        ),
        pytest.param(
            'valid_token',
            {**BASE_USER_REQUEST, 'phone': 'other_phone'},
            RESPONSE_USER_CREATE_400_DUPLICATE,
            id='400 duplicate user phone',
        ),
        pytest.param(
            'invalid_token',
            BASE_USER_REQUEST,
            RESPONSE_GENERAL_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            {**BASE_USER_REQUEST, 'cost_centers_id': 'other_cost_centers_id1'},
            RESPONSE_USER_403,
            id='403 Acl check have not passed',
        ),
    ],
)
async def test_user_create(
    token: str,
    user_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        user_manager = UserManager(client)
        user = User(**user_params)
        try:
            resp = await user_manager.create(user)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'user_id', 'user_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'user_id1',
            BASE_USER_REQUEST,
            USER_SUCCESS_UPDATE,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            'user_id1',
            {
                **BASE_USER_REQUEST,
                'cost_centers_id': 'invalid_cost_centers_id1',
            },
            RESPONSE_USER_UPDATE_400,
            id='400 validation error invalid cost_centers_id',
        ),
        pytest.param(
            'invalid_token',
            'user_id1',
            BASE_USER_REQUEST,
            RESPONSE_GENERAL_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'other_user_id1',
            {**BASE_USER_REQUEST, 'cost_centers_id': 'other_cost_centers_id1'},
            RESPONSE_USER_403,
            id='403 Acl check have not passed',
        ),
        pytest.param(
            'valid_token',
            'invalid_user_id1',
            {**BASE_USER_REQUEST, 'cost_centers_id': 'other_cost_centers_id1'},
            RESPONSE_USER_404,
            id='404 not such user',
        ),
    ],
)
async def test_user_update(
    token: str,
    user_id: str,
    user_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        user_manager = UserManager(client)
        user = User(**user_params)
        try:
            resp = await user_manager.update(user_id=user_id, user=user)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
