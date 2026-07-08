import pytest

from social_network_mcp.presenters.mcp_create_post_presenter import (
    McpCreatePostPresenter,
)
from social_network_mcp.presenters.mcp_response_mixin import McpResponseMixin


class TestMcpResponseMixin:

    def test_prepare_201_created_response(self):
        mixin = McpResponseMixin()
        result = mixin.prepare_201_created_response({"post_id": 42})

        assert result == {
            "ok": True,
            "status": 201,
            "data": {"post_id": 42},
        }

    def test_prepare_400_bad_request_response(self):
        mixin = McpResponseMixin()
        result = mixin.prepare_400_bad_request_response({
            "response": "Invalid user",
            "http_status_code": 400,
            "res_status": "INVALID_USER_EXCEPTION",
        })

        assert result["ok"] is False
        assert result["status"] == 400
        assert result["error"]["res_status"] == "INVALID_USER_EXCEPTION"


class TestMcpCreatePostPresenter:

    def test_get_create_post_response(self):
        presenter = McpCreatePostPresenter()
        result = presenter.get_create_post_response(post_id=10)

        assert result["ok"] is True
        assert result["status"] == 201
        assert result["data"] == {"post_id": 10}

    def test_raise_invalid_user_exception(self):
        presenter = McpCreatePostPresenter()
        result = presenter.raise_invalid_user_exception()

        assert result["ok"] is False
        assert result["status"] == 400
        assert result["error"]["res_status"] == "INVALID_USER_EXCEPTION"
