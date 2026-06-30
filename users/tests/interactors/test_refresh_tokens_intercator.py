from unittest.mock import create_autospec, Mock

from mock import patch

from posts_auth.interactors.presenter_interfaces.refresh_auth_tokens_presenter_interface import \
    RefreshAuthTokensPresenterInterface
from posts_auth.interactors.refresh_auth_tokens_interactor import \
    RefreshAuthTokensInteractor


class TestRefreshAuthTokensInteractor:

    @patch(
        "users.adapters.user_service.AuthService.refresh_auth_tokens"
    )
    def test_given_invalid_access_token_raises_exception(self,
                                                         refresh_auth_tokens_mock):
        # Arrange
        access_token = "access_token"
        refresh_token = "refresh_token"
        interactor = RefreshAuthTokensInteractor()
        presenter = create_autospec(RefreshAuthTokensPresenterInterface)

        expected_response = Mock()
        presenter.raise_invalid_access_token_exception.return_value = \
            expected_response
        from posts_auth.exceptions.custom_exceptions import \
            InvalidAccessTokenException
        refresh_auth_tokens_mock.side_effect = InvalidAccessTokenException()

        # Act
        actual_response = interactor.refresh_auth_tokens_wrapper(
            access_token=access_token,
            refresh_token=refresh_token,
            presenter=presenter
        )

        # Assert
        assert actual_response == expected_response
        refresh_auth_tokens_mock.assert_called_once_with(
            access_token=access_token,
            refresh_token=refresh_token
        )
        presenter.raise_invalid_access_token_exception.assert_called_once()


    def test_given_expired_refresh_token_raises_exception(self, mocker):
        # Arrange
        access_token = "access_token"
        refresh_token = "refresh_token"
        interactor = RefreshAuthTokensInteractor()
        presenter = create_autospec(RefreshAuthTokensPresenterInterface)

        expected_response = Mock()
        presenter.raise_refresh_token_expired_exception.return_value = \
            expected_response
        from posts_auth.exceptions.custom_exceptions import \
            RefreshTokenExpiredException
        from posts_auth.tests.common_fixtures.adapters import \
            refresh_auth_tokens_mock
        refresh_auth_tokens_mock  = refresh_auth_tokens_mock(mocker)
        refresh_auth_tokens_mock.side_effect = RefreshTokenExpiredException()

        # Act
        actual_response = interactor.refresh_auth_tokens_wrapper(
            access_token=access_token,
            refresh_token=refresh_token,
            presenter=presenter
        )

        # Assert
        assert actual_response == expected_response
        refresh_auth_tokens_mock.assert_called_once_with(
            access_token=access_token,
            refresh_token=refresh_token
        )
        presenter.raise_refresh_token_expired_exception.assert_called_once()


    def test_given_account_deactivated_raises_exception(self, mocker):
        # Arrange
        access_token = "access_token"
        refresh_token = "refresh_token"
        interactor = RefreshAuthTokensInteractor()
        presenter = create_autospec(RefreshAuthTokensPresenterInterface)

        expected_response = Mock()
        presenter.raise_user_account_deactivated_exception.return_value = \
            expected_response
        from posts_auth.exceptions.custom_exceptions import \
            UserAccountDeactivatedException
        from posts_auth.tests.common_fixtures.adapters import \
            refresh_auth_tokens_mock
        refresh_auth_tokens_mock = refresh_auth_tokens_mock(mocker)
        refresh_auth_tokens_mock.side_effect = UserAccountDeactivatedException()

        # Act
        actual_response = interactor.refresh_auth_tokens_wrapper(
            access_token=access_token,
            refresh_token=refresh_token,
            presenter=presenter
        )

        # Assert
        assert actual_response == expected_response
        refresh_auth_tokens_mock.assert_called_once_with(
            access_token=access_token,
            refresh_token=refresh_token
        )
        presenter.raise_user_account_deactivated_exception.assert_called_once()


    def test_given_refresh_token_return_new_auth_tokens(self, mocker):
        # Arrange
        access_token = "access_token"
        refresh_token = "refresh_token"
        interactor = RefreshAuthTokensInteractor()
        presenter = create_autospec(RefreshAuthTokensPresenterInterface)

        expected_response = Mock()
        presenter.get_response_for_refresh_auth_tokens.return_value = \
            expected_response
        from posts_auth.adapters.dtos import UserAuthTokensDTO
        auth_tokens_dto = UserAuthTokensDTO(
            user_id=str(1),
            expires_in=100000,
            access_token=access_token,
            refresh_token=refresh_token,
        )
        from posts_auth.tests.common_fixtures.adapters import \
            refresh_auth_tokens_mock
        refresh_auth_tokens_mock = refresh_auth_tokens_mock(mocker)
        refresh_auth_tokens_mock.return_value = auth_tokens_dto

        # Act
        actual_response = interactor.refresh_auth_tokens_wrapper(
            access_token=access_token,
            refresh_token=refresh_token,
            presenter=presenter
        )

        # Assert
        assert actual_response == expected_response
        refresh_auth_tokens_mock.assert_called_once_with(
            access_token=access_token,
            refresh_token=refresh_token
        )
        presenter.get_response_for_refresh_auth_tokens.assert_called_once_with(
            auth_tokens_dto=auth_tokens_dto
        )
