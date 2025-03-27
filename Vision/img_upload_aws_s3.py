import streamlit as st;import boto3,requests,os,json,urllib.parse
from dotenv import load_dotenv;load_dotenv()
from PIL import Image;from io import BytesIO

# ✅ AWS S3 설정
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = "img4ocr"  # S3 버킷 이름
AWS_REGION = "ap-northeast-2"  # 서울 리전

# S3 클라이언트 초기화
s3 = boto3.client("s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION)

st.set_page_config(layout="wide")
st.title("이미지 업로드 → S3 특정 폴더 저장 → 외부 OCR API")

# ✅ 이미지 업로드
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # 이미지 표시
    image = Image.open(uploaded_file)
    
    # ✅ Streamlit용으로만 크기 조정 (50%)
    width, height = image.size
    new_size = (width // 2.5, height // 2.5)  # ✅ Reduce by 50%
    resized_image = image.resize(new_size, Image.ANTIALIAS)  # ✅ Display only
    
    st.image(resized_image, caption="업로드된 이미지", use_container_width=True)  # ✅ 최신 Streamlit 대응

    # ✅ S3 특정 폴더(`img/`)에 저장
    folder_path = "img/"  # S3 내부 폴더 경로
    s3_filename = f"{folder_path}{uploaded_file.name}"  # 최종 S3 저장 경로

    # S3에 업로드할 파일 준비
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    # ✅ S3 업로드 (ACL 없이 업로드)
    try:
        s3.upload_fileobj(image_bytes, AWS_BUCKET_NAME, s3_filename, ExtraArgs={"ContentType": "image/png"})

        # ✅ 업로드된 파일의 퍼블릭 URL 생성 (S3 버킷 정책이 퍼블릭 접근을 허용해야 가능)
        s3_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_filename}"
        # ✅ URL 인코딩 (한글 및 공백을 % 코드로 변환)
        encoded_url = urllib.parse.quote(s3_url, safe=":/")

        # Streamlit에 올바르게 표시
        st.success(f"S3 업로드 완료: [S3 링크]({encoded_url})")
    
    except Exception as e:
        st.error(f"S3 업로드 또는 OCR 처리 중 오류 발생: {e}")