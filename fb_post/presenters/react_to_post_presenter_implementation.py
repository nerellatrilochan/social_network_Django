from django.http import HttpResponse

from dsu.runtime.mixin.http_response_mixin import HTTPResponseMixin

from fb_post.constants.exception_messages import (
    INVALID_POST_BAD_REQUEST,
    INVALID_REACTION_TYPE,
    INVALID_USER,
)
from fb_post.interactors.presenter_interfaces.react_to_post_presenter_interface import (
    ReactToPostPresenterInterface,
)


class ReactToPostPresenterImplementation(
    ReactToPostPresenterInterface,
    HTTPResponseMixin,
):

    def raise_invalid_user_exception(self) -> HttpResponse:
        return self.prepare_400_bad_request_response({
            "response": INVALID_USER[0],
            "http_status_code": 400,
            "res_status": INVALID_USER[1],
        })

    def raise_invalid_post_exception(self) -> HttpResponse:
        return self.prepare_400_bad_request_response({
            "response": INVALID_POST_BAD_REQUEST[0],
            "http_status_code": 400,
            "res_status": INVALID_POST_BAD_REQUEST[1],
        })

    def raise_invalid_reaction_type_exception(self) -> HttpResponse:
        return self.prepare_400_bad_request_response({
            "response": INVALID_REACTION_TYPE[0],
            "http_status_code": 400,
            "res_status": INVALID_REACTION_TYPE[1],
        })

    def get_react_to_post_response(self) -> HttpResponse:
        return self.prepare_200_success_response({})