from django.http import HttpResponse

from dsu.runtime.mixin.http_response_mixin import HTTPResponseMixin

from fb_post.constants.exception_messages import (
    INVALID_POST_CONTENT,
    INVALID_USER,
)
from fb_post.interactors.presenter_interfaces.create_post_presenter_interface import (
    CreatePostPresenterInterface,
)


class CreatePostPresenterImplementation(
    CreatePostPresenterInterface,
    HTTPResponseMixin,
):

    def raise_invalid_user_exception(self) -> HttpResponse:
        return self.prepare_400_bad_request_response({
            "response": INVALID_USER[0],
            "http_status_code": 400,
            "res_status": INVALID_USER[1],
        })

    def raise_invalid_post_content_exception(self) -> HttpResponse:
        return self.prepare_400_bad_request_response({
            "response": INVALID_POST_CONTENT[0],
            "http_status_code": 400,
            "res_status": INVALID_POST_CONTENT[1],
        })

    def get_create_post_response(self, post_id: int) -> HttpResponse:
        return self.prepare_201_created_response({
            "post_id": post_id,
        })