import pandas as pd; from tqdm import tqdm
ground_df = pd.read_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/train_dh_v2.csv")

from dotenv import load_dotenv; import os
load_dotenv(); 
from multiprocessing import Pool
# pip install openai
 
from openai import OpenAI # openai == 1.2.0
 
client = OpenAI(
    api_key=os.getenv("upstage"),
    base_url="https://api.upstage.ai/v1/solar"
)
 
notGrounded = []
for idx, row in tqdm(ground_df.iterrows(), total=len(ground_df)):     
    response = client.chat.completions.create(
        model="groundedness-check",
        messages=[
            {
                "role": "user",
                "content": row['dialogue']
            },
            {
                "role": "assistant",
                "content": row['summary']
            }
        ]
    )    
    if response.choices[0].message.content != 'grounded':
        notGrounded.append({'index':idx, 'dialogue':row['dialogue'], 'summary':row['summary']})
notGrounded = pd.DataFrame(notGrounded)
notGrounded.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/groundness/ground.csv", encoding='utf-8-sig')
print(notGrounded)
print(f"갯수: {len(notGrounded)}")