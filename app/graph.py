from langgraph.graph import StateGraph, START, END
from app.state import State
from app.nodes import call_model, analyze, generate, review 

def build_graph():
    builder = StateGraph(State)
   # builder.add_node("model", call_model)
    builder.add_node("analyze", analyze)
    builder.add_node("generate", generate)
    builder.add_node("review", review)

    # TODO: two edges
    # builder.add_edge(START, "model")
    # builder.add_edge("model",END)
    builder.add_edge(START, "analyze")
    builder.add_edge("analyze", "generate")
    builder.add_edge("generate", "review")
    builder.add_edge("review", END)

    return builder.compile()
