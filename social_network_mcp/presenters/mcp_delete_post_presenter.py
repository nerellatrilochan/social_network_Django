from fb_post.constants.exception_messages import (
    INVALID_POST_BAD_REQUEST,
    INVALID_USER,
    USER_CANNOT_DELETE_POST,
)
from fb_post.interactors.presenter_interfaces.delete_post_presenter_interface import (
    DeletePostPresenterInterface,
)
from social_network_mcp.presenters.mcp_response_mixin import McpResponseMixin


class McpDeletePostPresenter(
    DeletePostPresenterInterface,
    McpResponseMixin,
):

    def raise_invalid_user_exception(self) -> dict:
        return self.prepare_400_bad_request_response({
            "response": INVALID_USER[0],
            "http_status_code": 400,
            "res_status": INVALID_USER[1],
        })

    def raise_invalid_post_exception(self) -> dict:
        return self.prepare_400_bad_request_response({
            "response": INVALID_POST_BAD_REQUEST[0],
            "http_status_code": 400,
            "res_status": INVALID_POST_BAD_REQUEST[1],
        })

    def raise_user_cannot_delete_post_exception(self) -> dict:
        return self.prepare_403_forbidden_response({
            "response": USER_CANNOT_DELETE_POST[0],
            "http_status_code": 403,
            "res_status": USER_CANNOT_DELETE_POST[1],
        })

    def get_delete_post_response(self) -> dict:
        return self.prepare_200_success_response({})
