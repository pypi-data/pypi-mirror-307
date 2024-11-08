from unittest.mock import AsyncMock

import pytest

from yandex_b2b_go import Client, UserManager
from yandex_b2b_go.errors import ApiError

SUCCESS_ARCHIVE = {'status': 'OK'}
RESPONSE_GENERAL_401 = {
    'code': 'unauthorized',
    'message': 'Not authorized request',
}
RESPONSE_403 = {'code': 'FORBIDDEN', 'message': 'Acl check have not passed'}
RESPONSE_404 = {'code': 'NOT_FOUND', 'message': 'No such user'}


def mock_users_archive(params, headers, **kwargs):
    response = AsyncMock()
    if headers['Authorization'] == 'Bearer invalid_token':
        response.status = 401
        response.json.return_value = RESPONSE_GENERAL_401
        return response

    if params['user_id'] == 'user_id1':
        response.status = 200
        response.json.return_value = SUCCESS_ARCHIVE
    elif params['user_id'] == 'other_user_id1':
        response.status = 403
        response.json.return_value = RESPONSE_403
    else:
        response.status = 404
        response.json.return_value = RESPONSE_404

    return response


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ['token', 'user_id', 'expected_response'],
    [
        pytest.param(
            'valid_token',
            'user_id1',
            SUCCESS_ARCHIVE,
            id='200 success',
        ),
        pytest.param(
            'invalid_token',
            'user_id1',
            RESPONSE_GENERAL_401,
            id='401 unauthorized',
        ),
        pytest.param(
            'valid_token',
            'other_user_id1',
            RESPONSE_403,
            id='403 Acl check have not passed',
        ),
        pytest.param(
            'valid_token',
            'user_invalid',
            RESPONSE_404,
            id='404 not such user',
        ),
    ],
)
async def test_user_archive(
    token: str,
    user_id: str,
    expected_response,
    aiohttp_request,
):
    async with Client(token) as client:
        user_manager = UserManager(client)
        try:
            resp = await user_manager.archive(user_id)
            assert expected_response == resp.serialize()
        except ApiError as api_error:
            data_error = api_error.serialize()
            data_error.pop('status')
            assert data_error == expected_response
