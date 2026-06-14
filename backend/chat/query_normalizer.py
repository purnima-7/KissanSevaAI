import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

NORMALIZE_PROMPT = """
Rephrase the following question to match agricultural dataset style.

STRICT RULES:
- Do NOT add new pests, crops, or chemicals
- Do NOT remove any pests, crops, or chemicals
- Only rephrase wording
- Keep meaning EXACTLY the same
- Make it generic and dataset-like

Question:
{question}
"""

def normalize_question(question: str) -> str:
    """
    Converts user-style English question into dataset-style English question.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": NORMALIZE_PROMPT.format(question=question)}],
            temperature=0
        )

        if response and response.choices:
            return response.choices[0].message.content.strip()

    except Exception as e:
        print("Query normalization error:", e)

    # fallback → return original question
    return question
