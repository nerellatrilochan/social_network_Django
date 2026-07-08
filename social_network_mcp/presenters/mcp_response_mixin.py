from typing import Any


class McpResponseMixin:
    """Build structured MCP responses mirroring HTTPResponseMixin shapes."""

    def prepare_200_success_response(self, response_data: dict) -> dict:
        return {
            "ok": True,
            "status": 200,
            "data": response_data,
        }

    def prepare_201_created_response(self, response_data: dict) -> dict:
        return {
            "ok": True,
            "status": 201,
            "data": response_data,
        }

    def prepare_400_bad_request_response(self, response_data: dict) -> dict:
        return self._prepare_error_response(400, response_data)

    def prepare_403_forbidden_response(self, response_data: dict) -> dict:
        return self._prepare_error_response(403, response_data)

    def prepare_404_not_found_response(self, response_data: dict) -> dict:
        return self._prepare_error_response(404, response_data)

    @staticmethod
    def _prepare_error_response(status: int, response_data: dict[str, Any]) -> dict:
        return {
            "ok": False,
            "status": status,
            "error": response_data,
        }
