from langchain_core.messages import HumanMessage
from app.graph import build_graph, run_graph

graph = build_graph()

while True:
    question = input("you> ").strip()
    if question in {"exit", "quit"}:
        break
    out = run_graph(graph, {"messages": [HumanMessage(question)]})
    print("agent>", out["messages"][-1].content)