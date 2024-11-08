from unittest.mock import AsyncMock

import pytest

from yandex_b2b_go import Client, GeoManager
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.typing import (
    SupportedRequirementItemResponse,
    TariffClassItemResponse,
    ZoneInfoResponse,
)

RESPONSE_200 = ZoneInfoResponse(
    tariff_classes=[
        TariffClassItemResponse(
            name='econom',
            name_translate='эконом',
            supported_requirements=[
                SupportedRequirementItemResponse(
                    name='support_name',
                    label='lable',
                    glued=False,
                    type_requirement='boolean',
                    multiselect=False,
                    max_weight=3.0,
                ),
            ],
        ),
    ],
).serialize()
RESPONSE_400 = 'lat must be between -90.0 and 90.0'
RESPONSE_401 = {'code': 'unauthorized', 'message': 'Not authorized request'}
RESPONSE_404 = {'code': 'NOT_FOUND', 'message': 'Zone not found'}


def mock_zoneinfo_get(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_401
        return response

    if params['lat'] == '49.0' and params['lon'] == '-30.0':
        response.status = 404
        response.json.return_value = RESPONSE_404
    else:
        response.status = 200
        response.json.return_value = RESPONSE_200

    return response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'lat', 'lon', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            30.0,
            30.0,
            RESPONSE_200,
            id='200 success',
        ),
        pytest.param(
            'valid_token',
            -230.0,
            30.0,
            RESPONSE_400,
            id='400 invalid lat',
        ),
        pytest.param(
            'invalid_token',
            30.0,
            30.0,
            RESPONSE_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            49.0,
            -30.0,
            RESPONSE_404,
            id='404 Not Found',
        ),
    ],
)
async def test_zoneinfo_get(
    token: str,
    lat: float,
    lon: float,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        geo_manager = GeoManager(client)
        try:
            resp = await geo_manager.zoneinfo.get(lat=lat, lon=lon)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
        except ValidationError as validation_error:
            assert validation_error.args[0] == expected_response
