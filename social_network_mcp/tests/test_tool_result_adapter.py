import pytest

from social_network_mcp.adapters.tool_result_adapter import to_tool_result


class TestToolResultAdapter:

    def test_to_tool_result_passthrough(self):
        payload = {"ok": True, "status": 200, "data": {"post_id": 1}}
        assert to_tool_result(payload) == payload

    def test_to_tool_result_wraps_plain_dict(self):
        payload = {"post_id": 1}
        assert to_tool_result(payload) == {
            "ok": True,
            "status": 200,
            "data": {"post_id": 1},
        }

    def test_to_tool_result_rejects_non_dict(self):
        with pytest.raises(TypeError):
            to_tool_result("invalid")
