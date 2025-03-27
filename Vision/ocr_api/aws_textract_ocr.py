from dotenv import load_dotenv;load_dotenv()
from PIL import Image;from io import BytesIO;import os
import boto3

# Textract 클라이언트 생성
textract = boto3.client('textract',
                        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                        region_name='us-east-1')

# 이미지 파일 열기 (로컬 파일 사용)
with open(r"C:\code-samples\Document\img\python_vis_code.png", "rb") as image_file:
    image_bytes = image_file.read()

# Textract로 OCR 분석 요청
response = textract.detect_document_text(Document={'Bytes': image_bytes})

# 결과 출력
for item in response['Blocks']:
    if item['BlockType'] == 'LINE':  # 라인 단위로 텍스트 추출
        print(item['Text'])
