import json
import os
import re
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_quiz(title: str, summary: str):
    prompt = f"""
You are an expert quiz designer.

Create EXACTLY 5 DISTINCT multiple-choice questions
based ONLY on the article summary below.

CRITICAL RULES:
- Each question must test a DIFFERENT fact
- DO NOT repeat or rephrase the same question
- Cover different aspects (life, work, impact, institutions, legacy)
- Each question must have 4 options
- Only ONE option must be correct
- Difficulty should vary (easy, medium, hard)
- Explanations must reference a unique fact

Return ONLY valid JSON in the following format:

{{
  "quiz": [
    {{
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "...",
      "difficulty": "easy | medium | hard",
      "explanation": "..."
    }}
  ],
  "related_topics": ["topic1", "topic2", "topic3"]
}}

Article Title:
{title}

Article Summary:
{summary}
"""

    response = model.generate_content(prompt)
    text = response.text.strip()

    # Remove markdown if present
    text = re.sub(r"```json|```", "", text).strip()

    try:
        data = json.loads(text)
        quiz = data.get("quiz", [])
        related_topics = data.get("related_topics", [])
        return quiz, related_topics
    except Exception:
        # Safe fallback to prevent frontend crash
        return [], []
