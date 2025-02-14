import sys; sys.path.append("/data/ephemeral/home/upstageailab-llm-pjt-chatbot-1/Daun")
from Naver_Shopping.api_naver_shopping import naver;import json
from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
openai = OpenAI(api_key=os.getenv("openai"), base_url="https://api.openai.com/v1")
# ✅ 1. 네이버 검색 함수 정의
def naver(keyword):
    print(f"naver 검색 keyword: {keyword}")
    from dotenv import load_dotenv;import os,sys;import requests as req;import pandas as pd
    load_dotenv("/data/ephemeral/home/upstageailab-llm-pjt-chatbot-1/Daun/.env")
    client_id,client_secret=os.getenv("naverclient"),os.getenv("naversecret")
    sys.stdout.reconfigure(encoding='utf-8')# 콘솔 출력 인코딩을 UTF-8로 설정
    url="https://openapi.naver.com/v1/search/shop.json"
    headers={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
    params={"query":keyword,"display":10}
    res=req.get(url,headers=headers,params=params)
    res_json=res.json()['items']
    res_df=pd.DataFrame(res_json)
    return res_df, res_json

# ✅ 2. OpenAI GPT Function Calling 설정
functions = [{"name": "naver","description": "네이버 쇼핑에서 상품을 검색하는 함수",
        "parameters": {"type": "object","properties": {"keyword": {"type": "string", "description": "검색할 키워드"}},"required": ["keyword"],},}]

# ✅ 3. GPT-4에게 함수 호출 요청
gpt4_answer = openai.chat.completions.create(model="gpt-4",messages=[
    {"role": "system", "content": "너는 [내 개인 조리사 및 건강 관리사]야. 내 키, 체중, 혈당, 재료별 칼로리를 고려하여 건강당뇨식단을 추천한다."
     "너가 할 [임무] 1. 내 냉장고에 있는 식자재 목록을 알고 있다. 2. 식자재 목록을 나에게 받아서 업데이트 한다. 3. 현재 식자재 목록으로 할 수 있는 최적의 식사조리법을 가르쳐준다. 4. 기분에 따라 상황에 맞는 조리법을 권장하는데 이 때는 내가 해당 재료를 가지고 있는지 여부와 무관하게 추천한다. 5. 추천한 요리 중에서 내가 마음에 드는 요리가 생기면 거기에 필요한 재료 중 내 냉장고에 없는 재료 목록을 네이버 쇼핑에서 검색하라라"},
    {"role": "user", "content": "안녕 넌 누구니"}
    ], functions=functions, function_call="auto")
# ✅ 4. 함수 호출이 필요한지 확인
if gpt4_answer.choices[0].message.function_call:
    function_name = gpt4_answer.choices[0].message.function_call.name
    arguments = json.loads(gpt4_answer.choices[0].message.function_call.arguments)
    print(f"arguments: {arguments}")
    if function_name == "naver":
        # ✅ GPT가 `naver()`를 호출하라고 하면 실제 실행
        result_df, result_json = naver(**arguments)
        print("\n✅ 네이버 검색 결과:")
        print(result_json)
            # ✅ 5. GPT에게 결과를 다시 전달해서 분석 요청
        analysis_response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "아래 네이버 쇼핑 검색 결과를 분석하고 최적의 거래를 추천하세요."},
                {"role": "user", "content": json.dumps(result_json, ensure_ascii=False)}
            ]
        )

        # ✅ 6. GPT의 분석 결과 출력
        print("\n📝 GPT-4 분석 결과:")
        print(analysis_response.choices[0].message.content)
else:
    print(f"openai 답변: {gpt4_answer.choices[0].message.content}")