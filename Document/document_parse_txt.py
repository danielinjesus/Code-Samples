import requests as req,json;from dotenv import load_dotenv;import os;load_dotenv()

filename=r"C:\code-samples\Document\img\DP1.JPG"
url="https://api.upstage.ai/v1/document-ai/document-parse"
headers={"Authorization":f"Bearer {os.getenv('upstage')}"}
data={"output_formats":"['text']"}
files={"document":open(filename,"rb")}

with open(filename, "rb") as f:
    files = {"document": f}
    res=req.post(url,headers=headers,files=files,data=data)    

json_data = res.json()

# ? JSON 출력 (디버깅)
print(json.dumps(json_data, ensure_ascii=False, indent=2))  # ? 한글 깨짐 없이 보기