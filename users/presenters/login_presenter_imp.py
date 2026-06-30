from django.http import response

from posts_auth.interactors.presenter_interfaces\
    .login_presenter_interface import \
    LoginPresenterInterface
from posts_auth.interactors.storage_interfaces.dtos import TokensDTO

INVALID_CREDENTIALS = (
    "Invalid Credentials. Please enter valid credentials or contact support.",
    "INVALID_CREDENTIALS"
)
USER_ACCOUNT_IS_DEACTIVATED = (
    "User Account is deactivated. Please contact support.",
    "USER_ACCOUNT_IS_DEACTIVATED"
)


class LoginPresenterImplementation(LoginPresenterInterface):
    def raise_invalid_credentials_exception(self):
        import json
        data = json.dumps({
            "response": INVALID_CREDENTIALS[0],
            "http_status_code": 403,
            "res_status": INVALID_CREDENTIALS[1]
        })

        response_object = response.HttpResponse(data, status=403)
        return response_object

    def raise_user_account_deactivated_exception(self):
        import json
        data = json.dumps({
            "response": USER_ACCOUNT_IS_DEACTIVATED[0],
            "http_status_code": 403,
            "res_status": USER_ACCOUNT_IS_DEACTIVATED[1]
        })

        response_object = response.HttpResponse(data, status=403)
        return response_object

    def get_response_for_login(self, token_dto: TokensDTO):
        import json
        data = json.dumps({
            "access_token": token_dto.access_token,
            "refresh_token": token_dto.refresh_token,
            "expires_in": token_dto.expires_in
        })

        response_object = response.HttpResponse(data, status=200)
        return response_object
