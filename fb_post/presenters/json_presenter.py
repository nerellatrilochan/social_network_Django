from dsu.runtime.mixin.http_response_mixin import HTTPResponseMixin


class JsonPresenter(HTTPResponseMixin):
    def raise_exception_for_invalid_user(self):
        return self.prepare_400_bad_request_response({
            "response": "Invalid user",
            "http_status_code": 400,
            "res_status": "INVALID_USER_EXCEPTION",
        })

    def raise_exception_for_invalid_post_content(self):
        return self.prepare_400_bad_request_response({
            "response": "Invalid post content",
            "http_status_code": 400,
            "res_status": "INVALID_POST_CONTENT",
        })

    def raise_exception_for_invalid_comment_content(self):
        return self.prepare_400_bad_request_response({
            "response": "Invalid comment content",
            "http_status_code": 400,
            "res_status": "INVALID_COMMENT_CONTENT",
        })

    def raise_exception_for_invalid_post(self):
        return self.prepare_404_not_found_response({
            "response": "Post not found",
            "http_status_code": 404,
            "res_status": "INVALID_POST_EXCEPTION",
        })

    def raise_exception_for_invalid_post_bad_request(self):
        return self.prepare_400_bad_request_response({
            "response": "Invalid post",
            "http_status_code": 400,
            "res_status": "INVALID_POST_EXCEPTION",
        })

    def raise_exception_for_invalid_reaction_type(self):
        return self.prepare_400_bad_request_response({
            "response": "Invalid reaction type",
            "http_status_code": 400,
            "res_status": "INVALID_REACTION_TYPE_EXCEPTION",
        })

    def raise_exception_for_user_cannot_delete_post(self):
        return self.prepare_400_bad_request_response({
            "response": "User cannot delete post",
            "http_status_code": 400,
            "res_status": "USER_CANNOT_DELETE_POST_EXCEPTION",
        })