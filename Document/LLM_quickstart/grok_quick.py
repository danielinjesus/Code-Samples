import json

file_path = '/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/documents.jsonl'

with open(file_path, 'r') as file:
    documents = [json.loads(line) for line in file]

# 확인
# for doc in documents[:5]:  # 처음 5개만 출력
#     print(doc)


from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
    
client = OpenAI(api_key=os.getenv("grok"),base_url="https://api.x.ai/v1")

persona="""
## Role: 검색 및 요약 전문가
## Instructions
- 사용자가 질문한 내용이 {documents}에 있으면 어떤 action을 하도록 판단하기 위한 prompt를 만들꺼야
- 그 prompt에는 {documents}의 내용요약을 주어서 LLM의 판단을 도와줄꺼야.
- 위 지시대로 Prompt 내용을 작성해.
"""

completion = client.chat.completions.create(
  model="grok-2-latest",
  messages=[{"role": "system", "content": f"{persona}"},{"role": "user", "content": f"{documents}"}]
); print(f"grok 답변: {completion.choices[0].message.content}")