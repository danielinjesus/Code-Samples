import boto3
from io import BytesIO
from PIL import Image

# 이미지 바이트 스트림 생성 (streamlit 사용 시)
image_path = "your_image.jpg"
image = Image.open(image_path)
image_bytes = BytesIO()
image.save(image_bytes, format="PNG")
image_bytes.seek(0)

# AWS Rekognition 클라이언트 설정
client = boto3.client('rekognition')

# 이미지 바이트로 Rekognition에서 OCR 수행
response = client.detect_text(
    Image={'Bytes': image_bytes.getvalue()}
)

# ######################################
# # 파일을 바이너리로 읽어서 Rekognition에 넘김
# with open('your_image.jpg', 'rb') as image_file:
#     image_bytes = image_file.read()

# # AWS Rekognition 클라이언트 설정
# client = boto3.client('rekognition')

# # 이미지 바이트로 Rekognition에서 OCR 수행
# response = client.detect_text(
#     Image={'Bytes': image_bytes}
# )
######################################

# OCR 결과 출력
print(response)
