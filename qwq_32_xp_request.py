import requests
from dotenv import load_dotenv
import os

load_dotenv()

huggingface_token = os.getenv("HUGGINGFACE_API_KEY")

headers = {
    "Authorization": f"Bearer {huggingface_token}",
    "Content-Type": "application/json"
}

data = {
    "model": "Qwen/QwQ-32B",
    "messages": [
        {
            "role": "user",
            "content": "Qual a capital do Brasil?"
        }
    ],
    "max_tokens": 500,
    "stream": False
}

response = requests.post(
    "https://router.huggingface.co/hf-inference/models/Qwen/QwQ-32B/v1/chat/completions",
    headers=headers,
    json=data
)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code}")
    print(response.text)