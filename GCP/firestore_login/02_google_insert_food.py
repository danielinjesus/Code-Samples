from google.cloud import firestore; import hashlib
from google.oauth2 import service_account
SERVICE_ACCOUNT_FILE = "/data/ephemeral/home/upstageailab-llm-pjt-chatbot-1/TeamCode/token/upstageailab5-llm-pjt-985da1d6a634.json"
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
db=firestore.Client(credentials=credentials)

def create_user(username, password, food):
    user_id = hashlib.sha256(username.encode()).hexdigest()[:10]  # 해시를 이용해 user_id 생성
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # 비밀번호 해싱

    user_ref = db.collection("users").document(username)

    if user_ref.get().exists:
        return "❌ 이미 존재하는 계정입니다."

    input_food = {
        "username": username,
        "password": hashed_password,  # 실제 서비스에서는 해싱 후 저장해야 함
        "created_at": firestore.SERVER_TIMESTAMP
    }; input_food.update(food)

    user_ref.set(input_food)
    return f"✅ 계정 생성 완료! user_id: {user_id}"

# 예제 실행
print(create_user("dani2", "1234*", {"아보카도":20, "파프리카":20, "꼬막(kg)":3, "당근": 30, "오이":4, "양파": 2, "빻은마늘 gram":300, "사과":3, "나이": 38, "키": 160, "체중": 50, "공복혈당":180}))