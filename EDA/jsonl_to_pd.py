from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
client = OpenAI(api_key=os.getenv("grok"),base_url="https://api.x.ai/v1");import pandas as pd
persona="""
## Role: 요약 전문가
## Instructions
- 핵심을 몇 단어로 요약해
"""

file_path='/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/documents.jsonl' # JSONL 파일 불러오기
df = pd.read_json(file_path, lines=True)
df['key']=[get_key(content) for content in df['content']]

def get_key(x):
    completion = client.chat.completions.create(model="grok-2-latest",
    messages=[{"role": "system", "content": f"{persona}"},{"role": "user", "content": f"{x}"}])
    return completion.choices[0].message.content
print(df.head(30)) # 데이터프레임 확인