import pytest
from django.http import response

from posts_auth.presenters.login_presenter_imp import \
    INVALID_CREDENTIALS, USER_ACCOUNT_IS_DEACTIVATED

class TestLoginPresenterImplementation:

    @pytest.fixture
    def presenter(self):
        from posts_auth.presenters.login_presenter_imp import \
            LoginPresenterImplementation

        return LoginPresenterImplementation()

    def test_raise_invalid_credentials_exception(self, presenter):
        # Arrange
        import json
        data = json.dumps({
            "response": INVALID_CREDENTIALS[0],
            "http_status_code": 403,
            "res_status": INVALID_CREDENTIALS[1]
        })
        expected_http_response = response.HttpResponse(data, status=403)
        expected_response = expected_http_response.content

        # Act
        actual_http_response = presenter.raise_invalid_credentials_exception()

        # Assert
        actual_response = actual_http_response.content
        assert actual_response == expected_response

    def test_raise_user_account_deactivated_exception(self, presenter):
        # Arrange
        import json
        data = json.dumps({
            "response": USER_ACCOUNT_IS_DEACTIVATED[0],
            "http_status_code": 403,
            "res_status": USER_ACCOUNT_IS_DEACTIVATED[1]
        })
        expected_http_response = response.HttpResponse(data, status=400)
        expected_response = expected_http_response.content

        # Act
        actual_http_response = presenter.raise_user_account_deactivated_exception()

        # Assert
        actual_response = actual_http_response.content
        assert actual_response == expected_response

    def test_get_response_for_login(self, presenter):
        # Arrange
        auth_tokens_dict = {
            "access_token": "access_token",
            "refresh_token": "refresh_token",
            "expires_in": 36000
        }
        from posts_auth.interactors.storage_interfaces.dtos import \
            TokensDTO
        auth_tokens_dto = TokensDTO(**auth_tokens_dict)
        import json
        data = json.dumps(auth_tokens_dict)
        expected_http_response = response.HttpResponse(data, status=200)
        expected_response = expected_http_response.content
        # Act
        actual_http_response = presenter.get_response_for_login(
            token_dto=auth_tokens_dto
        )
        # Assert
        actual_response = actual_http_response.content
        assert actual_response == expected_response