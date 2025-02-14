from google.cloud import firestore; import hashlib
from google.oauth2 import service_account
SERVICE_ACCOUNT_FILE = "/data/ephemeral/home/upstageailab-llm-pjt-chatbot-1/TeamCode/token/upstageailab5-llm-pjt-985da1d6a634.json"
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
db=firestore.Client(credentials=credentials)

def create_user(username, password):
    user_id = hashlib.sha256(username.encode()).hexdigest()[:10]  # 해시를 이용해 user_id 생성
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # 비밀번호 해싱
    user_ref = db.collection("users").document(username)
    user_doc = user_ref.get()

    if user_doc.exists:
        user_data = user_doc.to_dict()
        
        if user_data["password"] == hashed_password:
            return "✅ 로그인 성공! user_id: "
        else:
            return "❌ 이미 존재하는 계정입니다."

    user_ref.set({
        "username": username,
        "password": hashed_password,  # 실제 서비스에서는 해싱 후 저장해야 함
        "created_at": firestore.SERVER_TIMESTAMP
    })
    return f"✅ 계정 생성 완료! user_id: {user_id}"

print(create_user("dani", "1234*"))