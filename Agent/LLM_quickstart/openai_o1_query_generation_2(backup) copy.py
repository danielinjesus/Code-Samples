from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.openai.com/v1");import pandas as pd; import json

def get_key(msg):
    completion=openai.chat.completions.create(model="o1-preview",messages=[{"role":"user","content":f"""
- 너는 query문을 생성하는 전문가야
- 너는 [사용자와의 기존 대화]를 마지막까지 차분히 읽고 사용자가 궁금해하는 내용을 한 개의 query문으로 만들어.
- 그 query문은 나중에 벡터화되서, 내부 벡터 데이터베이스에서 사용자 질문과 관련한 문서를 찾아오는 retrieval system의 검색 query로 사용될꺼야. 
- 현재 retrieval system은 elasticsearch, KR-SBERT와 BGE-M3를 사용 중이야.
- 사용자의 질문과 관련있는 문서를 정확하게 retrieval 할 수 있는 query문을 만들어줘.
- 답변은 한 개의 query문으로만 출력해야 해.
- query문은 한국어로 작성해야 해.

[사용자와의 기존 대화]
{msg}
"""
}])    
    ans=completion.choices[0].message.content
    print(ans)
    return ans

# JSONL 파일 불러오기
file_path='/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added_intent.jsonl' 
df=pd.read_json(file_path, lines=True)
df['query']=[get_key(msg) for msg in df['msg']]

print(df.head(30)) # 데이터프레임 확인

df.to_csv('/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added_query.csv', index=False, encoding='utf-8-sig')
df.to_json('/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added_query.jsonl',orient='records', lines=True, force_ascii=False)