"""
Return Refresh Auth Token
"""
from unittest.mock import patch
import pytest
from django_swagger_utils.utils.test_utils import TestUtils
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX


class TestCase04RefreshAuthTokensV1APITestCase(TestUtils):
    APP_NAME = APP_NAME
    OPERATION_NAME = OPERATION_NAME
    REQUEST_METHOD = REQUEST_METHOD
    URL_SUFFIX = URL_SUFFIX
    SECURITY = {}

    @pytest.mark.django_db
    def test_case(self, snapshot, mocker):
        body = {'refresh_token': 'refresh_token'}
        path_params = {}
        query_params = {}
        headers = {}

        auth_tokens_dict = {
            "user_id": 1,
            "access_token": "access_token",
            "refresh_token": "refresh_token",
            "expires_in": 10000
        }
        from posts_auth.adapters.dtos import UserAuthTokensDTO
        auth_tokens_dto = UserAuthTokensDTO(**auth_tokens_dict)
        from posts_auth.tests.common_fixtures.adapters import \
            refresh_auth_tokens_mock
        refresh_auth_tokens_mock = refresh_auth_tokens_mock(mocker)
        refresh_auth_tokens_mock.return_value = auth_tokens_dto

        response = self.make_api_call(body=body,
                                      path_params=path_params,
                                      query_params=query_params,
                                      headers=headers,
                                      snapshot=snapshot)
