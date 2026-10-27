from typing import Annotated
from typing_extensions import TypedDict
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class State(TypedDict, total=False):
    messages: Annotated[list[AnyMessage], add_messages]   # Stage 1
    analysis: str      # Stage 2: what the user is really asking
    draft: str         # Stage 2: first answer before review
    intent: str       # Stage 3: what the user is really asking
    # later stages add fields here — never create a second state class
