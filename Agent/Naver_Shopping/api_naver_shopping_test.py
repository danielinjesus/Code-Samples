def naver(keyword):
    from dotenv import load_dotenv;import os,sys;import requests as req;import pandas as pd
    load_dotenv("/data/ephemeral/home/upstageailab-llm-pjt-chatbot-1/Daun/.env")
    client_id,client_secret=os.getenv("naverclient"),os.getenv("naversecret")
    sys.stdout.reconfigure(encoding='utf-8')# 콘솔 출력 인코딩을 UTF-8로 설정
    url="https://openapi.naver.com/v1/search/shop.json"
    headers={"X-Naver-Client-Id":client_id,"X-Naver-Client-Secret":client_secret}
    params={"query":keyword,"display":10}
    res=req.get(url,headers=headers,params=params)
    res_json=res.json()['items']
    res_df=pd.DataFrame(res_json)
    return res_df, res_json
if __name__ == "__main__":
    print(naver("아이패드"))
# if(res.status_code==200):
#     new_items = res.json()['items']  # 새로운 뉴스 항목들
#     try:    # 기존 뉴스 읽기 (없으면 빈 리스트)
#         with open(file_path, 'r', encoding='utf-8') as f:
#             saved_items = json.load(f)
#             # saved_items가 리스트가 아닌 경우, 빈 리스트로 초기화
#             if not isinstance(saved_items, list):
#                 saved_items = []
#     except (json.JSONDecodeError, FileNotFoundError):
#         saved_items = []
#     existing_links = {item['link'] for item in saved_items}
#     new_unique_items = [item for item in new_items if item['link'] not in existing_links]
#     saved_items.extend(new_unique_items)
#     print("ok")
# else:
#     print(f"Error Code: {res.status_code}")