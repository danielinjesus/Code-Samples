from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
upstage = OpenAI(api_key=os.getenv("upstage"), base_url="https://api.upstage.ai/v1/solar");import pandas as pd

persona="""## Role: 요약 전문가 ## Instructions: 핵심주제를 키워드 몇 단어로 요약해"""

def get_key(x):
    completion = upstage.chat.completions.create(model="solar-pro",
    messages=[{"role": "system", "content": f"{persona}"},{"role": "user", "content": f"{x}"}])
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

file_path='/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/documents.jsonl' # JSONL 파일 불러오기
df=pd.read_json(file_path, lines=True)
df['key']=[get_key(content) for content in df['content']]

print(df.head(30)) # 데이터프레임 확인

df.to_csv('/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/documents.csv', index=False, encoding='utf-8-sig') # CSV 파일로 저장