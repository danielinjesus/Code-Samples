from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()

upstage = OpenAI(api_key=os.getenv("upstage"), base_url="https://api.upstage.ai/v1/solar")
solar_answer = upstage.chat.completions.create(model="solar-pro",messages=[
    {"role": "system", "content": "Respond like a casual friend."},
    {"role": "user", "content": "What is quantum mechanics?"}
]); print(f"solar 답변: {solar_answer.choices[0].message.content}")