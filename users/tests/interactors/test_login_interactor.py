from unittest.mock import patch

import pytest


class TestLoginInteractor:

    @pytest.fixture
    def presenter_mock(self):
        from mock import create_autospec
        from posts_auth.interactors.presenter_interfaces.login_presenter_interface import \
           LoginPresenterInterface
        presenter = create_autospec(LoginPresenterInterface)
        return presenter

    @pytest.fixture
    def interactor_mock(self):
        from posts_auth.interactors.login_interactor import \
            LoginInteractor
        interactor = LoginInteractor()
        return interactor


    def test_raise_invalid_credentials_exception(self,presenter_mock,
                                                 interactor_mock, mocker):
        # Arrange
        client_id = "client_id"
        code = "code"
        from ib_user_accounts_helper.exceptions.custom_exceptions import \
            InvalidCredentialsException
        from posts_auth.tests.common_fixtures.adapters import \
            get_ib_accounts_access_token
        service_mock = get_ib_accounts_access_token(mocker)
        service_mock.side_effect = InvalidCredentialsException
        # Act
        interactor_mock.login_wrapper(client_id=client_id,
                                      code=code,
                                      presenter=presenter_mock)
        # Assert
        service_mock.assert_called_once_with(code=code)
        presenter_mock.raise_invalid_credentials_exception.assert_called_once()


    def test_given_valid_details_return_auth_tokens(self,presenter_mock,interactor_mock,mocker):
        # Arrange
        client_id = "client_id"
        code = "code"

        from posts_auth.interactors.storage_interfaces.dtos import \
            UserAuthTokensDTO, TokensDTO
        user_id = "user"
        from posts_auth.tests.common_fixtures.adapters import \
            get_ib_accounts_access_token, get_access_token, \
            create_user_in_ib_users, create_ib_accounts_auth_tokens
        create_user_in_ib_users = create_user_in_ib_users(mocker)
        create_ib_accounts_auth_tokens = create_ib_accounts_auth_tokens(mocker)
        get_ib_accounts_access_token = get_ib_accounts_access_token(mocker)
        get_ib_accounts_access_token.return_value = UserAuthTokensDTO(
            access_token="access_token",
            refresh_token="refresh_token",
            user_id=user_id)
        get_access_token = get_access_token(mocker)
        get_access_token.return_value = TokensDTO(
            access_token="access_token",
            refresh_token="refresh_token",
            expires_in=36000)
        # Act
        interactor_mock.login_wrapper(client_id=client_id,
                                      code=code,
                                      presenter=presenter_mock)
        # Assert
        get_ib_accounts_access_token.assert_called_once_with(code=code)
        get_access_token.assert_called_once_with(user_id=user_id)


    def test_user_account_deactivated_exception(
            self,
            presenter_mock,
            interactor_mock,
            mocker
    ):
        # Arrange
        client_id = "client_id"
        code = "code"
        from posts_auth.exceptions.custom_exceptions import \
            UserAccountIsDeactivatedException
        user_id = "user"
        from posts_auth.interactors.storage_interfaces.dtos import \
            UserAuthTokensDTO
        from posts_auth.tests.common_fixtures.adapters import \
            get_ib_accounts_access_token,create_ib_accounts_auth_tokens, \
            create_user_in_ib_users,get_access_token
        get_ib_accounts_access_token = get_ib_accounts_access_token(mocker)
        create_ib_accounts_auth_tokens = create_ib_accounts_auth_tokens(mocker)
        create_user_in_ib_users = create_user_in_ib_users(mocker)
        get_access_token = get_access_token(mocker)
        get_ib_accounts_access_token.return_value = UserAuthTokensDTO(
            access_token="access_token",
            refresh_token="refresh_token",
            user_id=user_id, expires_in=3600)
        get_access_token.side_effect = UserAccountIsDeactivatedException
        # Act
        interactor_mock.login_wrapper(client_id=client_id,
                                      code=code,
                                      presenter=presenter_mock)
        # Assert
        get_access_token.assert_called_once_with(user_id=user_id)
        presenter_mock.raise_user_account_deactivated_exception.assert_called_once()
