from unittest.mock import AsyncMock

import pytest

from tests.test_budget_cost_centers import mock_budget_cost_center_list
from tests.test_budget_limit import mock_budget_limit_list, mock_budget_limit_update
from tests.test_department import (
    mock_department_create,
    mock_department_delete,
    mock_department_list,
    mock_department_taxi_limit_get,
    mock_department_taxi_limit_update,
    mock_department_update,
)
from tests.test_eat import mock_eat_order_list
from tests.test_geo import (
    mock_geo_create,
    mock_geo_delete,
    mock_geo_list,
    mock_geo_update,
)
from tests.test_promocode import (
    mock_promocode_cancel,
    mock_promocode_code_list,
    mock_promocode_create,
    mock_promocode_get,
    mock_promocode_list,
)
from tests.test_role import (
    mock_role_create,
    mock_role_delete,
    mock_role_list,
    mock_role_update,
)
from tests.test_tanker import mock_tanker_order_list
from tests.test_taxi_order import (
    mock_taxi_active_order_list,
    mock_taxi_order_cancel,
    mock_taxi_order_create,
    mock_taxi_order_destination_update,
    mock_taxi_order_feedback_create,
    mock_taxi_order_get,
    mock_taxi_order_list,
    mock_taxi_order_routestats_get,
    mock_taxi_order_status_get,
)
from tests.test_users import mock_users
from tests.test_users_archive import mock_users_archive
from tests.test_users_spending_details import mock_users_spending_details
from tests.test_zoneinfo import mock_zoneinfo_get


@pytest.fixture
def patch(monkeypatch):
    def dec_generator(full_func_path):
        def dec(func):
            mocked = func
            monkeypatch.setattr(full_func_path, mocked)
            return mocked

        return dec

    return dec_generator


@pytest.fixture
def aiohttp_request(monkeypatch, patch):
    @patch('aiohttp.ClientSession.request')
    async def request(*args, url, **kwargs):
        if url.startswith('https://b2b-api.go.yandex.ru/integration/2.0/'):
            if url.endswith('/users'):
                return mock_users(**kwargs)
            if url.endswith('/users/archive'):
                return mock_users_archive(**kwargs)
            if url.endswith('/users-spending-details'):
                return mock_users_spending_details(**kwargs)
            if url.endswith('/managers/create'):
                return mock_role_create(**kwargs)
            if url.endswith('/managers/update'):
                return mock_role_update(**kwargs)
            if url.endswith('/managers/delete'):
                return mock_role_delete(**kwargs)
            if url.endswith('/managers/list'):
                return mock_role_list(**kwargs)
            if url.endswith('/orders/tanker'):
                return mock_tanker_order_list(**kwargs)
            if url.endswith('/geo_restrictions/create'):
                return mock_geo_create(**kwargs)
            if url.endswith('/geo_restrictions/update'):
                return mock_geo_update(**kwargs)
            if url.endswith('/geo_restrictions/delete'):
                return mock_geo_delete(**kwargs)
            if url.endswith('/geo_restrictions/list'):
                return mock_geo_list(**kwargs)
            if url.endswith('/zoneinfo'):
                return mock_zoneinfo_get(**kwargs)
            if url.endswith('/orders/eats/list'):
                return mock_eat_order_list(**kwargs)
            if url.endswith('/promocodes/orders/create'):
                return mock_promocode_create(**kwargs)
            if url.endswith('/promocodes/orders/cancel'):
                return mock_promocode_cancel(**kwargs)
            if url.endswith('/promocodes/orders/list'):
                return mock_promocode_list(**kwargs)
            if url.endswith('/promocodes/orders/info'):
                return mock_promocode_get(**kwargs)
            if url.endswith('/promocodes/orders/codes/list'):
                return mock_promocode_code_list(**kwargs)
            if url.endswith('departments/create'):
                return mock_department_create(**kwargs)
            if url.endswith('departments/list'):
                return mock_department_list(**kwargs)
            if url.endswith('departments/update'):
                return mock_department_update(**kwargs)
            if url.endswith('departments/archive'):
                return mock_department_delete(**kwargs)
            if url.endswith('departments/limits/taxi'):
                return mock_department_taxi_limit_get(**kwargs)
            if url.endswith('departments/limits/taxi/update'):
                return mock_department_taxi_limit_update(**kwargs)
            if url.endswith('/orders/eats/list'):
                return mock_eat_order_list(**kwargs)
            if url.endswith('/limits/search'):
                return mock_budget_limit_list(**kwargs)
            if url.endswith('/limits/personal'):
                return mock_budget_limit_update(**kwargs)
            if url.endswith('/cost_centers/list'):
                return mock_budget_cost_center_list(**kwargs)
            if url.endswith('/orders/create'):
                return mock_taxi_order_create(**kwargs)
            if url.endswith('/orders/info'):
                return mock_taxi_order_get(**kwargs)
            if url.endswith('/orders/list'):
                return mock_taxi_order_list(**kwargs)
            if url.endswith('/orders/cancel'):
                return mock_taxi_order_cancel(**kwargs)
            if url.endswith('/orders/active'):
                return mock_taxi_active_order_list(**kwargs)
            if url.endswith('/orders/routestats'):
                return mock_taxi_order_routestats_get(**kwargs)
            if url.endswith('/orders/feedback'):
                return mock_taxi_order_feedback_create(**kwargs)
            if url.endswith('/orders/change-destinations'):
                return mock_taxi_order_destination_update(**kwargs)
            if url.endswith('/orders/progress'):
                return mock_taxi_order_status_get(**kwargs)

        response = AsyncMock()
        response.status = 404

        return response
