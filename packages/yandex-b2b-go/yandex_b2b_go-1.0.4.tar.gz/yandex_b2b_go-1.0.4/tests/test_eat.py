from typing import Any, Dict, List
from unittest.mock import AsyncMock

import pytest

from yandex_b2b_go import Client, EatManager
from yandex_b2b_go.errors import ApiError
from yandex_b2b_go.typing import EatsOrdersListRequest, SortingOrder

EAT_1 = {
    'id': 'order_id1',
    'user_id': 'user_id1',
    'status': 'delivered',
    'created_at': '2024-09-01T10:00:00.000',
    'closed_at': '2024-09-01T10:00:00.000',
    'restaurant_name': 'restaurant_name1',
    'department_id': 'department_id1',
    'destination_address': 'destination_address1',
    'order_calculation': [
        {
            'name': 'order_calculation_name_1',
            'cost': '1000.0000',
            'vat': '200.0000',
            'cost_with_vat': '1200.0000',
            'count': 1,
        },
        {
            'name': 'order_calculation_name_2',
            'cost': '1000.0000',
            'vat': '200.0000',
            'cost_with_vat': '1200.0000',
            'count': 1,
            'modifiers': [
                {
                    'name': 'modifiers_name_1',
                    'cost': '1000.0000',
                    'vat': '200.0000',
                    'cost_with_vat': '1200.0000',
                    'count': 1,
                },
            ],
        },
    ],
    'final_cost': '1000.0000',
    'vat': '200.0000',
    'final_cost_with_vat': '1200.0000',
    'corp_discount': {
        'sum': '200.0000',
        'vat': '40.0000',
        'with_vat': '240.0000',
        'sales_tax': '25.0000',
        'total': '265.0000',
    },
    'corp_discount_reverted': False,
    'currency': 'RUB',
    'eats_cost_centers': [
        {'id': 'id_cost_center1', 'title': 'title1', 'value': 'value1'},
        {'id': 'id_cost_center2', 'title': 'title2', 'value': 'value2'},
    ],
    'transactions_total': {'sum': '1000.0000', 'with_vat': '1200.0000'},
}
EAT_2 = {
    **EAT_1,
    'id': 'order_id2',
    'user_id': 'user_id2',
    'created_at': '2024-09-01T11:00:00.000',
    'closed_at': '2024-09-01T11:00:00.000',
}
EAT_3 = {
    **EAT_1,
    'id': 'order_id3',
    'user_id': 'user_id3',
    'created_at': '2024-09-01T12:00:00.000',
    'closed_at': '2024-09-01T12:00:00.000',
}
RESPONSE_400 = {
    'code': 'wrong-parameters',
    'message': 'Since date should be earlier than till date',
}
RESPONSE_401 = {'code': 'unauthorized', 'message': 'Not authorized request'}
RESPONSE_403 = {'code': 'FORBIDDEN', 'message': 'Acl check have not passed'}


def mock_eat_order_list(params, json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if 'since_datetime' in params and 'till_datetime' in params and params['since_datetime'] > params['till_datetime']:
        response.status = 400
        response.json.return_value = RESPONSE_400
    elif 'other_user_id' in json['user_ids']:
        response.status = 403
        response.json.return_value = RESPONSE_403
    else:
        items = [EAT_3, EAT_2, EAT_1]
        return_value = {'sorting_order': 'desc', 'limit': 150, 'cursor': ''}
        items = [item for item in items if item['user_id'] in json['user_ids']]
        if 'cursor' in params:
            items = items[1:]
            return_value['cursor'] = 'cursor1'
        if 'since_datetime' in params:
            items = [item for item in items if item['created_at'] >= params['since_datetime']]
        if 'till_datetime' in params:
            items = [item for item in items if item['created_at'] < params['till_datetime']]
        if 'limit' in params:
            limit = int(params['limit'])
            items = items[:limit]
            return_value['limit'] = limit
            return_value['cursor'] = 'cursor'
        if 'sorting_order' in params:
            return_value['sorting_order'] = params['sorting_order']
            items = sorted(items, key=lambda x: x['created_at'])

        response.status = 200
        return_value['orders'] = items
        response.json.return_value = return_value
    return response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'params', 'user_ids', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            {},
            ['user_id1', 'user_id2', 'user_id3'],
            {
                'orders': [EAT_3, EAT_2, EAT_1],
                'limit': 150,
                'cursor': '',
                'sorting_order': 'desc',
            },
            id='200 success without params',
        ),
        pytest.param(
            'valid_token',
            {'limit': 2},
            ['user_id1', 'user_id2', 'user_id3'],
            {
                'orders': [EAT_3, EAT_2],
                'limit': 2,
                'cursor': 'cursor',
                'sorting_order': 'desc',
            },
            id='200 success with limit',
        ),
        pytest.param(
            'valid_token',
            {'cursor': 'cursor'},
            ['user_id1', 'user_id2', 'user_id3'],
            {
                'orders': [EAT_2, EAT_1],
                'limit': 150,
                'cursor': 'cursor1',
                'sorting_order': 'desc',
            },
            id='200 success with cursor',
        ),
        pytest.param(
            'valid_token',
            {
                'since_datetime': '2024-09-01T10:30:00.000',
                'till_datetime': '2024-09-01T11:30:00.000',
            },
            ['user_id1', 'user_id2', 'user_id3'],
            {
                'orders': [EAT_2],
                'limit': 150,
                'cursor': '',
                'sorting_order': 'desc',
            },
            id='200 success with since_datetime and till_datetime',
        ),
        pytest.param(
            'valid_token',
            {'sorting_order': SortingOrder.asc},
            ['user_id1', 'user_id2', 'user_id3'],
            {
                'orders': [EAT_1, EAT_2, EAT_3],
                'limit': 150,
                'cursor': '',
                'sorting_order': 'asc',
            },
            id='200 success with order',
        ),
        pytest.param(
            'valid_token',
            {},
            ['user_id2', 'user_id3'],
            {
                'orders': [EAT_3, EAT_2],
                'limit': 150,
                'cursor': '',
                'sorting_order': 'desc',
            },
            id='200 success with user_id',
        ),
        pytest.param(
            'valid_token',
            {
                'since_datetime': '2024-09-01T11:30:00.000',
                'till_datetime': '2024-09-01T10:30:00.000',
            },
            ['user_id1'],
            RESPONSE_400,
            id='400 wrong parameters',
        ),
        pytest.param(
            'invalid_token',
            {},
            ['user_id1'],
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            {},
            ['other_user_id'],
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
    ],
)
async def test_eat_orders_list(
    token: str,
    params: Dict[str, Any],
    user_ids: List[str],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        eat_manager = EatManager(client)
        try:
            resp = await eat_manager.order.list(
                user_ids=EatsOrdersListRequest(user_ids=user_ids),
                **params,
            )
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
