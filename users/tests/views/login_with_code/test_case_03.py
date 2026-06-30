"""
Raise UserAccountIsDeactivatedException
"""
from unittest.mock import patch

import pytest
from django_swagger_utils.utils.test_utils import TestUtils
from . import APP_NAME, OPERATION_NAME, REQUEST_METHOD, URL_SUFFIX


class TestCase03LoginWithCodeAPITestCase(TestUtils):
    APP_NAME = APP_NAME
    OPERATION_NAME = OPERATION_NAME
    REQUEST_METHOD = REQUEST_METHOD
    URL_SUFFIX = URL_SUFFIX
    SECURITY = {}

    @pytest.mark.django_db
    def test_case(self,  snapshot, mocker):
        body = {'client_id': 'string', 'code': 'string'}
        path_params = {}
        query_params = {}
        headers = {}
        from posts_auth.exceptions.custom_exceptions import \
            UserAccountIsDeactivatedException
        user_id = "user"
        from posts_auth.interactors.storage_interfaces.dtos import \
            UserAuthTokensDTO
        from posts_auth.tests.common_fixtures.adapters import \
            get_ib_accounts_access_token, get_access_token, \
            create_ib_accounts_auth_tokens, create_user_in_ib_users
        get_ib_accounts_access_token = get_ib_accounts_access_token(mocker)
        get_access_token = get_access_token(mocker)
        create_ib_accounts_auth_tokens = create_ib_accounts_auth_tokens(mocker)
        create_user_in_ib_users = create_user_in_ib_users(mocker)
        get_ib_accounts_access_token.return_value = UserAuthTokensDTO(
            access_token="access_token",
            refresh_token="refresh_token",
            user_id=user_id,expires_in=3600)
        get_access_token.side_effect = UserAccountIsDeactivatedException

        response = self.make_api_call(body=body,
                                      path_params=path_params,
                                      query_params=query_params,
                                      headers=headers,
                                      snapshot=snapshot)
