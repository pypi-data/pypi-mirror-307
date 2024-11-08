from typing import Any, Dict
from unittest.mock import AsyncMock

import pytest

from yandex_b2b_go import Client, GeoManager
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.typing import Geo, GeoCircle, GeoRestrictions

BASE_GEO_REQUEST = {
    'name': 'geo_name',
    'geo_type': Geo.circle,
    'geo': GeoCircle(lat=37.642639, lon=55.734894, radius=1000),
}

GEO_1 = {
    'id': 'geo_id1',
    'name': 'geo_name1',
    'geo_type': Geo.circle.value,
    'geo': GeoCircle(lat=37.642639, lon=55.734894, radius=1000).serialize(),
}
GEO_2 = {**GEO_1, 'id': 'geo_id2'}
GEO_3 = {**GEO_1, 'id': 'geo_id3'}

RESPONSE_200 = {'id': 'geo_id1'}
RESPONSE_400 = {
    'code': 'BadRequest',
    'message': 'geo restriction has incorrect radius',
    'reason': 'radius should be greater than 0, got -500',
}
RESPONSE_LIST_400 = {
    'code': 'BadRequest',
    'message': 'has incorrect offset',
    'reason': 'offset should be greater than 0, got -5',
}
RESPONSE_401 = {'code': 'unauthorized', 'message': 'Not authorized request'}
RESPONSE_403 = {'code': 'FORBIDDEN', 'message': 'Acl check have not passed'}
RESPONSE_404 = {'code': 'NOT_FOUND', 'message': 'Not found geo_restriction'}


def mock_geo_create(json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if json['geo']['radius'] < 0:
        response.status = 400
        response.json.return_value = RESPONSE_400
    else:
        response.status = 200
        response.json.return_value = RESPONSE_200

    return response


def mock_geo_update(params, json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if json['geo']['radius'] < 0:
        response.status = 400
        response.json.return_value = RESPONSE_400
    elif params['id'] == 'other_geo_id':
        response.status = 403
        response.json.return_value = RESPONSE_403
    elif params['id'] == 'invalid_geo_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    else:
        response.status = 200
        response.json.return_value = RESPONSE_200

    return response


def mock_geo_delete(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params['id'] == 'other_geo_id':
        response.status = 403
        response.json.return_value = RESPONSE_403
    elif params['id'] == 'invalid_geo_id':
        response.status = 404
        response.json.return_value = RESPONSE_404
    else:
        response.status = 200
        response.json.return_value = RESPONSE_200

    return response


def mock_geo_list(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    items = [GEO_1, GEO_2, GEO_3]

    if params.get('offset') == '-5':
        response.status = 400
        response.json.return_value = RESPONSE_LIST_400
    else:
        return_value = {'amount': len(items), 'limit': 100, 'offset': 0}
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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'geo_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            BASE_GEO_REQUEST,
            RESPONSE_200,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            {
                **BASE_GEO_REQUEST,
                'geo': GeoCircle(lat=37.642639, lon=55.734894, radius=-500),
            },
            RESPONSE_400,
            id='400 invalid radius',
        ),
        pytest.param(
            'invalid_token',
            BASE_GEO_REQUEST,
            RESPONSE_401,
            id='401 unauthorized',
        ),
    ],
)
async def test_geo_create(
    token: str,
    geo_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        geo_manager = GeoManager(client)
        geo_restrictions = GeoRestrictions(**geo_params)
        try:
            resp = await geo_manager.create(geo_restrictions=geo_restrictions)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'geo_id', 'geo_params', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'geo_id1',
            BASE_GEO_REQUEST,
            RESPONSE_200,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            'geo_id1',
            {
                **BASE_GEO_REQUEST,
                'geo': GeoCircle(lat=37.642639, lon=55.734894, radius=-500),
            },
            RESPONSE_400,
            id='400 Invalid radius',
        ),
        pytest.param(
            'invalid_token',
            'geo_id1',
            BASE_GEO_REQUEST,
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'other_geo_id',
            BASE_GEO_REQUEST,
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
        pytest.param(
            'valid_token',
            'invalid_geo_id',
            BASE_GEO_REQUEST,
            RESPONSE_404,
            id='404 Geo not found',
        ),
    ],
)
async def test_geo_update(
    token: str,
    geo_id: str,
    geo_params: Dict[str, Any],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        geo_manager = GeoManager(client)
        geo_restrictions = GeoRestrictions(**geo_params)
        try:
            resp = await geo_manager.update(
                geo_id=geo_id,
                geo_restrictions=geo_restrictions,
            )
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'geo_id', 'expected_response'],
    [
        pytest.param('valid_token', 'geo_id1', RESPONSE_200, id='200 success'),
        pytest.param(
            'invalid_token',
            'geo_id1',
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'other_geo_id',
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
        pytest.param(
            'valid_token',
            'invalid_geo_id',
            RESPONSE_404,
            id='404 Geo not found',
        ),
    ],
)
async def test_geo_delete(
    token: str,
    geo_id: str,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        geo_manager = GeoManager(client)
        try:
            resp = await geo_manager.delete(geo_id=geo_id)
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
                'items': [GEO_1, GEO_2, GEO_3],
                'limit': 100,
                'amount': 3,
                'offset': 0,
            },
            id='200 success without params',
        ),
        pytest.param(
            'valid_token',
            {'limit': 2},
            {'items': [GEO_1, GEO_2], 'limit': 2, 'amount': 3, 'offset': 0},
            id='200 success with limit',
        ),
        pytest.param(
            'valid_token',
            {'offset': 1},
            {'items': [GEO_2, GEO_3], 'limit': 100, 'amount': 3, 'offset': 1},
            id='200 success with offset',
        ),
        pytest.param(
            'valid_token',
            {'limit': 1, 'offset': 1},
            {'items': [GEO_2], 'limit': 1, 'amount': 3, 'offset': 1},
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
async def test_geo_list(
    token: str,
    params: Dict[str, str],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        geo_manager = GeoManager(client)
        try:
            resp = await geo_manager.list(**params)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
        except ValidationError as validation_error:
            assert validation_error.args[0] == expected_response
