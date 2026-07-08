from fb_post.constants.exception_messages import (
    INVALID_POST_CONTENT,
    INVALID_USER,
)
from fb_post.interactors.presenter_interfaces.create_post_presenter_interface import (
    CreatePostPresenterInterface,
)
from social_network_mcp.presenters.mcp_response_mixin import McpResponseMixin


class McpCreatePostPresenter(
    CreatePostPresenterInterface,
    McpResponseMixin,
):

    def raise_invalid_user_exception(self) -> dict:
        return self.prepare_400_bad_request_response({
            "response": INVALID_USER[0],
            "http_status_code": 400,
            "res_status": INVALID_USER[1],
        })

    def raise_invalid_post_content_exception(self) -> dict:
        return self.prepare_400_bad_request_response({
            "response": INVALID_POST_CONTENT[0],
            "http_status_code": 400,
            "res_status": INVALID_POST_CONTENT[1],
        })

    def get_create_post_response(self, post_id: int) -> dict:
        return self.prepare_201_created_response({
            "post_id": post_id,
        })
