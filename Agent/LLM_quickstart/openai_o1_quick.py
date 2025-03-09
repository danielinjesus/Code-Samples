from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()

openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.openai.com/v1")
o1_answer = openai.chat.completions.create(model="o1-preview",messages=[    
    {"role": "user", "content": """    
     What is quantum mechanics?"""}
]); print(f"openai-o1 답변: {o1_answer.choices[0].message.content}")