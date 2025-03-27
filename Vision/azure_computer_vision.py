import requests
from io import BytesIO
from PIL import Image

# 이미지 바이트 스트림 생성
image_path = "your_image.jpg"
image = Image.open(image_path)
image_bytes = BytesIO()
image.save(image_bytes, format="PNG")
image_bytes.seek(0)

# Azure Computer Vision API 엔드포인트
subscription_key = "your_subscription_key"
endpoint = "https://your_endpoint.com/vision/v3.0/ocr"
headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Content-Type': 'application/octet-stream'
}

# Azure OCR API 호출
response = requests.post(endpoint, headers=headers, data=image_bytes.getvalue())
ocr_result = response.json()

# ######################################
# # 파일을 바이너리로 읽어서 Azure에 넘김
# with open('your_image.jpg', 'rb') as image_file:
#     image_bytes = image_file.read()
    
#     # Azure OCR API 호출
# response = requests.post(endpoint, headers=headers, data=image_bytes)
# ocr_result = response.json()
# ######################################

# OCR 결과 출력
print(ocr_result)
