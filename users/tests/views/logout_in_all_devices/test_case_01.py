"""
# logout success response
"""
import pytest

from unittest.mock import patch
from django_swagger_utils.utils.test_utils import TestUtils
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX


class TestCase01LogoutInAllDevicesAPITestCase(TestUtils):
    APP_NAME = APP_NAME
    OPERATION_NAME = OPERATION_NAME
    REQUEST_METHOD = REQUEST_METHOD
    URL_SUFFIX = URL_SUFFIX
    SECURITY = {'oauth': {'scopes': ['read', 'write']}}

    @pytest.mark.django_db
    def test_case(self, snapshot, mocker):
        body = {}
        path_params = {}
        query_params = {}
        headers = {}
        from posts_auth.tests.common_fixtures.adapters import \
            logout_in_all_devices
        logout_mock = logout_in_all_devices(mocker)
        response = self.make_api_call(body=body,
                                      path_params=path_params,
                                      query_params=query_params,
                                      headers=headers,
                                      snapshot=snapshot)
