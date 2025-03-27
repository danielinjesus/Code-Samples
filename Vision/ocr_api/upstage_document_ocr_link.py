import requests as req,json;from dotenv import load_dotenv;import os;load_dotenv()
# ✅ Use the S3 URL instead of a local file
s3_url = "https://img4ocr.s3.ap-northeast-2.amazonaws.com/img/%EC%8A%A4%ED%81%AC%EB%A6%B0%EC%83%B7%202024-09-23%20142840.png"

# ✅ Download the image from S3
image_response = req.get(s3_url)
if image_response.status_code != 200:
    raise Exception(f"Failed to download image: {image_response.status_code}")
files = {"document": ("image.png", image_response.content, "image/png")}  # ✅ Pass binary content
url="https://api.upstage.ai/v1/document-ai/ocr"
headers={"Authorization":f"Bearer {os.getenv("upstage")}"}
res=req.post(url,headers=headers,files=files)
 
res.encoding = "utf-8" # ✅ 인코딩 강제 설정 (utf-8)
json_data = json.loads(res.content.decode("utf-8")) # ✅ 직접 JSON 변환 (BOM 제거)
print(json.dumps(json_data, ensure_ascii=False, indent=2)) # ✅ 한글 깨짐 없이 출력