from langgraph.graph import StateGraph, START, END
from app.state import State
from app.nodes import (classify, route_by_intent,
                       answer_policy, answer_course, answer_gpa, answer_general)


def build_graph():
    builder = StateGraph(State)
    builder.add_node("classify", classify)
    builder.add_node("answer_policy", answer_policy)
    builder.add_node("answer_course", answer_course)
    builder.add_node("answer_gpa", answer_gpa)
    builder.add_node("answer_general", answer_general)

    builder.add_edge(START, "classify")
    builder.add_conditional_edges(
        "classify",
        route_by_intent,
        {"policy": "answer_policy", "course_info": "answer_course",
         "gpa": "answer_gpa", "planning": "answer_general", "other": "answer_general"},
    )
    builder.add_edge("answer_policy", END)
    builder.add_edge("answer_course", END)
    builder.add_edge("answer_gpa", END)
    builder.add_edge("answer_general", END)

    return builder.compile()