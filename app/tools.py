import json
from pathlib import Path
from langchain_core.tools import tool

CATALOGUE = json.loads(Path("data/catalogue.json").read_text())
POINTS = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5, "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}


@tool
def calculate_gpa(courses: list[dict]) -> float:
    """Compute a GPA. Each course is {"credits": int, "grade": letter grade such as "B+"}."""
    total = sum(c["credits"] for c in courses)
    return round(sum(POINTS[c["grade"]] * c["credits"] for c in courses) / total, 2)


@tool
def get_course(code: str) -> dict:
    """Look up a course by code (e.g. "SE 444"): title, credits, prerequisites, semesters offered."""
    return CATALOGUE.get(code.upper(), {"error": f"No course {code}"})


@tool
def check_prerequisites(code: str, completed: list[str]) -> dict:
    """Check whether a student who completed the given course codes may register for a course."""
    course = CATALOGUE.get(code.upper())
    if course is None:
        return {"error": f"No course {code}"}
    missing = [p for p in course["prerequisites"] if p not in completed]
    return {"eligible": not missing, "missing": missing}


TOOLS = [calculate_gpa, get_course, check_prerequisites]