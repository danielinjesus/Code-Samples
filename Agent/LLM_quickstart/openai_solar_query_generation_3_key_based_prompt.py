from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
upstage = OpenAI(api_key=os.getenv("upstage"), base_url="https://api.upstage.ai/v1/solar");import pandas as pd; import json

def get_key(msg):
    solar_answer = upstage.chat.completions.create(
        model="solar-pro",
        messages=[
        {"role":"user","content":f"""

당신은 query 작성 Assistant다. 아래 규칙을 따른다:

- [사용자와의 기존 대화]를 참고하여, 사용자의 질문에 대한 답변이 되는 문서를 데이터베이스에서 검색하기 위한 한국어 query를 작성한다.
- query는 사용자의 질문사항을 가지고 만들어야 한다.
- 최대 길이는 30토큰 이내로 작성하라.
- 출력은 query외에 아무것도 없어야 한다.

[사용자와의 기존 대화]
{msg}
"""
}])    
    ans=solar_answer.choices[0].message.content
    print(ans)
    return ans

# JSONL 파일 불러오기
file_path='/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added_intent.jsonl' 
df=pd.read_json(file_path, lines=True)
df['query']=[get_key(msg) for msg in df['msg']]

print(df.head(30)) # 데이터프레임 확인

df.to_csv('/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added_keyword_query.csv', index=False, encoding='utf-8-sig')
df.to_json('/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added_keyword_query.jsonl',orient='records', lines=True, force_ascii=False)