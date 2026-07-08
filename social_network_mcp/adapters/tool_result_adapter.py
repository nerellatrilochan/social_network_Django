from typing import Any


def to_tool_result(result: dict[str, Any]) -> dict[str, Any]:
    """Normalize interactor/presenter output for MCP tool responses."""
    if not isinstance(result, dict):
        raise TypeError("Tool handler must return a dict response")

    if "ok" in result:
        return result

    return {
        "ok": True,
        "status": 200,
        "data": result,
    }
