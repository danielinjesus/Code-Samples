import easyocr
from io import BytesIO
from PIL import Image

# 이미지를 바이트 스트림으로 읽기
image_path = "your_image.jpg"
image = Image.open(image_path)
image_bytes = BytesIO()
image.save(image_bytes, format="PNG")
image_bytes.seek(0)

reader = easyocr.Reader(['en'])  # 언어에 맞는 리더 인스턴스
result = reader.readtext(image_bytes)  # 이미지 바이트로 OCR 수행

# 이미지 파일 경로로 OCR 수행
# result = reader.readtext('your_image.jpg')  # 파일 경로로 직접 OCR 수행

# 결과 출력
print(result)
