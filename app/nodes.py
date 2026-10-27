from app.llm import model
from app.state import State
from typing import Literal
from pydantic import BaseModel, Field

#--------------------
from app.tools import TOOLS

model_with_tools = model.bind_tools(TOOLS)


def agent(state: State) -> dict:
    system = SystemMessage("You are an academic advisor. Use tools for course facts and arithmetic.")
    return {"messages": [model_with_tools.invoke([system] + state["messages"])]}


def final_answer(state: State) -> dict:
    return {"messages": [model.invoke(state["messages"])]}

#--------------------

Intent = Literal["policy", "course_info", "gpa", "planning", "other"]


class Classification(BaseModel):
    intent: Intent = Field(description="The single best category for the request")


classifier = model.with_structured_output(Classification)


def classify(state: State) -> dict:
    system = SystemMessage(
        "Classify the student's latest request. "
        "policy = university rules; course_info = a specific course; "
        "gpa = grade calculations; planning = choosing future courses; other = anything else."
    )
    result = classifier.invoke([system] + state["messages"])
    return {"intent": result.intent}


def route_by_intent(state: State) -> str:
    return state["intent"]

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


def _answer(state: State, instructions: str) -> dict:
    """Shared helper: call the model with a branch-specific system prompt."""
    reply = model.invoke([SystemMessage(instructions)] + state["messages"])
    return {"messages": [reply]}


def answer_policy(state: State) -> dict:
    return _answer(state, "You are an academic advisor answering questions about university rules "
                          "and regulations. If you are not sure of a rule, say so.")


def answer_course(state: State) -> dict:
    return _answer(state, "You are an academic advisor answering questions about a specific course: "
                          "content, prerequisites, credits. If you do not know the details, say so.")


def answer_gpa(state: State) -> dict:
    return _answer(state, "You are an academic advisor helping with grade and GPA calculations. "
                          "Show each step of the calculation.")


def answer_general(state: State) -> dict:
    return _answer(state, "You are a helpful academic advisor. Help with course planning "
                          "and general student questions.")


