import json
import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = os.getenv("GROQ_API_URL", "https://api.groq.com/v1/generate")


def fallback_extract(text: str) -> dict:
    hcp_name_match = re.search(r"(Dr\.|Dr|Doctor)\s+[A-Z][a-z]+", text)
    sentiment = (
        "Positive"
        if "positive" in text.lower()
        else "Negative"
        if "negative" in text.lower()
        else "Neutral"
    )

    return {
        "hcp_name": hcp_name_match.group(0) if hcp_name_match else "",
        "interaction_type": "Meeting" if "meet" in text.lower() else "",
        "date": "",
        "time": "",
        "topics": text,
        "materials_shared": "Brochure" if "brochure" in text.lower() else "",
        "sample_distributed": "" if "sample" not in text.lower() else "Sample",
        "sentiment": sentiment,
        "outcomes": "",
        "summary": text,
    }


def extract_interaction_from_text(text: str) -> dict:
    if not GROQ_API_KEY:
        return fallback_extract(text)

    prompt = (
        "Extract HCP interaction details from the following note and return valid JSON with the keys: "
        "hcp_name, interaction_type, date, time, topics, materials_shared, sample_distributed, sentiment, outcomes, summary.\n\n"
        f"Note:\n{text}"
    )

    payload = {
        "model": "gemma2-9b-it",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2,
        "max_tokens": 512,
    }

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        text_output = data.get("choices", [{}])[0].get("message", {}).get("content", "")

        # Simple JSON extraction fallback
        match = re.search(r"\{.*\}", text_output, re.S)
        if match:
            try:
                parsed = json.loads(match.group(0))
                parsed["summary"] = parsed.get("summary", text)
                return parsed
            except json.JSONDecodeError:
                pass

    except Exception:
        pass

    return fallback_extract(text)
