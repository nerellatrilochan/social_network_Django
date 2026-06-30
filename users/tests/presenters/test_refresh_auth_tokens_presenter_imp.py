import pytest
from django.http import response

from posts_auth.presenters.refresh_auth_tokens_presenter_imp import \
    RefreshAuthTokensPresenterImplementation, INVALID_ACCESS_TOKEN, REFRESH_TOKEN_EXPIRED, \
    USER_ACCOUNT_IS_DEACTIVATED


class TestPresenterImplementation:

    @pytest.fixture
    def presenter(self):
        return RefreshAuthTokensPresenterImplementation()

    def test_raise_invalid_access_token_exception(self, presenter):
        # Arrange
        import json
        data = json.dumps({
            "response": INVALID_ACCESS_TOKEN[0],
            "http_status_code": 400,
            "res_status": INVALID_ACCESS_TOKEN[1]
        })
        expected_http_response = response.HttpResponse(data, status=400)
        expected_response = expected_http_response.content

        # Act
        actual_http_response = presenter.raise_invalid_access_token_exception()

        # Assert
        actual_response = actual_http_response.content
        assert actual_response == expected_response

    def test_raise_refresh_token_expired_exception(self, presenter):
        # Arrange
        import json
        data = json.dumps({
            "response": REFRESH_TOKEN_EXPIRED[0],
            "http_status_code": 400,
            "res_status": REFRESH_TOKEN_EXPIRED[1]
        })
        expected_http_response = response.HttpResponse(data, status=400)
        expected_response = expected_http_response.content

        # Act
        actual_http_response = presenter.raise_refresh_token_expired_exception()

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

    def test_prepare_response_for_refresh_auth_tokens(self, presenter):
        # Arrange
        auth_tokens_dict = {
            "user_id": 1,
            "access_token": "access_token",
            "refresh_token": "refresh_token",
            "expires_in": 10000
        }
        from posts_auth.adapters.dtos import UserAuthTokensDTO
        auth_tokens_dto = UserAuthTokensDTO(**auth_tokens_dict)
        import json
        data = json.dumps(auth_tokens_dict)
        expected_http_response = response.HttpResponse(data, status=200)
        expected_response = expected_http_response.content

        # Act
        actual_http_response = presenter.get_response_for_refresh_auth_tokens(
            auth_tokens_dto=auth_tokens_dto
        )

        # Assert
        actual_response = actual_http_response.content
        assert actual_response == expected_response




