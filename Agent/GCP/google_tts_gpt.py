from google.cloud import speech # # pip install --upgrade google-cloud-speech
####################
from google.oauth2 import service_account

# 서비스 계정 키 파일을 직접 불러오기
SERVICE_ACCOUNT_FILE = "/data/ephemeral/home/upstageailab-llm-pjt-chatbot-1/TeamCode/token/upstageailab5-llm-pjt-e46dafec4e87.json"
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

# API 클라이언트 생성 (환경 변수 필요 없음)
def run_quickstart()-> speech.RecognizeResponse:
    client = speech.SpeechClient(credentials=credentials)

    gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"
    
    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # ✅ API 요청 후 응답 확인
    response = client.recognize(config=config, audio=audio)

    print("Raw Response:", response)  # 전체 응답 출력

    # ✅ 응답이 비어 있는 경우 확인
    if not response.results:
        print("⚠️ No transcription results found!")
        return

    # ✅ 결과 출력
    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")

run_quickstart()
