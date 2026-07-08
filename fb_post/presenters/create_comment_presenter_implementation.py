from django.http import HttpResponse

from dsu.runtime.mixin.http_response_mixin import HTTPResponseMixin

from fb_post.constants.exception_messages import (
    INVALID_COMMENT_CONTENT,
    INVALID_POST_BAD_REQUEST,
    INVALID_USER,
)
from fb_post.interactors.presenter_interfaces.create_comment_presenter_interface import (
    CreateCommentPresenterInterface,
)


class CreateCommentPresenterImplementation(
    CreateCommentPresenterInterface,
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

    def raise_invalid_comment_content_exception(self) -> HttpResponse:
        return self.prepare_400_bad_request_response({
            "response": INVALID_COMMENT_CONTENT[0],
            "http_status_code": 400,
            "res_status": INVALID_COMMENT_CONTENT[1],
        })

    def get_create_comment_response(self, comment_id: int) -> HttpResponse:
        return self.prepare_201_created_response({
            "comment_id": comment_id,
        })