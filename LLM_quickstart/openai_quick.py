from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.openai.com/v1")
gpt4_answer = openai.chat.completions.create(model="gpt-4",messages=[
    {"role": "system", "content": "Respond like a casual friend."},
    {"role": "user", "content": "What is quantum mechanics?"}
]); print(f"openai 답변: {gpt4_answer.choices[0].message.content}")