from typing import List
from unittest.mock import AsyncMock

import pytest

from yandex_b2b_go import Client, UserManager
from yandex_b2b_go.errors import ApiError
from yandex_b2b_go.typing import UsersSpendingListRequest

USER_IDS = ['user_id1', 'user_id2']
SUCCESS = {
    'users': [
        {'user_id': 'user_id1', 'limits': []},
        {
            'user_id': 'user_id2',
            'limits': [
                {
                    'limit_id': 'limit_id1',
                    'service': 'drive',
                    'spending_details': {
                        'orders_cost': '10000',
                        'spent': '0',
                        'orders_spent': 0,
                    },
                },
                {
                    'limit_id': 'limit_id2',
                    'service': 'eats2',
                    'spending_details': {
                        'orders_cost': '147614.40',
                        'spent': '0',
                        'orders_spent': 0,
                    },
                },
            ],
        },
    ],
}
RESPONSE_GENERAL_401 = {
    'code': 'unauthorized',
    'message': 'Not authorized request',
}
RESPONSE_403 = {'code': 'FORBIDDEN', 'message': 'Acl check have not passed'}
RESPONSE_404 = {'code': 'NOT_FOUND', 'message': 'User not found'}


def mock_users_spending_details(json, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_GENERAL_401
        return response

    if 'other_user_id' in json['user_ids']:
        response.status = 403
        response.json.return_value = RESPONSE_403
    elif 'invalid_user_id' in json['user_ids']:
        response.status = 404
        response.json.return_value = RESPONSE_404
    else:
        response.status = 200
        response.json.return_value = SUCCESS
    return response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'user_ids', 'expected_response'],
    [
        pytest.param('valid_token', USER_IDS, SUCCESS, id='200 success'),
        pytest.param(
            'invalid_token',
            USER_IDS,
            RESPONSE_GENERAL_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            [*USER_IDS, 'other_user_id'],
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
        pytest.param(
            'valid_token',
            [*USER_IDS, 'invalid_user_id'],
            RESPONSE_404,
            id='404 User not found',
        ),
    ],
)
async def test_users_spending_details(
    token: str,
    user_ids: List[str],
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        user_manager = UserManager(client)
        try:
            resp = await user_manager.spending.list(
                UsersSpendingListRequest(user_ids),
            )
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
