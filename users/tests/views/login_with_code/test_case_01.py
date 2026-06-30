"""
Raise InvalidCredentialsException
"""
from unittest.mock import patch

import pytest
from django_swagger_utils.utils.test_utils import TestUtils
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX


class TestCase01LoginWithCodeAPITestCase(TestUtils):
    APP_NAME = APP_NAME
    OPERATION_NAME = OPERATION_NAME
    REQUEST_METHOD = REQUEST_METHOD
    URL_SUFFIX = URL_SUFFIX
    SECURITY = {}


    @pytest.mark.django_db
    def test_case(self, snapshot, mocker):
        body = {'client_id': 'string', 'code': 'string'}
        path_params = {}
        query_params = {}
        headers = {}

        from ib_user_accounts_helper.exceptions.custom_exceptions import InvalidCredentialsException
        from posts_auth.tests.common_fixtures.adapters import get_ib_accounts_access_token
        service_mock = get_ib_accounts_access_token(mocker)
        service_mock.side_effect = InvalidCredentialsException

        response = self.make_api_call(body=body,
                                      path_params=path_params,
                                      query_params=query_params,
                                      headers=headers,
                                      snapshot=snapshot)
