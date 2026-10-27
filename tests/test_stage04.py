from app.tools import calculate_gpa, check_prerequisites

def test_gpa_tool():
    assert calculate_gpa.invoke({"courses": [{"credits": 3, "grade": "A"},
                                             {"credits": 3, "grade": "C"}]}) == 3.0

def test_prereq_tool():
    out = check_prerequisites.invoke({"code": "SE 444", "completed": ["SE 301"]})
    assert out == {"eligible": False, "missing": ["CS 220"]}
    