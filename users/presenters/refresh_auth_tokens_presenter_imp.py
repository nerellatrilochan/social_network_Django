from django.http import response

from posts_auth.adapters.dtos import UserAuthTokensDTO
from posts_auth.interactors.presenter_interfaces.refresh_auth_tokens_presenter_interface import \
    RefreshAuthTokensPresenterInterface

INVALID_ACCESS_TOKEN = (
    "Invalid access token",
    "INVALID_ACCESS_TOKEN"
)

REFRESH_TOKEN_EXPIRED = (
    "Refresh Token Expired",
    "REFRESH_TOKEN_EXPIRED"
)

USER_ACCOUNT_IS_DEACTIVATED = (
    "User Account is deactivated",
    "USER_ACCOUNT_IS_DEACTIVATED"
)

REFRESH_TOKEN_NOT_FOUND = (
    'Refresh token not found',
    'REFRESH_TOKEN_NOT_FOUND'
)


class RefreshAuthTokensPresenterImplementation(RefreshAuthTokensPresenterInterface):

    def raise_invalid_access_token_exception(self):
        import json
        data = json.dumps({
            "response": INVALID_ACCESS_TOKEN[0],
            "http_status_code": 400,
            "res_status": INVALID_ACCESS_TOKEN[1]
        })
        response_object = response.HttpResponse(data, status=400)
        return response_object

    def raise_refresh_token_expired_exception(self):
        import json
        data = json.dumps({
            "response": REFRESH_TOKEN_EXPIRED[0],
            "http_status_code": 400,
            "res_status": REFRESH_TOKEN_EXPIRED[1]
        })
        response_object = response.HttpResponse(data, status=400)
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

    def get_response_for_refresh_auth_tokens(self,
                                             auth_tokens_dto: UserAuthTokensDTO):
        import json
        data = json.dumps({
            "user_id": auth_tokens_dto.user_id,
            "access_token": auth_tokens_dto.access_token,
            "refresh_token": auth_tokens_dto.refresh_token,
            "expires_in": auth_tokens_dto.expires_in
        })
        response_object = response.HttpResponse(data, status=200)
        return response_object

    def raise_refresh_token_not_found_exception(self):
        import json
        data = json.dumps({
            "response": REFRESH_TOKEN_NOT_FOUND[0],
            "http_status_code": 404,
            "res_status": REFRESH_TOKEN_NOT_FOUND[1]
        })

        response_object = response.HttpResponse(data, status=404)
        return response_object
