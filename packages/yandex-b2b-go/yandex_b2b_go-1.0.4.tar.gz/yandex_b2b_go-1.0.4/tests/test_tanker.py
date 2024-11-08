from typing import Any, Dict
from unittest.mock import AsyncMock

import pytest

from yandex_b2b_go import Client, TankerManager
from yandex_b2b_go.errors import ApiError

TANKER_1 = {
    'id': 'order_id1',
    'user_id': 'user_id1',
    'client_id': 'client_id1',
    'created_at': '2024-09-01T01:00:00.000001',
    'closed_at': '2024-09-01T01:05:00.000001',
    'fuel_type': 'a92',
    'final_price': '236.4',
    'liters_filled': '5.0',
    'station_location': [37.8636, 51.341842],
}
TANKER_2 = {
    'id': 'order_id2',
    'user_id': 'user_id1',
    'client_id': 'client_id1',
    'created_at': '2024-09-01T02:00:00.000001',
    'closed_at': '2024-09-01T02:05:00.000001',
    'fuel_type': 'a95',
    'final_price': '236.4',
    'liters_filled': '10.0',
    'station_location': [37.8636, 51.341842],
}
TANKER_3 = {
    'id': 'order_id3',
    'user_id': 'user_id2',
    'client_id': 'client_id1',
    'created_at': '2024-09-01T03:00:00.000001',
    'closed_at': '2024-09-01T03:05:00.000001',
    'fuel_type': 'a95',
    'final_price': '236.4',
    'liters_filled': '10.0',
    'station_location': [37.8636, 51.341842],
}
RESPONSE_400 = {
    'code': 'REQUEST_VALIDATION_ERROR',
    'message': 'Some parameters are invalid',
}
RESPONSE_401 = {'code': 'unauthorized', 'message': 'Not authorized request'}
RESPONSE_403 = {'code': 'FORBIDDEN', 'message': 'Acl check have not passed'}


def mock_tanker_order_list(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params.get('user_id') == 'other_user_id':
        response.status = 403
        response.json.return_value = RESPONSE_403
    elif params.get('since_datetime') == 'invalid_datetime':
        response.status = 400
        response.json.return_value = RESPONSE_400
    else:
        items = [TANKER_1, TANKER_2, TANKER_3]
        if 'user_id' in params:
            items = [tanker for tanker in items if tanker['user_id'] == params['user_id']]

        if 'since_datetime' in params:
            items = [tanker for tanker in items if tanker['closed_at'] >= params['since_datetime']]

        if 'till_datetime' in params:
            items = [tanker for tanker in items if tanker['closed_at'] < params['till_datetime']]

        if 'limit' in params:
            items = items[: int(params['limit'])]

        response.status = 200
        return_value = {'orders': items}

        if items:
            return_value['last_closed_at'] = max([tanker['closed_at'] for tanker in items])

        response.json.return_value = return_value

    return response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            {},
            {
                'orders': [TANKER_1, TANKER_2, TANKER_3],
                'last_closed_at': '2024-09-01T03:05:00.000001',
            },
            id='200 success without params',
        ),
        pytest.param(
            'valid_token',
            {'limit': 1},
            {
                'orders': [TANKER_1],
                'last_closed_at': '2024-09-01T01:05:00.000001',
            },
            id='200 success with limit',
        ),
        pytest.param(
            'valid_token',
            {'user_id': 'user_id1'},
            {
                'orders': [TANKER_1, TANKER_2],
                'last_closed_at': '2024-09-01T02:05:00.000001',
            },
            id='200 success with user_id',
        ),
        pytest.param(
            'valid_token',
            {'since_datetime': '2024-09-01T02:02:00.000001'},
            {
                'orders': [TANKER_2, TANKER_3],
                'last_closed_at': '2024-09-01T03:05:00.000001',
            },
            id='200 success with since_datetime',
        ),
        pytest.param(
            'valid_token',
            {'till_datetime': '2024-09-01T03:00:00.000001'},
            {
                'orders': [TANKER_1, TANKER_2],
                'last_closed_at': '2024-09-01T02:05:00.000001',
            },
            id='200 success with till_datetime',
        ),
        pytest.param(
            'valid_token',
            {'since_datetime': 'invalid_datetime'},
            RESPONSE_400,
            id='400',
        ),
        pytest.param('invalid_token', {}, RESPONSE_401, id='401 unauthorized'),
        pytest.param(
            'valid_token',
            {'user_id': 'other_user_id'},
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
    ],
)
async def test_tanker_orders(
    token: str,
    params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        tanker_manager = TankerManager(client)
        try:
            resp = await tanker_manager.order.list(**params)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
