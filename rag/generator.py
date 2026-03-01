import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_answer(question, contexts):
    """
    Generate grounded answer using retrieved contexts.
    Returns:
        answer (str)
        confidence (float)
    """

    # ---------- If no context found ----------
    if not contexts or len(contexts) == 0:
        return "Not found in references.", 0.0

    # Combine context text
    context_text = "\n\n".join(contexts)

    prompt = f"""
You are a compliance assistant.

Rules:
- Answer ONLY using the reference text.
- Do NOT make assumptions.
- If information is not present, reply exactly: Not found in references.
- Keep answer short and factual.

Reference:
{context_text}

Question:
{question}
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        answer = response["choices"][0]["message"]["content"].strip()

    # ---------- If API fails ----------
    except Exception as e:
        print("OpenAI Error:", e)
        return "Error generating answer.", 0.0

    # ---------- Confidence logic ----------
    if "Not found in references" in answer:
        confidence = 0.2
    else:
        confidence = 0.9

    return answer, confidence