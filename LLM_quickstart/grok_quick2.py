import json;file_path='/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/documents.jsonl'

with open(file_path, 'r') as file:
    documents = [json.loads(line) for line in file]



from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
client = OpenAI(api_key=os.getenv("grok"),base_url="https://api.x.ai/v1")

persona="""
## Role: 요약 전문가
## Instructions
- 핵심을 몇 단어로 요약해
"""

completion = client.chat.completions.create(
  model="grok-2-latest",
  messages=[{"role": "system", "content": f"{persona}"},{"role": "user", "content": f"{documents}"}]
); print(f"grok 답변: {completion.choices[0].message.content}")