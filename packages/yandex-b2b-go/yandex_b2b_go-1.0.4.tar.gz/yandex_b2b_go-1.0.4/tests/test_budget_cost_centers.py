from unittest.mock import AsyncMock

import pytest

from yandex_b2b_go import BudgetManager, Client
from yandex_b2b_go.errors import ApiError, ValidationError

COST_CENTER_1 = {
    'id': 'cost_center1',
    'name': 'Test1',
    'default': True,
    'field_settings': [
        {
            'id': 'settings_id1',
            'hidden': False,
            'title': 'Центр затрат',
            'required': True,
            'services': ['taxi'],
            'format': 'select',
            'values': ['командировка', 'в офис'],
        },
    ],
}
COST_CENTER_2 = {
    'id': 'cost_center2',
    'name': 'Test2',
    'default': True,
    'field_settings': [
        {
            'id': 'settings_id2',
            'hidden': False,
            'title': 'Центр затрат',
            'required': True,
            'services': ['taxi'],
            'format': 'select',
            'values': ['в центральный офис', 'аэропорт'],
        },
    ],
}
COST_CENTER_3 = {
    'id': 'cost_center3',
    'name': 'Test3',
    'default': True,
    'field_settings': [
        {
            'id': 'settings_id3',
            'hidden': False,
            'title': 'Центр затрат',
            'required': True,
            'services': ['taxi'],
            'format': 'select',
            'values': ['вокзал', 'аэропорт'],
        },
    ],
}
RESPONSE_GENERAL_401 = {
    'code': 'unauthorized',
    'message': 'Not authorized request',
}
RESPONSE_BUDGET_COST_CENTER_LIST_400 = {
    'code': 'REQUEST_VALIDATION_ERROR',
    'message': 'Some parameters are invalid',
}


def mock_budget_cost_center_list(method, params, json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_GENERAL_401
        return response

    if method == 'GET':
        items = [COST_CENTER_1, COST_CENTER_2, COST_CENTER_3]
        return_value = {'total_amount': len(items)}
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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            {},
            {
                'items': [COST_CENTER_1, COST_CENTER_2, COST_CENTER_3],
                'limit': 3,
                'total_amount': 3,
                'offset': 0,
            },
            id='200 success without params',
        ),
        pytest.param(
            'valid_token',
            {'limit': 2},
            {
                'items': [COST_CENTER_1, COST_CENTER_2],
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
                'items': [COST_CENTER_2, COST_CENTER_3],
                'limit': 2,
                'total_amount': 3,
                'offset': 1,
            },
            id='200 success with offset',
        ),
        pytest.param(
            'valid_token',
            {'limit': 1, 'offset': 1},
            {
                'items': [COST_CENTER_2],
                'limit': 1,
                'total_amount': 3,
                'offset': 1,
            },
            id='200 success with limit and offset',
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
            {'limit': 10},
            RESPONSE_GENERAL_401,
            id='401 unauthorized',
        ),
    ],
)
async def test_budget_cost_center_list(
    token: str,
    params: dict,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        budget_manager = BudgetManager(client)
        try:
            resp = await budget_manager.cost_center.list(**params)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
        except ValidationError as validation_error:
            assert validation_error.args[0] == expected_response
