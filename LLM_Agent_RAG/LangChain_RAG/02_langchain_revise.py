from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
import json, os, requests
from google.cloud import firestore
from google.oauth2 import service_account

# 🔹 환경 변수 로드
SERVICE_ACCOUNT_FILE = "/data/ephemeral/home/upstageailab-llm-pjt-chatbot-1/TeamCode/token/upstageailab5-llm-pjt-985da1d6a634.json"
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
db = firestore.Client(credentials=credentials)

# 🔹 네이버 쇼핑 API 함수
def naver(keyword):
    url = "https://openapi.naver.com/v1/search/shop.json"
    headers = {
        "X-Naver-Client-Id": os.getenv("naverclient"),
        "X-Naver-Client-Secret": os.getenv("naversecret"),
    }
    params = {"query": keyword, "display": 10}
    try:
        res = requests.get(url, headers=headers, params=params)
        return res.json()["items"]
    except Exception as e:
        return f"❌ Error: {e}"

# 🔹 냉장고 데이터 조회
def retrieve_food(username):
    user = db.collection("users").document(username)
    try:
        user_food = user.get()
        if user_food.exists:
            data = user_food.to_dict()
            return {k: v for k, v in data.items() if k not in ["username", "password", "created_at"]}
        return "❌ 존재하지 않는 계정입니다."
    except Exception as e:
        return f"❌ 에러 발생: {e}"

# 🔹 LangChain의 Tool로 네이버 검색 함수 등록
tools = [
    Tool(
        name="naver",
        func=naver,
        description="네이버 쇼핑에서 키워드로 상품을 검색하는 함수",
    ),
]

# 🔹 LangChain Agent 초기화
llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
agent = initialize_agent(tools=tools, llm=llm, agent=AgentType.OPENAI_FUNCTIONS, verbose=True)

# 🔹 사용자 입력 받기
username = input("사용자이름: ")
user_food = retrieve_food(username)
print(f"\n내 냉장고 상태: {json.dumps(user_food, ensure_ascii=False)}\n")

# 🔹 GPT에 냉장고 정보 제공 후 대화 시작
while True:
    user_input = input("입력: ")
    response = agent.run(user_input)
    print(f"\n📝 GPT 응답: {response}\n")