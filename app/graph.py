from langgraph.graph import StateGraph, START, END
from app.state import State
from app.nodes import call_model


def build_graph():
    builder = StateGraph(State)
    builder.add_node("model", call_model)
    # TODO: two edges
    builder.add_edge(START, "model")
    builder.add_edge("model",END)
    return builder.compile()
