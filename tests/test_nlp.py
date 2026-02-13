from inclusivoice.nlp import classify_question, generate_suggestions


def test_question_classification_behavioral() -> None:
    assert classify_question("Describe a time you handled conflict in a team") == "behavioral"


def test_generate_suggestions_returns_text() -> None:
    s = generate_suggestions("Why are you interested in this role?")
    assert s.question_type == "motivation"
    assert len(s.quick_reply) > 10
    assert "role" in s.standard_reply.lower() or "aligns" in s.standard_reply.lower()
