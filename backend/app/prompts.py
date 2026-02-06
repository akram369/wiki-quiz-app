QUIZ_PROMPT = """
You are a factual quiz generator.

Use ONLY the article content below.
If a fact is not explicitly present, DO NOT create a question.

Article Title: {title}

Article Content:
{content}

Generate 5–10 MCQs in STRICT JSON:
[
  {{
    "question": "...",
    "options": ["A", "B", "C", "D"],
    "answer": "...",
    "difficulty": "easy | medium | hard",
    "explanation": "Based on the article content"
  }}
]
"""

RELATED_TOPICS_PROMPT = """
Suggest 3–5 related Wikipedia topics.
Return ONLY a JSON array of strings.

Article Content:
{content}
"""
