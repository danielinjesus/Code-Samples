import os
from multiprocessing import Pool
from openai import OpenAI
from dotenv import load_dotenv
from openai import error
load_dotenv()
client = OpenAI(
    api_key=os.getenv("upstage"),
    base_url="https://api.upstage.ai/v1/solar")

# API 호출 함수
def check_groundedness(row):
    try:
        response = client.chat.completions.create(
            model="groundedness-check",
            messages=[
                {"role": "user", "content": row['dialogue']},
                {"role": "assistant", "content": row['summary']}
            ]
        )
        if response.choices[0].message.content != 'grounded':
            return {'index': row.name, 'dialogue': row['dialogue'], 'summary': row['summary']}
        return None
    except error.OpenAIError as e:
        # 예외를 문자열로 변환하여 반환
        return {'index': row.name, 'error': str(e)}
# 실행
if __name__ == "__main__":
    import pandas as pd
    ground_df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/train_dh_v2.csv")    
    with Pool(processes=4) as pool:
        results = pool.map(check_groundedness, [row for _, row in ground_df.iterrows()])
    results.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/groundness/ground.csv")
    print(results)