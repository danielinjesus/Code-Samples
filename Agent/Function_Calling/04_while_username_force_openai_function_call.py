import sys,json,os;from dotenv import load_dotenv;load_dotenv("/data/ephemeral/home/upstageailab-llm-pjt-chatbot-1/Daun/.env")
import requests as req;from openai import OpenAI;openai=OpenAI(api_key=os.getenv("openai"),base_url="https://api.openai.com/v1")
sys.stdout.reconfigure(encoding='utf-8')# 콘솔 출력 인코딩을 UTF-8로 설정 
from google.cloud import firestore;from google.oauth2 import service_account
SERVICE_ACCOUNT_FILE="/data/ephemeral/home/upstageailab-llm-pjt-chatbot-1/TeamCode/token/upstageailab5-llm-pjt-985da1d6a634.json"
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE);db=firestore.Client(credentials=credentials)
def naver(keyword): # ✅ 1. 함수 정의 (네이버 상품 조회)
    url="https://openapi.naver.com/v1/search/shop.json"
    headers={"X-Naver-Client-Id":os.getenv("naverclient"),"X-Naver-Client-Secret":os.getenv("naversecret")}
    try:
        params={"query":keyword,"display":10}
        print(f"naver 검색 keyword:{keyword}")
        res=req.get(url,headers=headers,params=params)        
    except Exception as e: return f"❌ Error: {e}"
    return res.json()['items']
def retrieve_food(username): # ✅ 2. 함수 정의 (냉장고 털기)
    user=db.collection("users").document(username)
    try:
        user_food=user.get()
        if user_food.exists:
            data=user_food.to_dict()
            filtered_data={k: v for k, v in data.items() if k not in ["username","password","created_at"]}
            return filtered_data
        else: return "❌ 존재하지 않는 계정입니다."
    except Exception as e: return f"❌ 에러 발생: {e}"    
functions=[{"name": "naver","description": "네이버 쇼핑에서 여러 개의 키워드를 검색하는 함수", # ✅ 3.  GPT Function Calling 설정
        "parameters": {"type": "object","properties": {"keyword": {"type":"string", "description": "검색할 키워드"}},"required": ["keyword"],},}]             
sys_message={"role": "system", "content": ("너는 [내 개인 조리사 및 건강 관리사]야. 내 키, 체중, 혈당, 재료별 칼로리를 고려하여 건강당뇨식단을 추천한다."
        "너가 할 [구체적 임무] 1. 한국어로 대답한다."
        "2. 요청 시 현재 식자재 목록으로 할 수 있는 최적의 식사조리법과 재료, 칼로리, 혈당 관점에서 가르쳐준다."
        "3. 필요한 재료 중 냉장고에 없는 재료들 중 사용자가 원하는 것은 [naver함수] 호출하여 좋은 deal을 제안하라")}
threads=[];threads.append(sys_message)
# ✅ 4. 대화 시작 : 이름 입력, 개인정보 추출
result=retrieve_food(input('사용자이름: '));print("내 냉장고 음식들과 건강정보:");print(result)
threads.append({"role":"assistant","content":json.dumps(result,ensure_ascii=False)})
while True:
    user_input={"role": "user", "content": f"{input()}.한국어로 대답하라"}; threads.append(user_input)
    gpt4_answer=openai.chat.completions.create(model="gpt-4",messages=threads,functions=functions,function_call="auto")
    if gpt4_answer.choices[0].message.function_call: # ✅ 5. 함수 호출이 필요한지 확인
        function_name=gpt4_answer.choices[0].message.function_call.name
        arguments=json.loads(gpt4_answer.choices[0].message.function_call.arguments); print(f"arguments: {arguments}")        
        if function_name=="naver":   # ✅ 5-1. GPT가 `naver()`를 호출
            result_json=naver(arguments["keyword"]);print("\n✅ 네이버 검색 결과:");print(result_json)
            threads.append({"role":"assistant","content":json.dumps(result_json, ensure_ascii=False)})
            threads.append({"role":"user","content":"나의 상황에 맞는 최적의 거래를 이유와 구매링크와 함께 추천하라"})
            analysis_response=openai.chat.completions.create(model="gpt-4",messages=threads).choices[0].message.content
            print("\n📝 GPT-4 분석 결과:");print(analysis_response)
            threads.append({"role":"assistant","content":analysis_response})           
    else: res_txt=gpt4_answer.choices[0].message.content; print(f"openai 답변: {res_txt}"); threads.append({"role":"assistant","content":res_txt})