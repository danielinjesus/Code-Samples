from google.cloud import firestore

db = firestore.Client()
user_id = "user_123"
item_id = "item_1"

# 데이터 추가
db.collection("users").document(user_id).collection("fridge_items").document(item_id).set({
    "name": "당근",
    "quantity": 3,
    "unit": "개",
    "expiration_date": "2025-02-20"
})

# 데이터 수정
db.collection("users").document(user_id).collection("fridge_items").document(item_id).update({
    "quantity": 5  # 개수 변경
})

# 데이터 삭제
db.collection("users").document(user_id).collection("fridge_items").document(item_id).delete()
