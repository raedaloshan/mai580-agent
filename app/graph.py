from langchain_core.messages import AIMessage
from langgraph.errors import GraphRecursionError
from langgraph.graph import StateGraph, START
from langgraph.prebuilt import ToolNode, tools_condition
from app.state import State
from app.tools import TOOLS
from app.nodes import agent


def build_graph():
    builder = StateGraph(State)
    builder.add_node("agent", agent)
    builder.add_node("tools", ToolNode(TOOLS))

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)   # -> "tools" or END
    builder.add_edge("tools", "agent")                        # was: "tools" -> "final_answer"

    return builder.compile()


def run_graph(graph, inputs):
    try:
        return graph.invoke(inputs, {"recursion_limit": 12})
    except GraphRecursionError:
        return {"messages": [AIMessage("I could not finish this request within my step budget.")]}