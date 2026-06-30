from posts_auth.adapters.service_adapter import get_service_adapter
from posts_auth.interactors.presenter_interfaces.refresh_auth_tokens_presenter_interface import \
    RefreshAuthTokensPresenterInterface
from posts_auth.exceptions.custom_exceptions import (
    InvalidAccessTokenException, RefreshTokenExpiredException,
    UserAccountDeactivatedException, RefreshTokenNotFoundException
)


class RefreshAuthTokensInteractor:

    def refresh_auth_tokens_wrapper(self, access_token: str,
                                    refresh_token: str,
                                    presenter: RefreshAuthTokensPresenterInterface):
        try:
            auth_tokens_dto = self.refresh_auth_tokens(
                access_token=access_token,
                refresh_token=refresh_token
            )
        except InvalidAccessTokenException:
            return presenter.raise_invalid_access_token_exception()
        except RefreshTokenExpiredException:
            return presenter.raise_refresh_token_expired_exception()
        except UserAccountDeactivatedException:
            return presenter.raise_user_account_deactivated_exception()
        except RefreshTokenNotFoundException:
            return presenter.raise_refresh_token_not_found_exception()

        return presenter.get_response_for_refresh_auth_tokens(
            auth_tokens_dto=auth_tokens_dto
        )

    @staticmethod
    def refresh_auth_tokens(access_token: str, refresh_token: str):
        service_adapter = get_service_adapter()
        auth_tokens_dto = service_adapter.auth_service.refresh_auth_tokens(
            access_token=access_token,
            refresh_token=refresh_token
        )

        return auth_tokens_dto
