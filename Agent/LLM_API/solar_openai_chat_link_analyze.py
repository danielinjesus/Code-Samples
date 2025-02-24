from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
upstage = OpenAI(api_key=os.getenv("upstage"), base_url="https://api.upstage.ai/v1/solar")
openai = OpenAI(api_key=os.getenv("openai"), base_url="https://api.openai.com/v1")

solar_answer = upstage.chat.completions.create(model="solar-pro",messages=[
    {"role": "system", "content": "Visit each website provided and compare all the sales options and return the best option with reasonable reasons."},
    {"role": "user", "content": """
https://smartstore.naver.com/main/products/4657340221
https://smartstore.naver.com/main/products/7672499859
https://smartstore.naver.com/main/products/11351754537
https://smartstore.naver.com/main/products/9450569060
https://smartstore.naver.com/main/products/4778473014
https://search.shopping.naver.com/catalog/26225092961
https://smartstore.naver.com/main/products/5466506349
https://smartstore.naver.com/main/products/4694555170
https://smartstore.naver.com/main/products/6628727657
https://smartstore.naver.com/main/products/5940575767
"""}
]); print(f"solar 답변: {solar_answer.choices[0].message.content}")

gpt4_answer = openai.chat.completions.create(model="gpt-4",messages=[
    {"role": "system", "content": "Visit each website provided and compare all the sales options and return the best option with reasonable reasons."},
    {"role": "user", "content": """
https://smartstore.naver.com/main/products/4657340221
https://smartstore.naver.com/main/products/7672499859
https://smartstore.naver.com/main/products/11351754537
https://smartstore.naver.com/main/products/9450569060
https://smartstore.naver.com/main/products/4778473014
https://search.shopping.naver.com/catalog/26225092961
https://smartstore.naver.com/main/products/5466506349
https://smartstore.naver.com/main/products/4694555170
https://smartstore.naver.com/main/products/6628727657
https://smartstore.naver.com/main/products/5940575767
"""}
]); print(f"openai 답변: {gpt4_answer.choices[0].message.content}")