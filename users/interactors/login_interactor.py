
from posts_auth.interactors.presenter_interfaces\
    .login_presenter_interface import \
    LoginPresenterInterface
from posts_auth.interactors.storage_interfaces.dtos import \
    TokensDTO


class LoginInteractor:

    def login_wrapper(self, client_id: str, code: str,
                      presenter: LoginPresenterInterface):
        from ib_user_accounts_helper.exceptions.custom_exceptions import InvalidCredentialsException
        from posts_auth.exceptions.custom_exceptions import UserAccountIsDeactivatedException
        try:
            token_dto = self.login(client_id=client_id, code=code)
        except InvalidCredentialsException:
            return presenter.raise_invalid_credentials_exception()
        except UserAccountIsDeactivatedException:
            return presenter.raise_user_account_deactivated_exception()
        return presenter.get_response_for_login(token_dto=token_dto)

    # ruff: noqa: ARG004
    @staticmethod
    def login(client_id: str, code: str) -> TokensDTO:
        from posts_auth.adapters.service_adapter import \
            get_service_adapter

        service_adapter = get_service_adapter()
        auth_service = service_adapter.auth_service

        ib_user_auth_tokens_dto = auth_service.get_ib_accounts_access_token(
            code=code)
        user_id = ib_user_auth_tokens_dto.user_id
        auth_service.create_ib_accounts_auth_tokens(
            user_id=user_id,
            access_token=ib_user_auth_tokens_dto.access_token,
            refresh_token=ib_user_auth_tokens_dto.refresh_token,
            expires_in=ib_user_auth_tokens_dto.expires_in

        )

        from posts_auth.adapters.service_adapter import ServiceAdapter
        adapter = ServiceAdapter()
        adapter.auth_service.create_user_in_ib_users(user_id=user_id)
        app_auth_tokens_dto = auth_service.get_access_token(
            user_id=user_id)

        return app_auth_tokens_dto
