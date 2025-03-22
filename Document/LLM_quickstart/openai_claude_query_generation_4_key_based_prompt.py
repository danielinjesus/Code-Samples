from openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
import json

from dotenv import load_dotenv;load_dotenv();import anthropic, os

client = anthropic.Anthropic(api_key=os.getenv("claude"))

def get_key(msg):
    message = client.messages.create(model="claude-3-7-sonnet-20250219",max_tokens=1024,
        messages=[
            {"role": "user", "content": f"""
## 역할 ##
당신은 query 작성 전문 Assistant다. 아래 규칙을 따른다.

## 현재 상황 ##
사용자의 질문과 연관되는 문서를 데이터베이스에서 검색하기 위한한 query가 필요해

## 지시사항 ##
1. [사용자와의 기존 대화]를 참고해
2. 사용자의 질문에 기반한 query를 작성해.
3. 영어로 된 단어가 있으면 한국어로 번역해.
4. 고유명사 등 영어로 쓰는 것이 자연스럽다면, 영어와 한국어를 함께 적어줘

## 예시 ##
질문 : [{{"role": "user", "content": "나무의 분류에 대해 조사해 보기 위한 방법은?"}}]
답변 : 나무 분류 조사 방법

## 실제 ##
질문 : {msg}
답변 :
"""
            }
        ]
    )
    print(message.content[0].text)
    return message.content[0].text

# JSONL 파일 불러오기
file_path = '/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added_intent.jsonl'
df = pd.read_json(file_path, lines=True)
df['query'] = [get_key(msg) for msg in df['msg']]

print(df.head(30))
df.to_json('/data/ephemeral/home/upstageailab-ir-competition-ir_s3/baseline/data/eval_added_keyword_query.jsonl',
           orient='records', lines=True, force_ascii=False)