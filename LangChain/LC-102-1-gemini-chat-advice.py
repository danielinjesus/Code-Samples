from dotenv import load_dotenv; import os
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드 (기존 값 덮어쓰기)
load_dotenv(dotenv_path="C:/code-samples/.env", override=True)
# print(os.getenv("OPENAI_API_KEY"))
      
from langchain.chat_models import init_chat_model
model = init_chat_model("gpt-4o-mini", model_provider="openai")
res=model.invoke("Hello, world!")

# langchain.chat_models에서 init_chat_model 함수를 가져옵니다.
# 이 함수가 정의되어 있거나, 사용하시는 라이브러리에 포함되어 있어야 합니다.
try:
    from langchain.chat_models import init_chat_model

    # 채팅 모델 초기화
    # 이 과정에서 API 키 문제 등으로 오류가 발생할 수 있으므로 try 블록 내에 위치시킵니다.
    print("채팅 모델을 초기화하는 중...")
    model = init_chat_model("gpt-4o-mini", model_provider="openai") # <--- 원래 있던 호출이 여기로 이동했습니다.

    # 모델 호출
    print("모델을 호출하는 중...")
    res = model.invoke("Hello, world!")

    # 응답 내용 출력
    # res 객체에 'content' 속성이 있다고 가정합니다 (LangChain의 AIMessage 객체 등).
    print("\n모델 응답:")
    print(res.content)

except ImportError as ie:
    print(f"라이브러리 가져오기 오류: {ie}")
    print("필요한 라이브러리(예: langchain, openai, python-dotenv)가 올바르게 설치되었는지 확인해주세요.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
    if "api key" in str(e).lower() or "authentication" in str(e).lower():
        print("이 오류는 OPENAI_API_KEY와 관련이 있을 수 있습니다. ")
        print("'C:/code-samples/.env' 파일에 키가 올바르게 설정되어 있고 유효한지 확인해주세요.")
