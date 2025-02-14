from google.cloud import speech
from google.oauth2 import service_account

# 서비스 계정 키 파일을 직접 불러오기
SERVICE_ACCOUNT_FILE = "/data/ephemeral/home/upstageailab-llm-pjt-chatbot-1/Daun/upstageailab5-llm-pjt-ccd1cde04a8a.json"
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

# API 클라이언트 생성 (환경 변수 필요 없음)
client = speech.SpeechClient(credentials=credentials)

print("GCP STT API 인증 성공!")
