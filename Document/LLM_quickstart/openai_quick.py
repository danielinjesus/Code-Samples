from openai import OpenAI;from dotenv import load_dotenv;import os

# 기존 환경 변수 삭제 (캐시 초기화)
if "openai" in os.environ:
    del os.environ["openai"]

load_dotenv()

print(os.getenv("openai"))
openai = OpenAI(api_key=os.getenv("openai"), base_url="https://api.openai.com/v1")
gpt4_answer = openai.chat.completions.create(model="gpt-4o",messages=[
    {"role": "system", "content": "Respond like a casual friend."},
    {"role": "user", "content": "What is quantum mechanics?"}
]); print(f"openai 답변: {gpt4_answer.choices[0].message.content}")