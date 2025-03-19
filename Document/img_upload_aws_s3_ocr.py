import streamlit as st;import boto3,requests,os,json,urllib.parse,base64
from dotenv import load_dotenv;load_dotenv()
from PIL import Image;from io import BytesIO

# ✅ AWS S3 설정
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = "img4ocr"
AWS_REGION = "ap-northeast-2"

# ✅ S3 클라이언트 초기화
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# ✅ OCR API 설정
url = "https://api.upstage.ai/v1/document-ai/ocr"
headers = {"Authorization": f"Bearer {os.getenv('upstage')}"}

st.set_page_config(layout="wide")
st.title("이미지 업로드 → S3 저장 → OCR 처리")

# ✅ 이미지 업로드
uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["png", "jpg", "jpeg"])

if uploaded_file:
    # ✅ 이미지 표시
    image = Image.open(uploaded_file)
    st.image(image, caption="업로드된 이미지", use_container_width=True)

    # ✅ S3 저장 경로
    folder_path = "img/"
    s3_filename = f"{folder_path}{uploaded_file.name}"

    # ✅ S3에 업로드할 파일 준비
    image_bytes = BytesIO()
    image.save(image_bytes, format="PNG")
    image_bytes.seek(0)  # ✅ Reset pointer before upload

    try:
        # ✅ 1. S3 업로드
        s3.upload_fileobj(image_bytes, AWS_BUCKET_NAME, s3_filename, ExtraArgs={"ContentType": "image/png"})

        # ✅ 2. S3 Public URL 생성
        s3_url = f"https://{AWS_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{s3_filename}"
        st.success(f"S3 업로드 완료: [S3 링크]({s3_url})")

        # ✅ 3. OCR 요청 (Use uploaded image without re-downloading)
        # ✅ OCR API request using URL instead of downloading
        image_response = requests.get(s3_url)
        if image_response.status_code != 200:
            raise Exception(f"Failed to download image: {image_response.status_code}")
        files = {"document": ("image.png", image_response.content, "image/png")}  # ✅ Pass binary content
        url = "https://api.upstage.ai/v1/document-ai/ocr"
        headers = {"Authorization": f"Bearer {os.getenv('upstage')}"}
        res = requests.post(url, headers=headers, files=files)  # ✅ Uses URL instead of binary file
        # ✅ Parse the response
        res.encoding = "utf-8"
        json_data = res.json()
        print(json.dumps(json_data, ensure_ascii=False, indent=2))  # ✅ Pretty print OCR result

        st.subheader("OCR 결과:")
        if "text" in json_data and json_data["text"]:  # ✅ Ensure OCR text is present
            st.text_area("추출된 텍스트", json_data["text"], height=200)
        else:
            st.warning("OCR 결과가 비어 있습니다. 이미지가 명확한지 확인하세요.")

    except Exception as e:
        st.error(f"S3 업로드 또는 OCR 처리 중 오류 발생: {e}")