import requests as req,json;from dotenv import load_dotenv;import os,time;load_dotenv()
 
# res.encoding = "utf-8" # ✅ 인코딩 강제 설정 (utf-8)
# json_data = json.loads(res.content.decode("utf-8")) # ✅ 직접 JSON 변환 (BOM 제거)
# print(json.dumps(json_data, ensure_ascii=False, indent=2)) # ✅ 한글 깨짐 없이 출력

filename = r"C:\OCR\eval_test\t-drp.en_ko.in_house.selectstar_003927.jpg"
# API URL
api_url = "https://7pnf4rczq4.apigw.ntruss.com/custom/v1/39304/d37c5e7961d0ed500ecf0475346027cf2d7010b7083c411f953936b0e38b1ab2/general"  # API Gateway 엔드포인트

# 인증 정보
api_key = os.getenv("naver")  # 환경 변수에서 API Key 로드
print(api_key)
# 요청 데이터
payload = {
    "images": [
        {
            "format": "jpg",
            "name": "medium",
            "data": None
        }
    ],
    "lang": "ko",
    "requestId": "string",  # 요청 ID (원하는 값으로 설정)
    "resultType": "string",
    "timestamp": int(time.time()),
    "version": "V1"
}

# HTTP 요청 헤더
headers = {"Content-Type": "application/json",
    "X-OCR-SECRET": api_key}

with open(filename, "rb") as f:
    files = {"file": f}  # 파일 업로드 설정
    response = req.post(api_url, headers=headers, json=payload, files=files) # API 요청

# 응답 확인
if response.status_code == 200:
    print(json.dumps(response.json(), ensure_ascii=False, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.text)