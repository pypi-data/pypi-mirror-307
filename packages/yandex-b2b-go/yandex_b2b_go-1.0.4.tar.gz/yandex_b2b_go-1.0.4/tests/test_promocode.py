import uuid
from typing import Any, Dict
from unittest.mock import AsyncMock

import pytest

from yandex_b2b_go import Client, PromocodeManager
from yandex_b2b_go.errors import ApiError
from yandex_b2b_go.typing import (
    BankName,
    Promocode,
    PromocodeGeoRestrictions,
    PromocodeGeoRestrictionsPoint,
    PromocodeOrderService,
)

PROMOCODE_REQUEST = {
    'name': 'promocode order name',
    'value': 500,
    'count': 100,
    'active_until': '2025-09-31',
    'active_from': '2024-09-31',
    'max_usages_count': 10,
    'service': PromocodeOrderService.taxi,
    'bin_ranges': [['220000', '220500']],
    'bank_name': BankName(ru='Название банка', en='Bank Name'),
    'geo_restrictions': [
        PromocodeGeoRestrictions(
            max_intermediate_points=2,
            source=PromocodeGeoRestrictionsPoint(
                geo_restriction_id='geo_restriction_id1',
            ),
            destination=PromocodeGeoRestrictionsPoint(
                geo_restriction_id='geo_restriction_id2',
            ),
        ),
    ],
    'classes': ['econom', 'business', 'comfortplus', 'vip'],
}
PROMOCODE_1 = {
    'order_id': 'order_id1',
    'count': 100,
    'value': 500,
    'status': 'creation_success',
    'active_until': '2025-09-31',
    'pricing': {
        'cost': '1000.00',
        'cost_with_vat': '1200.00',
        'vat': '200.00',
        'currency': 'RUB',
    },
    'service': 'taxi',
    'bin_ranges': [['220000', '220500']],
    'classes': ['econom', 'business', 'comfortplus', 'vip'],
    'bank_name': {'ru': 'Название банка', 'en': 'Bank Name'},
    'geo_restrictions': [
        {
            'max_intermediate_points': 2,
            'source': {
                'corp_geo_id': 'corp_geo_id1',
                'name': 'name1',
                'geo': {'radius': 100.00, 'center': [54.3, 37.5]},
            },
            'destination': {
                'corp_geo_id': 'corp_geo_id2',
                'name': 'name2',
                'geo': {'radius': 100.00, 'center': [54.3, 37.5]},
            },
        },
    ],
}
PROMOCODE_2 = {**PROMOCODE_1, 'order_id': 'order_id2'}
PROMOCODE_3 = {**PROMOCODE_1, 'order_id': 'order_id3'}
CODE_1 = {
    'id': 'code_id1',
    'code': 'code',
    'status': 'status',
    'usages': [
        {'used_at': '2024-09-10T10:00:00.000'},
        {'used_at': '2024-09-13T12:00:00.000'},
    ],
}
CODE_2 = {**CODE_1, 'id': 'code_id2'}
CODE_3 = {**CODE_1, 'id': 'code_id2'}
RESPONSE_200 = {'order_id': 'order_id1'}
RESPONSE_CANCEL_200 = {'status': 'cancelled'}
RESPONSE_400 = {
    'code': 'BAD_REQUEST',
    'message': 'limitation of the minimum nominal value in an order. expect more or equal 100',
}
RESPONSE_CANCEL_400 = {
    'code': 'BAD_REQUEST',
    'message': 'wrong id format, expect uuid v4',
}
RESPONSE_LIST_400 = {'message': 'WRONG_CURSOR', 'code': '400'}
RESPONSE_401 = {'code': 'unauthorized', 'message': 'Not authorized request'}
RESPONSE_404 = {'code': 'NOT_FOUND', 'message': 'order not found'}
RESPONSE_GET_404 = {'message': 'not found', 'code': '404'}


def mock_promocode_create(json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if json['count'] < 100:
        response.status = 400
        response.json.return_value = RESPONSE_400
    else:
        response.status = 200
        response.json.return_value = RESPONSE_200

    return response


def mock_promocode_cancel(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params['order_id'] == 'wrong_order_id1':
        response.status = 400
        response.json.return_value = RESPONSE_CANCEL_400
    elif params['order_id'] == 'invalid_order_id':
        response.status = 400
        response.json.return_value = RESPONSE_404
    else:
        response.status = 200
        response.json.return_value = RESPONSE_CANCEL_200

    return response


def mock_promocode_list(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params.get('cursor') == 'invalid_cursor':
        response.status = 400
        response.json.return_value = RESPONSE_LIST_400
    else:
        items = [PROMOCODE_1, PROMOCODE_2, PROMOCODE_3]
        return_value = {}
        if 'cursor' in params:
            items = items[1:]
            return_value['next_cursor'] = 'next_cursor'
        limit = int(params['limit'])
        items = items[:limit]
        return_value['orders'] = items
        response.status = 200
        response.json.return_value = return_value

    return response


def mock_promocode_get(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params['order_id'] == 'invalid_order_id':
        response.status = 404
        response.json.return_value = RESPONSE_GET_404
    else:
        response.status = 200
        response.json.return_value = PROMOCODE_1

    return response


def mock_promocode_code_list(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params.get('cursor') == 'invalid_cursor':
        response.status = 400
        response.json.return_value = RESPONSE_LIST_400
    elif params['order_id'] == 'invalid_order_id1':
        response.status = 404
        response.json.return_value = RESPONSE_GET_404
    else:
        items = [CODE_1, CODE_2, CODE_3]
        return_value = {}
        if 'cursor' in params:
            items = items[1:]
            return_value['next_cursor'] = 'next_cursor'
        if 'limit' in params:
            limit = int(params['limit'])
            items = items[:limit]
        return_value['codes'] = items
        response.status = 200
        response.json.return_value = return_value

    return response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'promo_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            PROMOCODE_REQUEST,
            RESPONSE_200,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            {**PROMOCODE_REQUEST, 'count': 5},
            RESPONSE_400,
            id='400 invalid count',
        ),
        pytest.param(
            'invalid_token',
            PROMOCODE_REQUEST,
            RESPONSE_401,
            id='401 unauthorized',
        ),
    ],
)
async def test_promocode_create(
    token: str,
    promo_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        promocode_manager = PromocodeManager(client)
        try:
            promocode = Promocode(**promo_params)
            resp = await promocode_manager.order.create(
                promocode=promocode,
                idempotency_token=uuid.uuid4(),
            )
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'order_id', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'order_id1',
            RESPONSE_CANCEL_200,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            'wrong_order_id1',
            RESPONSE_CANCEL_400,
            id='400 invalid order_id',
        ),
        pytest.param(
            'invalid_token',
            'order_id1',
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'invalid_order_id',
            RESPONSE_404,
            id='404 invalid count',
        ),
    ],
)
async def test_promocode_cancel(
    token: str,
    order_id: str,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        promocode_manager = PromocodeManager(client)
        try:
            resp = await promocode_manager.order.cancel(order_id=order_id)
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
            {'limit': 10},
            {'orders': [PROMOCODE_1, PROMOCODE_2, PROMOCODE_3]},
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            {'limit': 2},
            {'orders': [PROMOCODE_1, PROMOCODE_2]},
            id='200 success with small limit',
        ),
        pytest.param(
            'valid_token',
            {'limit': 10, 'cursor': 'cursor'},
            {
                'orders': [PROMOCODE_2, PROMOCODE_3],
                'next_cursor': 'next_cursor',
            },
            id='200 success with cursor',
        ),
        pytest.param(
            'valid_token',
            {'limit': 10, 'cursor': 'invalid_cursor'},
            RESPONSE_LIST_400,
            id='400 invalid cursor',
        ),
        pytest.param(
            'invalid_token',
            {'limit': 10},
            RESPONSE_401,
            id='401 unauthorized',
        ),
    ],
)
async def test_promocode_list(
    token: str,
    params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        promocode_manager = PromocodeManager(client)
        try:
            resp = await promocode_manager.order.list(**params)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'order_id', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'order_id1',
            PROMOCODE_1,
            id='200 success',
        ),
        pytest.param(
            'invalid_token',
            'order_id1',
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'invalid_order_id',
            RESPONSE_GET_404,
            id='404 nof found',
        ),
    ],
)
async def test_promocode_get(
    token: str,
    order_id: str,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        promocode_manager = PromocodeManager(client)
        try:
            resp = await promocode_manager.order.get(order_id=order_id)
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
            {'order_id': 'order_id1'},
            {'codes': [CODE_1, CODE_2, CODE_3]},
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            {'order_id': 'order_id1', 'limit': 2},
            {'codes': [CODE_1, CODE_2]},
            id='200 success with small limit',
        ),
        pytest.param(
            'valid_token',
            {'order_id': 'order_id1', 'cursor': 'cursor'},
            {'codes': [CODE_2, CODE_3], 'next_cursor': 'next_cursor'},
            id='200 success with cursor',
        ),
        pytest.param(
            'valid_token',
            {'order_id': 'order_id1', 'limit': 10, 'cursor': 'invalid_cursor'},
            RESPONSE_LIST_400,
            id='400 invalid cursor',
        ),
        pytest.param(
            'invalid_token',
            {'order_id': 'order_id1', 'limit': 10},
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            {'order_id': 'invalid_order_id1'},
            RESPONSE_GET_404,
            id='404 nof found',
        ),
    ],
)
async def test_promocode_code_list(
    token: str,
    params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        promocode_manager = PromocodeManager(client)
        try:
            resp = await promocode_manager.order.code.list(**params)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
