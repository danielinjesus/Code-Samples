import requests as req,json;from dotenv import load_dotenv;import os;load_dotenv()

filename=r"C:\OCR\eval_test\t-drp.en_ko.in_house.selectstar_003927.jpg"
files={"document":open(filename,"rb")}
url="https://api.upstage.ai/v1/document-ai/document-parse"
headers={"Authorization":f"Bearer {os.getenv("upstage")}"}
res=req.post(url,headers=headers,files=files)

res.encoding = "utf-8" # ✅ 인코딩 강제 설정 (utf-8)
json_data = json.loads(res.content.decode("utf-8")) # ✅ 직접 JSON 변환 (BOM 제거)
print(json.dumps(json_data, ensure_ascii=False, indent=2)) # ✅ 한글 깨짐 없이 출력