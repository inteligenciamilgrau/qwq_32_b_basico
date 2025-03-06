from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()

huggingface_token = os.getenv("HUGGINGFACE_API_KEY")

client = InferenceClient(
	provider="hf-inference",
	api_key=huggingface_token
)

messages = [
	{
		"role": "user",
		"content": "Qual a capital do Brasil?"
	}
]

completion = client.chat.completions.create(
    model="Qwen/QwQ-32B", 
	messages=messages, 
	max_tokens=500,
)

print(completion.choices[0].message)