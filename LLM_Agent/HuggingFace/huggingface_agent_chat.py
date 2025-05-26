from dotenv import load_dotenv; load_dotenv(); import os
from huggingface_hub import InferenceClient
os.environ["HF_TOKEN"] = os.getenv("HF_TOKEN")

# 챗봇 기능이 지원되는 공개 모델 예시 (mistralai/Mistral-7B-Instruct-v0.2)
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.2")

# 대화 이력 예시
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "The capital of France is"},
]

output = client.chat_completion(
    messages=messages
)

print(output)