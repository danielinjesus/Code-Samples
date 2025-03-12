import requests as req
import json
import os
import time
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# ✅ CLOVA OCR API Gateway 엔드포인트 확인 필요
api_url = "https://7pnf4rczq4.apigw.ntruss.com/custom/v1/39304/d37c5e7961d0ed500ecf0475346027cf2d7010b7083c411f953936b0e38b1ab2/general"

# ✅ API Key 로드
api_key = os.getenv("naver")
if not api_key:
    print("❌ API Key를 불러오지 못했습니다. .env 파일을 확인하세요.")
    exit()

# ✅ 파일 경로 (로컬 이미지)
filename = r"C:\OCR\eval_test\t-drp.en_ko.in_house.selectstar_003927.jpg"

# ✅ HTTP 요청 헤더
headers = {
    "X-OCR-SECRET": api_key  # CLOVA OCR API Key
}

# ✅ 요청 데이터 (JSON)
payload = {
    "images": [
        {
            "format": "jpg",
            "name": "medium",
            "data": None  # 파일 업로드 방식 사용
        }
    ],
    "lang": "ko",
    "requestId": "string",
    "resultType": "string",
    "timestamp": int(time.time()),
    "version": "V1"
}

# ✅ API 요청 (파일 업로드 방식)
with open(filename, "rb") as f:
    files = {"file": f}  # 파일 업로드 설정
    try:
        response = req.post(api_url, headers=headers, data={"message": json.dumps(payload)}, files=files, timeout=10)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        response_json = response.json()
        
        # OCR 결과에서 텍스트 추출
        extracted_text = " ".join(field["inferText"] for field in response_json["images"][0]["fields"])
        # 결과 출력
        print(extracted_text)
        
        # print(json.dumps(response_json, ensure_ascii=False, indent=2))  # JSON 출력
        # num_objects = len(response_json["images"][0]["fields"])  # 첫 번째 이미지의 필드 개수
        # print(f"📌 검출된 객체 개수: {num_objects} 개")
    except req.exceptions.HTTPError as http_err:
        print(f"❌ HTTP 오류 발생: {http_err}")
        print(response.text)
    except req.exceptions.Timeout:
        print("❌ 요청 시간이 초과되었습니다. 서버 상태 또는 네트워크 연결을 확인하세요.")
    except req.exceptions.RequestException as e:
        print(f"❌ 요청 중 오류 발생: {e}")