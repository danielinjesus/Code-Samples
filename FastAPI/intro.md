# 사전 환경 세팅
먼저 아래 두 줄 실행 cmd에서 실행하기.
pip가 conda와 꼬여서 로컬에 설치했어도 pip 실행이 안 되어 python -m pip로 실행하기

python -m pip install fastapi
python -m pip install "uvicorn[standard]"

# 파이썬은 필요하다. 웹서버와 파이썬 중간에 중계서버가. 그게 UNICORN.

서버실행 : uvicorn main:app --reload
url/docs 에서 바로 swagger 확인 가능

# Return은 그냥 txt로 보내도 된다. 고객도 그냥 r.text로 받으면 된다.
문제는 FastAPI에 보낼 때다.

# FastAPI는 아무 말도 없이 str으로 보내면 다음 에러가 난다.
127.0.0.1:7172 - "POST /infer HTTP/1.1" 422 Unprocessable Entity
JSON으로 보내고, Pydantic 혹은 Type Hinting으로 받아야 된다.
str으로 보낼 때는 request 모듈 호출하고 여러 설정이 필요하다.

# Streamlit에서 보낼 때 key이름은 pydantic 정의 클래스의 key이름과 같지 않으면 에러 발생

# Python에서 from 3_mlflow.infer_model_test import test와 같은 코드는
여전히 문법 오류를 유발합니다.
Python에서는 패키지 이름이나 모듈 이름이
숫자로 시작하는 것을 허용하지 않기 때문입니다. -->