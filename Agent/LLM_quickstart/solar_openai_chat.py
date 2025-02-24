from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
upstage = OpenAI(api_key=os.getenv("upstage"), base_url="https://api.upstage.ai/v1/solar")
openai = OpenAI(api_key=os.getenv("openai"), base_url="https://api.openai.com/v1")

solar_answer = upstage.chat.completions.create(model="solar-pro",messages=[
    {"role": "system", "content": "Respond like a casual friend."},
    {"role": "user", "content": "What is quantum mechanics?"}
]); print(f"solar 답변: {solar_answer.choices[0].message.content}")

gpt4_answer = openai.chat.completions.create(model="gpt-4",messages=[
    {"role": "system", "content": "Respond like a casual friend."},
    {"role": "user", "content": "What is quantum mechanics?"}
]); print(f"openai 답변: {gpt4_answer.choices[0].message.content}")