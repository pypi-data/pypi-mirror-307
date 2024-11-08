from typing import Any, Dict
from unittest.mock import AsyncMock

import pytest

from yandex_b2b_go import BudgetManager, Client
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.typing import (
    BudgetLimitTaxiRequest,
    GeoRestriction,
    MeasurePeriod,
    OrdersCostTaxiLimit,
    Service,
    TaxiLimits,
)

BASE_LIMIT = {
    'title': 'Такси - 5000',
    'service': 'taxi',
    'counters': {'users': 3},
    'is_default': True,
    'limits': {
        'orders_cost': {
            'value': 5000.0,
            'period': 'month',
        },
        'orders_amount': {
            'value': 5000.0,
            'period': 'month',
        },
    },
    'categories': ['comfortplus'],
    'geo_restrictions': [
        {'source': '50d17034e0ebаааd952d2dad4bbbabcf', 'destination': '62b9160b33ааа4548e11bbb736bde8b'}
    ],
    'time_restrictions': [
        {
            'type': 'weekly_date',
            'start_time': '00:59:00',
            'end_time': '02:00:00',
            'days': ['mo', 'tu', 'we', 'th', 'fr', 'sa', 'su'],
        }
    ],
}
LIMIT_1 = {
    **BASE_LIMIT,
    'id': 'limit_id1',
    'client_id': 'client_id1',
    'department_id': 'department_id1',
}
LIMIT_2 = {
    **BASE_LIMIT,
    'id': 'limit_id2',
    'client_id': 'client_id2',
    'department_id': 'department_id2',
}
LIMIT_3 = {
    **BASE_LIMIT,
    'id': 'limit_id3',
    'client_id': 'client_id3',
    'department_id': 'department_id3',
}
BASE_BUDGET_LIMIT_REQUEST = {
    'client_id': 'client_id1',
    'title': 'Такси - 5000',
    'service': Service.taxi,
    'categories': ['child_tariff', 'cargo', 'business'],
    'limits': TaxiLimits(orders_cost=OrdersCostTaxiLimit(value=10.0, period=MeasurePeriod.day)),
}
RESPONSE_GENERAL_401 = {
    'code': 'unauthorized',
    'message': 'Not authorized request',
}
RESPONSE_BUDGET_LIMIT_LIST_400 = {
    'code': 'REQUEST_VALIDATION_ERROR',
    'message': 'Some parameters are invalid',
}
RESPONSE_BUDGET_LIMIT_UPDATE_400_USER_NOT_FOUND = {
    'code': 'NOT_FOUND',
    'message': 'Not found',
}
BUDGET_LIMIT_SUCCESS_UPDATE = {'id': 'limit_id1'}
RESPONSE_BUDGET_LIMIT_UPDATE_400 = {
    'code': 'REQUEST_VALIDATION_ERROR',
    'message': 'Some parameters are invalid',
}


def mock_budget_limit_list(method, params, json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_GENERAL_401
        return response

    if method == 'GET':
        items = [LIMIT_1, LIMIT_2, LIMIT_3]
        return_value = {'total_amount': len(items)}
        if 'department_id' in params:
            items = [item for item in items if item['department_id'] == params['department_id']]
        if 'offset' in params:
            offset = int(params['offset'])
            items = items[offset:]
        if 'limit' in params:
            limit = int(params['limit'])
            items = items[:limit]
        return_value['items'] = items
        return_value['limit'] = len(items)
        return_value['offset'] = int(params.get('offset', '0'))
        response.status = 200
        response.json.return_value = return_value
    else:
        response.status = 500

    return response


def mock_budget_limit_update(method, params, json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_GENERAL_401
        return response
    if method == 'PUT':
        if params['user_id'] == 'invalid_user_id1':
            response.status = 400
            response.json.return_value = RESPONSE_BUDGET_LIMIT_UPDATE_400_USER_NOT_FOUND
        elif json.get('geo_restrictions') == [{'source': 'invalid_geo_restrictions'}]:
            response.status = 400
            response.json.return_value = RESPONSE_BUDGET_LIMIT_UPDATE_400
        else:
            response.status = 200
            response.json.return_value = BUDGET_LIMIT_SUCCESS_UPDATE
    else:
        response.status = 500

    return response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            {},
            {
                'items': [LIMIT_1, LIMIT_2, LIMIT_3],
                'limit': 3,
                'total_amount': 3,
                'offset': 0,
            },
            id='200 response',
        ),
        pytest.param(
            'valid_token',
            {'department_id': 'other_department_id'},
            {'items': [], 'limit': 0, 'total_amount': 3, 'offset': 0},
            id='200 other_department_id',
        ),
        pytest.param(
            'valid_token',
            {'department_id': 'department_id2'},
            {'items': [LIMIT_2], 'limit': 1, 'total_amount': 3, 'offset': 0},
            id='200 exists department_id',
        ),
        pytest.param(
            'valid_token',
            {'limit': 2},
            {
                'items': [LIMIT_1, LIMIT_2],
                'limit': 2,
                'total_amount': 3,
                'offset': 0,
            },
            id='200 with limit',
        ),
        pytest.param(
            'valid_token',
            {'offset': 1},
            {
                'items': [LIMIT_2, LIMIT_3],
                'limit': 2,
                'total_amount': 3,
                'offset': 1,
            },
            id='200 with offset',
        ),
        pytest.param(
            'valid_token',
            {'offset': 1, 'limit': 1},
            {'items': [LIMIT_2], 'limit': 1, 'total_amount': 3, 'offset': 1},
            id='200 with limit and offset',
        ),
        pytest.param(
            'valid_token',
            {'limit': 'abc'},
            "Invalid value for limit: 'abc' is not instance of int",
            id='400 invalid params limit',
        ),
        pytest.param(
            'valid_token',
            {'offset': 'abc'},
            "Invalid value for offset: 'abc' is not instance of int",
            id='400 invalid params offset',
        ),
        pytest.param(
            'invalid_token',
            {},
            RESPONSE_GENERAL_401,
            id='401 unauthorized',
        ),
    ],
)
async def test_budget_limit_list(
    token: str,
    params: dict,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        budget_manager = BudgetManager(client)
        try:
            resp = await budget_manager.limit.list(**params)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
        except ValidationError as validation_error:
            assert validation_error.args[0] == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'user_id', 'limit_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'user_id1',
            BASE_BUDGET_LIMIT_REQUEST,
            BUDGET_LIMIT_SUCCESS_UPDATE,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            'user_id1',
            {
                **BASE_BUDGET_LIMIT_REQUEST,
                'geo_restrictions': [GeoRestriction(source='invalid_geo_restrictions')],
            },
            RESPONSE_BUDGET_LIMIT_UPDATE_400,
            id='400 validation error invalid geo_restrictions',
        ),
        pytest.param(
            'invalid_token',
            'user_id1',
            BASE_BUDGET_LIMIT_REQUEST,
            RESPONSE_GENERAL_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'invalid_user_id1',
            BASE_BUDGET_LIMIT_REQUEST,
            RESPONSE_BUDGET_LIMIT_UPDATE_400_USER_NOT_FOUND,
            id='400 not such user',
        ),
    ],
)
async def test_budget_limit_update(
    token: str,
    user_id: str,
    limit_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        budget_manager = BudgetManager(client)
        limit = BudgetLimitTaxiRequest(**limit_params)
        try:
            resp = await budget_manager.limit.update(
                user_id=user_id,
                budget_limit=limit,
            )
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
