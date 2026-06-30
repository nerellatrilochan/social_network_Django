"""
gives get user profile success response
"""
import pytest
from django_swagger_utils.utils.test_utils import TestUtils
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX


class TestCase03GetUserProfileAPITestCase(TestUtils):
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
        from posts_auth.tests.factories.adapter_dtos import \
            UserProfileDTOFactory
        UserProfileDTOFactory.reset_sequence()
        user_profile_dto = UserProfileDTOFactory.create_batch(1)[0]
        get_user_profile_mock = get_user_profile_mock(mocker)
        get_user_profile_mock.return_value = user_profile_dto

        response = self.make_api_call(body=body,
                                      path_params=path_params,
                                      query_params=query_params,
                                      headers=headers,
                                      snapshot=snapshot)
