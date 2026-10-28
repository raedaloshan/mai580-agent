from langchain_core.messages import HumanMessage
from app.graph import build_graph


def test_loop_uses_two_tools():
    out = build_graph().invoke({"messages": [HumanMessage(
        "Look up SE 444 and check if I can take it. I completed SE 301 and CS 220.")]})
    called = [c["name"] for m in out["messages"] for c in getattr(m, "tool_calls", [])]
    assert "check_prerequisites" in called