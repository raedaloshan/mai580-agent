from langchain_core.messages import HumanMessage
from app.graph import build_graph

graph = build_graph()

for update in graph.stream({"messages": [HumanMessage("Can I take 21 credits?")]},
                           stream_mode="updates"):
    print(update)