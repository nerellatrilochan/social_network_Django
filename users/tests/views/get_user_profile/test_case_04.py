"""
Raise GetUserProfileFailedException
"""
import pytest
from django_swagger_utils.utils.test_utils import TestUtils
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX


class TestCase04GetUserProfileAPITestCase(TestUtils):
    APP_NAME = APP_NAME
    OPERATION_NAME = OPERATION_NAME
    REQUEST_METHOD = REQUEST_METHOD
    URL_SUFFIX = URL_SUFFIX
    SECURITY = {'oauth': {'scopes': ['write', 'read']}}

    @pytest.mark.django_db
    def test_case(self, api_user, mocker, snapshot):
        body = {}
        path_params = {}
        query_params = {}
        headers = {}

        from posts_auth.tests.common_fixtures.adapters import \
            get_user_profile_mock
        from posts_auth.exceptions.custom_exceptions import \
            GetUserProfileFailedException
        get_user_profile_mock = get_user_profile_mock(mocker)
        get_user_profile_mock.side_effect = GetUserProfileFailedException()

        response = self.make_api_call(body=body,
                                      path_params=path_params,
                                      query_params=query_params,
                                      headers=headers,
                                      snapshot=snapshot)
