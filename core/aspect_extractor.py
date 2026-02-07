from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

MAX_ASPECTS = 3


def extract_query_aspects(query: str) -> List[Dict]:
    """
    Extract concrete, retrievable aspects from a user query.
    """

    prompt = f"""
You are a retrieval auditor.

Break the following user query into at most {MAX_ASPECTS}
clear, factual aspects that can be directly supported by documents.

Rules:
- Do NOT ask questions
- Do NOT explain
- Do NOT include filler text
- Each aspect must be a short noun phrase
- Output ONLY a bullet list

User query:
{query}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You extract factual retrieval aspects."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.0
    )

    raw = response.choices[0].message.content.strip()

    aspects = []
    for i, line in enumerate(raw.split("\n")):
        line = line.strip("-• ").strip()
        if len(line) < 5:
            continue

        aspects.append({
            "aspect_id": f"A{i+1}",
            "aspect_text": line
        })

    return aspects[:MAX_ASPECTS]
