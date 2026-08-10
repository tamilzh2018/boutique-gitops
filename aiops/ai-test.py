import requests

url = "http://localhost:11434/api/generate"

payload = {
    "model": "mistral",
    "prompt": "Why is Kubernetes Pod CrashLoopBackOff happening?.",
    "stream": False
}

response = requests.post(url, json=payload, timeout=120)

print("Status:", response.status_code)
print("Raw response:", response.text)

response.raise_for_status()

data = response.json()
print(data["response"])