from typing import Dict, Optional

from yandex_b2b_go import utils
from yandex_b2b_go.client import Client
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.request import Request
from yandex_b2b_go.typing import (
    GeoRestrictions,
    GeoRestrictionsListResponse,
    GeoRestrictionsResponse,
    ZoneInfoResponse,
)


class ZoneInfoManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def get(self, lat: float, lon: float) -> ZoneInfoResponse:
        params: Dict[str, str] = {}

        if lat is not None:
            if not -90.0 <= lat <= 90.0:
                raise ValidationError('lat must be between -90.0 and 90.0')
            params['lat'] = utils.serialize_number(lat, 'lat')
        if lon is not None:
            if not -180.0 <= lon <= 180.0:
                raise ValidationError('lon must be between -180.0 and 180.0')
            params['lon'] = utils.serialize_number(lon, 'lon')

        request = Request(method='GET', endpoint='zoneinfo', params=params)
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return ZoneInfoResponse.new(json)

        raise ApiError.new(response.status, json)


class GeoManager:
    _client: Client
    zoneinfo: ZoneInfoManager

    def __init__(self, client: Client):
        self._client = client
        self.zoneinfo = ZoneInfoManager(client)

    async def list(self, limit: Optional[int] = None, offset: Optional[int] = None) -> GeoRestrictionsListResponse:
        params: Dict[str, str] = {}

        if limit is not None:
            params['limit'] = utils.serialize_integer(limit, 'limit')

        if offset is not None:
            params['offset'] = utils.serialize_integer(offset, 'offset')

        request = Request(method='GET', endpoint='geo_restrictions/list', params=params)
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return GeoRestrictionsListResponse.new(json)

        raise ApiError.new(response.status, json)

    async def create(self, geo_restrictions: GeoRestrictions) -> GeoRestrictionsResponse:
        if not isinstance(geo_restrictions, GeoRestrictions):
            raise ValidationError(utils.error_string('geo_restrictions', geo_restrictions, 'GeoRestrictions'))
        request = Request(method='POST', endpoint='geo_restrictions/create', data=geo_restrictions.serialize())
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return GeoRestrictionsResponse.new(json)

        raise ApiError.new(response.status, json)

    async def update(self, geo_id: str, geo_restrictions: GeoRestrictions) -> GeoRestrictionsResponse:
        if not isinstance(geo_restrictions, GeoRestrictions):
            raise ValidationError(utils.error_string('geo_restrictions', geo_restrictions, 'GeoRestrictions'))
        if not isinstance(geo_id, str):
            raise ValidationError(utils.error_string('geo_id', geo_id, 'str'))
        params: Dict[str, str] = {'id': geo_id}
        request = Request(
            method='POST',
            endpoint='geo_restrictions/update',
            data=geo_restrictions.serialize(),
            params=params,
        )
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return GeoRestrictionsResponse.new(json)

        raise ApiError.new(response.status, json)

    async def delete(self, geo_id: str) -> GeoRestrictionsResponse:
        if not isinstance(geo_id, str):
            raise ValidationError(utils.error_string('geo_id', geo_id, 'str'))
        params: Dict[str, str] = {'id': geo_id}
        request = Request(method='POST', endpoint='geo_restrictions/delete', params=params)
        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return GeoRestrictionsResponse.new(json)

        raise ApiError.new(response.status, json)
