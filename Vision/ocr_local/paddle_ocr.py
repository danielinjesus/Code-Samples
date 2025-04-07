from paddleocr import PaddleOCR
from io import BytesIO
from PIL import Image

# 이미지를 바이트 스트림으로 읽기
image_path = "your_image.jpg"
image = Image.open(image_path)
image_bytes = BytesIO()
image.save(image_bytes, format="PNG")
image_bytes.seek(0)  # 바이트 스트림을 처음으로 리셋

ocr = PaddleOCR(use_angle_cls=True, lang='en')  # 언어와 설정에 맞게 초기화
result = ocr.ocr(image_bytes, cls=True)  # 이미지 바이트로 OCR 수행

# 이미지 파일 경로로 OCR 수행
# result = ocr.ocr('your_image.jpg', cls=True)  # 파일 경로로 직접 OCR 수행

# 결과 출력
print(result)
