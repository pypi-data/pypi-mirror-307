import uuid
from typing import Any, Dict
from unittest.mock import AsyncMock

import pytest

from yandex_b2b_go import Client, TaxiManager
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.typing import (
    Feedback,
    Order,
    OrderRequest,
    OrdersCancelRequest,
    RoutePoint,
    TaxiOrderCancelRulesState,
    TaxiOrderDestinationsUpdateRequest,
)

BASE_ORDER_CREATE_REQUEST = {
    'route': [
        RoutePoint(geopoint=[37.562394, 55.792993], fullname='Москва'),
        RoutePoint(geopoint=[37.609479, 55.746943], fullname='Москва'),
    ],
    'user_id': 'user_id',
    'class_tariff': 'econom',
}
ORDER_1 = {
    'id': 'order_id1',
    'user_id': 'user_id1',
    'status': 'driving',
    'class': 'econom',
    'source': {'fullname': 'Москва, Зоологическая улица, 28с1', 'geopoint': [37.58508433837886, 55.76631637044709]},
    'destination': {'fullname': 'Москва, улица Годовикова, 9с1', 'geopoint': [37.62525310058589, 55.80713497241309]},
    'due_date': '2023-02-10T10:54:55+03:00',
}
ORDER_2 = {**ORDER_1, 'id': 'order_id2'}
ORDER_3 = {**ORDER_1, 'id': 'order_id3'}


RESPONSE_401 = {'code': 'unauthorized', 'message': 'Not authorized request'}
RESPONSE_403 = {'code': 'FORBIDDEN', 'message': 'Acl check have not passed'}
RESPONSE_404 = {'code': 'USER_NOT_FOUND', 'message': 'Not found'}
RESPONSE_GET_404 = {'code': 'NOT_FOUND', 'message': 'order not found'}
RESPONSE_400 = {
    'code': 'REQUEST_VALIDATION_ERROR',
    'message': 'Some parameters are invalid',
}
RESPONSE_ORDER_CREATE_200 = {'order_id': 'order_id1'}
RESPONSE_CANCEL_200 = {'status': 'cancelled'}
RESPONSE_ACTIVE_ORDER_200 = {
    'items': [
        {'id': 'order_id1', 'status': 'expired'},
        {'id': 'order_id2', 'status': 'complete'},
        {'id': 'order_id3', 'status': 'driving'},
    ]
}
RESPONSE_ROUTESTATS_GET_200 = {
    'offer': 'offer_id',
    'service_levels': [
        {
            'class': 'comfortplus',
            'is_fixed_price': True,
            'price': '290 руб.',
            'details_tariff': [
                {'type': 'price', 'value': 'от 219 руб.'},
                {'type': 'icon', 'value': 'от 219 руб.'},
                {'type': 'comment', 'value': 'включено 5 мин., далее 14,3 руб./мин.'},
                {'type': 'comment', 'value': 'включено 0 км, далее 14,3 руб./км'},
            ],
        },
    ],
}
ROUTESTATS_REQUEST = {
    'route': [[37.593983, 55.738759], [37.609479, 55.746943]],
    'user_id': 'user_id1',
}
RESPONSE_DESTINATIONS_UPDATE_200 = {
    'changed_destinations': [
        {
            'fullname': 'Москва, Гоголевский бульвар, 31с1',
            'geopoint': [37.600296, 55.750379],
            'country': 'Россия',
            'locality': 'Москва',
            'premisenumber': '31с1',
            'thoroughfare': 'Гоголевский бульвар',
        },
    ]
}
DESTINATIONS_UPDATE_REQUEST = {
    'created_time': '2022-02-09T22:50:34',
    'destinations': [
        RoutePoint(
            geopoint=[37.600296, 55.750379],
            fullname='Гоголевский бульвар, 31с1',
        ),
    ],
}
RESPONSE_STATUS_GET_200 = {
    'status': 'finished',
    'vehicle': {'location': [55.749884, 37.589688]},
}


def mock_taxi_order_create(json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if json['user_id'] == 'invalid_user_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    elif json['class'] != 'econom':
        response.status = 400
        response.json.return_value = RESPONSE_400
    else:
        response.status = 200
        response.json.return_value = RESPONSE_ORDER_CREATE_200

    return response


def mock_taxi_order_get(params, headers, **kwargs):
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
        response.json.return_value = ORDER_1

    return response


def mock_taxi_order_list(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    items = [ORDER_1, ORDER_2, ORDER_3]

    if params.get('offset') == '-5':
        response.status = 400
        response.json.return_value = RESPONSE_400
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


def mock_taxi_order_cancel(json, params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params['order_id'] == 'wrong_order_id1':
        response.status = 400
        response.json.return_value = RESPONSE_400
    elif params['order_id'] == 'invalid_order_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    elif 'state' not in json:
        response.status = 400
        response.json.return_value = RESPONSE_400
    else:
        response.status = 200
        response.json.return_value = RESPONSE_CANCEL_200

    return response


def mock_taxi_active_order_list(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params['user_id'] == 'invalid_user_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    else:
        response.status = 200
        response.json.return_value = RESPONSE_ACTIVE_ORDER_200

    return response


def mock_taxi_order_routestats_get(json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if json['user_id'] == 'invalid_user_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    elif json['route'] == ['a', 'b']:
        response.status = 400
        response.json.return_value = RESPONSE_400
    else:
        response.status = 200
        response.json.return_value = RESPONSE_ROUTESTATS_GET_200

    return response


def mock_taxi_order_feedback_create(json, params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params['order_id'] == 'wrong_order_id1':
        response.status = 400
        response.json.return_value = RESPONSE_400
    elif params['order_id'] == 'invalid_order_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    elif json['rating'] > 5:
        response.status = 400
        response.json.return_value = RESPONSE_400
    else:
        response.status = 200
        response.json.return_value = {}

    return response


def mock_taxi_order_destination_update(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params['order_id'] == 'wrong_order_id1':
        response.status = 400
        response.json.return_value = RESPONSE_400
    elif params['order_id'] == 'invalid_order_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    else:
        response.status = 200
        response.json.return_value = RESPONSE_DESTINATIONS_UPDATE_200

    return response


def mock_taxi_order_status_get(params, headers, **kwargs):
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
        response.json.return_value = RESPONSE_STATUS_GET_200

    return response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'order_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            BASE_ORDER_CREATE_REQUEST,
            RESPONSE_ORDER_CREATE_200,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            {**BASE_ORDER_CREATE_REQUEST, 'class_tariff': 1},
            'Invalid value for class_tariff: 1 is not instance of str',
            id='400 invalid class',
        ),
        pytest.param(
            'valid_token',
            {**BASE_ORDER_CREATE_REQUEST, 'user_id': 'invalid_user_id'},
            RESPONSE_404,
            id='404 user not found',
        ),
        pytest.param(
            'invalid_token',
            BASE_ORDER_CREATE_REQUEST,
            RESPONSE_401,
            id='401 unauthorized',
        ),
    ],
)
async def test_taxi_order_create(
    token: str,
    order_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        taxi_manager = TaxiManager(client)
        try:
            order = Order(**order_params)
            resp = await taxi_manager.order.create(
                order=order,
                idempotency_token=uuid.uuid4(),
            )
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
        except ValidationError as validation_error:
            assert validation_error.args[0] == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'order_id', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'order_id1',
            ORDER_1,
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
async def test_taxi_order_get(
    token: str,
    order_id: str,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        taxi_manager = TaxiManager(client)
        try:
            resp = await taxi_manager.order.get(order_id=order_id)
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
                'items': [ORDER_1, ORDER_2, ORDER_3],
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
                'items': [ORDER_1, ORDER_2],
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
                'items': [ORDER_2, ORDER_3],
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
                'items': [ORDER_2],
                'limit': 1,
                'offset': 1,
                'total_amount': 3,
            },
            id='200 success with limit and offset',
        ),
        pytest.param(
            'valid_token',
            {'offset': -5},
            RESPONSE_400,
            id='400 invalid params offset',
        ),
    ],
)
async def test_taxi_order_list(
    token: str,
    params: Dict[str, str],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        taxi_manager = TaxiManager(client)
        try:
            resp = await taxi_manager.order.list(**params)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
        except ValidationError as validation_error:
            assert validation_error.args[0] == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'order_id', 'cancel_state', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'order_id1',
            {'state': TaxiOrderCancelRulesState('free')},
            RESPONSE_CANCEL_200,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            'wrong_order_id1',
            {'state': TaxiOrderCancelRulesState('free')},
            RESPONSE_400,
            id='400 invalid order_id',
        ),
        pytest.param(
            'invalid_token',
            'order_id1',
            {'state': TaxiOrderCancelRulesState('free')},
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'invalid_order_id',
            {'state': TaxiOrderCancelRulesState('free')},
            RESPONSE_404,
            id='404 invalid count',
        ),
    ],
)
async def test_taxi_order_cancel(
    token: str,
    order_id: str,
    cancel_state: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        taxi_manager = TaxiManager(client)
        cancel_state = OrdersCancelRequest(**cancel_state)
        try:
            resp = await taxi_manager.order.cancel(order_id=order_id, cancel_state=cancel_state)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'user_id', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'user_id1',
            RESPONSE_ACTIVE_ORDER_200,
            id='200 success',
        ),
        pytest.param(
            'invalid_token',
            'user_id1',
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'invalid_user_id',
            RESPONSE_404,
            id='404 nof found',
        ),
    ],
)
async def test_taxi_active_order_list(
    token: str,
    user_id: str,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        taxi_manager = TaxiManager(client)
        try:
            resp = await taxi_manager.order.active.list(user_id=user_id)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'order_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            ROUTESTATS_REQUEST,
            RESPONSE_ROUTESTATS_GET_200,
            id='200 success',
        ),
        pytest.param(
            'invalid_token',
            ROUTESTATS_REQUEST,
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            {**ROUTESTATS_REQUEST, 'user_id': 'invalid_user_id'},
            RESPONSE_404,
            id='404 not found',
        ),
        pytest.param(
            'valid_token',
            {**ROUTESTATS_REQUEST, 'route': ['a', 'b']},
            'Invalid value for route: [\'a\', \'b\'] is not instance of List[List[Union[int, float, Decimal]]]',
            id='400 invalid route',
        ),
    ],
)
async def test_taxi_order_routestats_get(
    token: str,
    order_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        taxi_manager = TaxiManager(client)
        try:
            order = OrderRequest(**order_params)
            resp = await taxi_manager.order.routestats.get(order=order)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
        except ValidationError as validation_error:
            assert validation_error.args[0] == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'order_id', 'feedback_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'order_id1',
            {'rating': 5, 'msg': 'message'},
            {},
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            'wrong_order_id1',
            {'rating': 5, 'msg': 'message'},
            RESPONSE_400,
            id='400 invalid order_id',
        ),
        pytest.param(
            'invalid_token',
            'order_id1',
            {'rating': 5, 'msg': 'message'},
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'order_id1',
            {'rating': 9, 'msg': 'message'},
            RESPONSE_400,
            id='400 invalid rating',
        ),
    ],
)
async def test_taxi_order_feedback_create(
    token: str,
    order_id: str,
    feedback_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        taxi_manager = TaxiManager(client)
        feedback = Feedback(**feedback_params)
        try:
            resp = await taxi_manager.order.feedback.create(order_id=order_id, feedback=feedback)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'order_id', 'destinations_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'order_id1',
            DESTINATIONS_UPDATE_REQUEST,
            RESPONSE_DESTINATIONS_UPDATE_200,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            'wrong_order_id1',
            DESTINATIONS_UPDATE_REQUEST,
            RESPONSE_400,
            id='400 invalid order_id',
        ),
        pytest.param(
            'invalid_token',
            'order_id1',
            DESTINATIONS_UPDATE_REQUEST,
            RESPONSE_401,
            id='401 unauthorized',
        ),
    ],
)
async def test_taxi_order_destinations_update(
    token: str,
    order_id: str,
    destinations_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        taxi_manager = TaxiManager(client)
        destinations = TaxiOrderDestinationsUpdateRequest(**destinations_params)
        try:
            resp = await taxi_manager.order.destinations.update(order_id=order_id, destinations=destinations)
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
            RESPONSE_STATUS_GET_200,
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
async def test_taxi_order_status_get(
    token: str,
    order_id: str,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        taxi_manager = TaxiManager(client)
        try:
            resp = await taxi_manager.order.status.get(order_id=order_id)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
