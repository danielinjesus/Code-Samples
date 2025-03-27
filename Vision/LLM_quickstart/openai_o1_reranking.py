from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.openai.com/v1");import pandas as pd; import json

def get_key(msg):
    completion=openai.chat.completions.create(model="o1-preview",messages=[{"role":"user","content":f"""
- 너는 채팅 사용자의 의도를 분류해서 응대하는 안내원이야.
- 너는 [사용자와의 기존 대화]를 마지막까지 읽고 사용자를 분류해.
- 사용자가 "안녕, 잘 있었어", "나 오늘 너무 슬퍼", "너 누구야?" 등 정서적인 공감이나 일상적인 대화를 원하는지 아니면 어떤 객관적인 사실에 대한 '지식'을 알고 싶어 하는지 분류해야 해.
- 사용자가 일상적인 대화를 원하면 '0', 과학적인 지식을 궁금해하면 '1'을 반환해
- 답변은 오직 한개의 숫자로 출력해야 해.

[사용자와의 기존 대화]
{msg}
"""}])    
    ans=completion.choices[0].message.content
    print(ans)
    return ans

# JSONL 파일 불러오기
file_path='/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval.jsonl' 
df=pd.read_json(file_path, lines=True)
df['intent']=[get_key(msg) for msg in df['msg']]

# # 칼럼 분류하기
# def parse_key(json_str):
#     try:
#         data = json.loads(json_str)
#         return data.get('intent',0), data.get('query',"")
#     except json.JSONDecodeError:
#         # JSON 파싱 실패 시 기본값 반환
#         return 0, ""
# df['intent'], df['query'] = zip(*df['key'].apply(parse_key))

print(df.head(30)) # 데이터프레임 확인

df.to_csv('/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added.csv', index=False, encoding='utf-8-sig')
df.to_json('/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added.jsonl',orient='records', lines=True, force_ascii=False)