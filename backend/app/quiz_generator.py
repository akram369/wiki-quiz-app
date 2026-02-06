import json
from google.generativeai import GenerativeModel
from google.api_core.exceptions import ResourceExhausted

MODEL = GenerativeModel("gemini-2.0-flash")


def generate_quiz(title: str, summary: str):
    prompt = f"""
Generate 5 quiz questions based ONLY on the content below.

Return ONLY valid JSON in this format:
{{
  "quiz": [
    {{
      "question": "",
      "options": ["A", "B", "C", "D"],
      "answer": "",
      "difficulty": "easy|medium|hard",
      "explanation": ""
    }}
  ],
  "related_topics": []
}}

Title: {title}
Summary: {summary}
"""

    try:
        response = MODEL.generate_content(prompt)
        data = json.loads(response.text)
        return data["quiz"], data["related_topics"]

    except ResourceExhausted:
        # ✅ FALLBACK (NO LLM)
        return fallback_quiz(title, summary)


def fallback_quiz(title: str, summary: str):
    quiz = [
        {
            "question": f"What is {title} best known for?",
            "options": [
                "Scientific research",
                "Mathematical contributions",
                "Historical importance",
                "All of the above"
            ],
            "answer": "All of the above",
            "difficulty": "easy",
            "explanation": "Based on the article summary."
        }
    ] * 5

    related_topics = [
        f"History of {title}",
        f"{title} contributions",
        "Computer science history"
    ]

    return quiz, related_topics
