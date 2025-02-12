import hashlib
from google.cloud import firestore

db = firestore.Client()

def create_user(username, password):
    user_id = hashlib.sha256(username.encode()).hexdigest()[:10]  # 해시를 이용해 user_id 생성
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # 비밀번호 해싱

    user_ref = db.collection("users").document(user_id)

    if user_ref.get().exists:
        return "❌ 이미 존재하는 계정입니다."

    user_ref.set({
        "username": username,
        "password": hashed_password,  # 실제 서비스에서는 해싱 후 저장해야 함
        "created_at": firestore.SERVER_TIMESTAMP
    })
    return f"✅ 계정 생성 완료! user_id: {user_id}"

# 예제 실행
print(create_user("test_user", "mypassword123"))
