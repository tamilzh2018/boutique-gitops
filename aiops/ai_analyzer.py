import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"


def analyze_incident(evidence):

    prompt = f"""
You are a Kubernetes SRE.

Analyze this incident:

{evidence}

Answer briefly:

INCIDENT:
What is happening?

ROOT CAUSE:
Most likely cause?

EVIDENCE:
Give 2 important pieces of evidence.

ACTION:
What should the engineer do?

CONFIDENCE:
High / Medium / Low
"""

    print("📤 Prompt size:", len(prompt), "characters")

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 100
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=180
    )

    response.raise_for_status()

    return response.json()["response"]