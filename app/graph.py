from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from app.state import State
from app.tools import TOOLS
from app.nodes import agent, final_answer


def build_graph():
    builder = StateGraph(State)
    builder.add_node("agent", agent)
    builder.add_node("tools", ToolNode(TOOLS))
    builder.add_node("final_answer", final_answer)

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)   # -> "tools" or END
    builder.add_edge("tools", "final_answer")
    builder.add_edge("final_answer", END)

    return builder.compile()