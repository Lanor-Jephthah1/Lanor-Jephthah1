from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


QuestionType = Literal[
    "behavioral",
    "technical",
    "motivation",
    "background",
    "other",
]


@dataclass
class SuggestionBundle:
    question_type: QuestionType
    quick_reply: str
    standard_reply: str
    star_reply: str


def classify_question(text: str) -> QuestionType:
    t = text.lower()
    if "tell me about yourself" in t or "background" in t:
        return "background"
    if "conflict" in t or "time you" in t or "example" in t:
        return "behavioral"
    if "technical" in t or "challenge" in t or "system" in t:
        return "technical"
    if "why are you interested" in t or "why this role" in t:
        return "motivation"
    return "other"


def generate_suggestions(text: str, user_name: str = "Candidate") -> SuggestionBundle:
    qtype = classify_question(text)
    if qtype == "background":
        return SuggestionBundle(
            question_type=qtype,
            quick_reply="I focus on practical problem-solving and collaborative delivery.",
            standard_reply=(
                f"I am {user_name}, and my background combines strong technical foundations "
                "with real project execution. I enjoy solving user-facing problems, "
                "communicating clearly, and continuously improving my impact."
            ),
            star_reply=(
                "Situation: I needed to bridge technical and non-technical priorities. "
                "Task: Present my background with relevance to outcomes. "
                "Action: I highlighted measurable projects and teamwork. "
                "Result: Stakeholders quickly understood my fit and value."
            ),
        )

    if qtype == "behavioral":
        return SuggestionBundle(
            question_type=qtype,
            quick_reply="I address conflict by aligning on facts, goals, and shared outcomes.",
            standard_reply=(
                "When conflict appears, I first listen to each perspective, clarify the core issue, "
                "and align the team around common goals. I then propose a concrete path forward "
                "with clear ownership and follow-up."
            ),
            star_reply=(
                "Situation: Two teammates disagreed on implementation priorities. "
                "Task: Keep delivery on schedule while resolving tension. "
                "Action: I facilitated a short decision session using requirements and risks. "
                "Result: We agreed on a phased solution and delivered on time."
            ),
        )

    if qtype == "technical":
        return SuggestionBundle(
            question_type=qtype,
            quick_reply="I break technical challenges into diagnosable components and validate quickly.",
            standard_reply=(
                "For technical challenges, I define the failure clearly, gather evidence, and test "
                "small hypotheses. Once the root cause is confirmed, I implement a fix with "
                "monitoring and documentation to prevent recurrence."
            ),
            star_reply=(
                "Situation: A core workflow had unstable performance. "
                "Task: Restore reliability without halting delivery. "
                "Action: I profiled bottlenecks, optimized queries, and added alerting. "
                "Result: Response time improved and incidents dropped significantly."
            ),
        )

    if qtype == "motivation":
        return SuggestionBundle(
            question_type=qtype,
            quick_reply="I’m motivated by meaningful impact, growth, and team collaboration.",
            standard_reply=(
                "This role aligns with my strengths in problem-solving and communication. "
                "I’m especially interested in contributing to high-impact work while growing "
                "through collaboration and feedback."
            ),
            star_reply=(
                "Situation: I evaluated opportunities for long-term fit. "
                "Task: Choose a role with impact and growth potential. "
                "Action: I mapped team goals to my strengths and values. "
                "Result: I pursued roles where I can deliver results and learn quickly."
            ),
        )

    return SuggestionBundle(
        question_type=qtype,
        quick_reply="Could you please clarify the key point you’d like me to address?",
        standard_reply=(
            "I want to give you a precise answer. If you share which area to focus on, "
            "I can respond directly and concisely."
        ),
        star_reply=(
            "Situation: I received a broad prompt. Task: Provide a relevant answer. "
            "Action: I requested clarification to target the response. Result: Better alignment."
        ),
    )
