from google.cloud import firestore;from google.oauth2 import service_account
SERVICE_ACCOUNT_FILE = "/data/ephemeral/home/upstageailab-llm-pjt-chatbot-1/TeamCode/token/upstageailab5-llm-pjt-985da1d6a634.json"
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
db=firestore.Client(credentials=credentials)
def retrieve_food(username):
    user = db.collection("users").document(username)
    try:
        user_food = user.get()
        if user_food.exists:
            data =  user_food.to_dict()
            filtered_data = {k: v for k, v in data.items() if k not in ["username", "password", "created_at"]}
            return f"음식들: {filtered_data}"
        else:
            return "❌ 존재하지 않는 계정입니다."
    except Exception as e:
        return f"❌ 에러 발생: {e}"
print(retrieve_food("dani2"))