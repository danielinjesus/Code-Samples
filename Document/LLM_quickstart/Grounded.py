import pandas as pd; from tqdm import tqdm
ground_df = pd.read_csv("/data/ephemeral/home/upstageailab-ir-competition-ir_s3/person/DU/output/02-2-5_solar_o1.csv", encoding='utf-8-sig')

from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
client = OpenAI(api_key=os.getenv("upstage"),base_url="https://api.upstage.ai/v1/solar")
 
notGrounded = []

print(ground_df.shape)

# if ground_df['intent']==0:
# for idx, row in tqdm(ground_df.iterrows(), total=len(ground_df)):     
#     response = client.chat.completions.create(
#         model="groundedness-check",
#         messages=[
#             {
#                 "role": "user",
#                 "content": row['dialogue']
#             },
#             {
#                 "role": "assistant",
#                 "content": row['summary']
#             }
#         ]
#     )    
#     if response.choices[0].message.content != 'grounded':
#         notGrounded.append({'index':idx, 'dialogue':row['dialogue'], 'summary':row['summary']})
# notGrounded = pd.DataFrame(notGrounded)
# notGrounded.to_csv("/data/ephemeral/home/upstageailab-nlp-summarization-nlp_s2/src/data/groundness/ground.csv", encoding='utf-8-sig')
# print(notGrounded)
# print(f"갯수: {len(notGrounded)}")