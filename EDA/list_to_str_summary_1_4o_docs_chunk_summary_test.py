from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
openai=OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.openai.com/v1");import pandas as pd; import json

df=pd.read_csv('/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/documents.csv')

df_list=df['key'].astype(str).tolist()
df_str=" ".join(df_list) # 리스트를 공백으로 연결하여 출력
print(len(df_list))
chunk_size = 1100
chunks = [df_list[i:i + chunk_size] for i in range(0, len(df_list), chunk_size)]
# print(df_str)
for chunk in chunks:
    completion=openai.chat.completions.create(model="gpt-4o",messages=[
        {"role": "system", "content": f"""
    ## Role: 요약 전문가 ## Instructions:
    다음 내용을 참조하여, [주어진 내용]을 요약해.
    1. 문제의 배경은 과학상식 챗봇 구축할 때, 사용자가 챗봇에게 query를 주었을 때 어떤 방식으로 사용자에게 답변할지를 결정하기 위한 거야.
    2. 현재 작업의 목적은 기업 내부에 참조할 수 있는 데이터베이스의의 지식의 분야와 범위를 LLM에게 알려주는 거야. 그래서 LLM이 내부 데이터베이스를 참조할지 아니면 일반적인 채팅답변을 할지 결정할꺼야.
    3. LLM이 정확히 판단하기 위해, [주어진 내용]을 포괄하면서 요약해야 해.
    4. 네가 요약한 내용을 나중에 프롬프트에 넣어서 LLM이 내부 데이터베이스 내용의 범위를 알기 쉽게 해줄꺼야.
    5. 답변 총 길이는 30000토큰 미만으로 작성해.
    """},    
        {"role": "user", "content": f"""
        [주어진 내용]
        {chunk}
    """}])
    print(completion.choices[0].message.content)
    file_name="/data/ephemeral/home/Code-Samples/EDA/list_to_str_summary1_4o.json"
    with open(file_name, 'a', encoding='utf-8') as file:
        # 파일 끝에 줄 바꿈 추가
        file.write(json.dumps(df_str, ensure_ascii=False) + "\n")
        file.write(json.dumps(completion.choices[0].message.content, ensure_ascii=False) + "\n")