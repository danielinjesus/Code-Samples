# pip install --upgrade google-cloud-speech
from google.cloud import speech
from google.oauth2 import service_account

# 서비스 계정 키 파일을 직접 불러오기
SERVICE_ACCOUNT_FILE = "/data/ephemeral/home/upstageailab-llm-pjt-chatbot-1/TeamCode/token/upstageailab5-llm-pjt-e46dafec4e87.json"
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
def run_quickstart():
    # Instantiates a client
    client = speech.SpeechClient(credentials=credentials)

    # The name of the audio file to transcribe
    gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)
    print("Raw Response:", response)  # 전체 응답 출력
    for result in response.results:
        print(f"Transcript: {result.alternatives[0].transcript}")
        
run_quickstart()