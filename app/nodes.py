from app.llm import model
from app.state import State


def call_model(state: State) -> dict:
    reply = model.invoke(state["messages"])
    return {"messages": [reply]}          # an update, not the whole state


from langchain_core.messages import AIMessage, SystemMessage

def analyze(state: State) -> dict:
    prompt = SystemMessage(
        "Restate the student's request in one sentence and list the facts needed to answer it."
    )
    return {"analysis": model.invoke([prompt] + state["messages"]).content}


def generate(state: State) -> dict:
    prompt = SystemMessage(f"You are an academic advisor. Request analysis:\n{state['analysis']}")
    return {"draft": model.invoke([prompt] + state["messages"]).content}


def review(state: State) -> dict:
    prompt = SystemMessage(
        "Rewrite the draft so it is correct, polite, and under 120 words. "
        "If it states a fact you cannot verify, say so explicitly.\n\nDRAFT:\n" + state["draft"]
    )
    final = model.invoke([prompt]).content
    return {"messages": [AIMessage(final)]}