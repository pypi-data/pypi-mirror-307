from typing import Dict, Optional, Union

from yandex_b2b_go import utils
from yandex_b2b_go.client import Client
from yandex_b2b_go.errors import ApiError, ValidationError
from yandex_b2b_go.request import Request
from yandex_b2b_go.typing import (
    BudgetCostCenterListResponse,
    BudgetLimitCargoRequest,
    BudgetLimitDriveRequest,
    BudgetLimitEatsRequest,
    BudgetLimitGroceryRequest,
    BudgetLimitListResponse,
    BudgetLimitTankerRequest,
    BudgetLimitTaxiRequest,
    BudgetLimitTravelRequest,
    BudgetLimitUpdateResponse,
    Service,
    SortingOrder,
)


class BudgetLimitManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def list(
        self,
        service: Optional[Service] = None,
        department_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        search: Optional[str] = None,
        sorting_order: Optional[SortingOrder] = None,
        sorting_field: Optional[str] = None,
    ) -> BudgetLimitListResponse:
        params: Dict[str, str] = {}

        if service is not None:
            if not isinstance(service, (Service,)):
                raise ValidationError(utils.error_string('service', service, '(Service)'))
            params['service'] = service.value
        if department_id is not None:
            if not isinstance(department_id, str):
                raise ValidationError(utils.error_string('department_id', department_id, 'str'))
            params['department_id'] = department_id
        if search is not None:
            if not isinstance(search, str):
                raise ValidationError(utils.error_string('search', search, 'str'))
            params['search'] = search
        if limit is not None:
            params['limit'] = utils.serialize_integer(limit, 'limit')
        if offset is not None:
            params['offset'] = utils.serialize_integer(offset, 'offset')
        if sorting_order is not None:
            if not isinstance(sorting_order, SortingOrder):
                raise ValidationError(utils.error_string('sorting_order', sorting_order, 'SortingOrder'))
            params['sortingStrDirection'] = sorting_order.value
        if sorting_field is not None:
            if not isinstance(sorting_field, str):
                raise ValidationError(utils.error_string('sorting_field', sorting_field, 'str'))
            params['sortingField'] = sorting_field

        request = Request(method='GET', endpoint='limits/search', params=params)

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return BudgetLimitListResponse.new(json)

        raise ApiError.new(response.status, json)

    async def update(
        self,
        user_id: str,
        budget_limit: Union[
            BudgetLimitTaxiRequest,
            BudgetLimitEatsRequest,
            BudgetLimitGroceryRequest,
            BudgetLimitTankerRequest,
            BudgetLimitDriveRequest,
            BudgetLimitCargoRequest,
            BudgetLimitTravelRequest,
        ],
    ) -> BudgetLimitUpdateResponse:
        if not isinstance(user_id, str):
            raise ValidationError(utils.error_string('user_id', user_id, 'str'))

        params: Dict[str, str] = {'user_id': user_id}

        request = Request(method='PUT', endpoint='limits/personal', params=params, data=budget_limit.serialize())

        response = await self._client.request(request=request)

        json = await response.json()

        if response.status == 200:
            return BudgetLimitUpdateResponse.new(json)

        raise ApiError.new(response.status, json)


class BudgetCostCenterManager:
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    async def list(self, limit: Optional[int] = None, offset: Optional[int] = None) -> BudgetCostCenterListResponse:
        params: Dict[str, str] = {}

        if limit is not None:
            params['limit'] = utils.serialize_integer(limit, 'limit')
        if offset is not None:
            params['offset'] = utils.serialize_integer(offset, 'offset')

        request = Request(method='GET', endpoint='cost_centers/list', params=params)

        response = await self._client.request(request=request)

        json = await response.json()
        if response.status == 200:
            return BudgetCostCenterListResponse.new(json)

        raise ApiError.new(response.status, json)


class BudgetManager:
    limit: BudgetLimitManager
    cost_center: BudgetCostCenterManager
    _client: Client

    def __init__(self, client: Client):
        self._client = client
        self.limit = BudgetLimitManager(client)
        self.cost_center = BudgetCostCenterManager(client)
