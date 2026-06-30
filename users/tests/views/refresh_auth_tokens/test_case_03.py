"""
Raise UserAccountDeactivatedException
"""
from unittest.mock import patch
import pytest
from django_swagger_utils.utils.test_utils import TestUtils
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX


class TestCase03RefreshAuthTokensV1APITestCase(TestUtils):
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

        from posts_auth.exceptions.custom_exceptions import \
            UserAccountDeactivatedException
        from posts_auth.tests.common_fixtures.adapters import \
            refresh_auth_tokens_mock
        refresh_auth_tokens_mock = refresh_auth_tokens_mock(mocker)
        refresh_auth_tokens_mock.side_effect = UserAccountDeactivatedException()

        response = self.make_api_call(body=body,
                                      path_params=path_params,
                                      query_params=query_params,
                                      headers=headers,
                                      snapshot=snapshot)
