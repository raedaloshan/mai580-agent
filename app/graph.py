from langgraph.graph import StateGraph, START, END
from app.state import State
from app.nodes import answer_course, answer_general, answer_gpa, answer_policy, call_model, analyze, generate, review 

def build_graph():
    builder = StateGraph(State)
   # builder.add_node("model", call_model)
   # builder.add_node("analyze", analyze)
   # builder.add_node("generate", generate)
   # builder.add_node("review", review)
   # builder.add_node("classify", classify)
    builder.add_node("answer_policy", answer_policy)
    builder.add_node("answer_course", answer_course)
    builder.add_node("answer_gpa", answer_gpa)
    builder.add_node("answer_general", answer_general) 


    # TODO: two edges
    # builder.add_edge(START, "model")
    # builder.add_edge("model",END)
    # builder.add_edge(START, "analyze")
    # builder.add_edge("analyze", "generate")
    # builder.add_edge("generate", "review")
    # builder.add_edge("review", END)

    builder.add_edge(START, "classify")
    builder.add_conditional_edges(
        "classify",
        route_by_intent,
        {"policy": "answer_policy", "course_info": "answer_course",
         "gpa": "answer_gpa", "planning": "answer_general", "other": "answer_general"},
    )

     for node in ["answer_policy", "answer_course", "answer_gpa", "answer_general"]:
        builder.add_edge(node, END)

    return builder.compile()
