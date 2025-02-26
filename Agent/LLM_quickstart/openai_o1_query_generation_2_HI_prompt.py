from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.openai.com/v1");import pandas as pd; import json

def get_key(msg):
    completion=openai.chat.completions.create(model="o1-preview",messages=[
        {"role":"user","content":f"""

당신은 과학 상식 AI Assistant다. 아래 규칙을 따른다:
- 사용자의 질문에 대한 답변이 되는 문서를 데이터베이스에서 검색하기 위해서 query를 작성한다.
- query는 사용자의 질문사항을 가지고 만들어야 한다.
- 출력은 query외에 아무것도 없어야 한다.
- 데이터베이스는 과학상식 데이터베이스이다. 
- 과학상식의 범위는 다음과 같다

인문학: 역사, 문학, 철학, 예술
사회과학: 경제학, 정치학, 심리학, 사회학
자연과학: 물리학, 화학, 생물학, 지구과학
수학 및 컴퓨터과학: 수학(대수, 기하, 미적분), 알고리즘, 프로그래밍
기타: 의학, 법학, 교육학, 종교학, 언어학
물리학: 물질, 에너지, 운동, 열, 전기
화학: 원소, 화합물, 화학 반응
생물학: 세포, 유전, 생태계, 인체
지구과학: 지질, 기후, 천문학

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

df.to_csv('/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added_query_HI.csv', index=False, encoding='utf-8-sig')
df.to_json('/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added_query_HI.jsonl',orient='records', lines=True, force_ascii=False)