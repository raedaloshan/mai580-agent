import pytest
from langchain_core.messages import HumanMessage
from app.graph import build_graph


@pytest.mark.parametrize("text,intent", [
    ("What is my GPA if I got A in 3 credits and B in 4?", "gpa"),
    ("Can I withdraw after week 10?", "policy"),
])
def test_router(text, intent):
    out = build_graph().invoke({"messages": [HumanMessage(text)]})
    assert out["intent"] == intent
