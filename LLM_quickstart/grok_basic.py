from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
    
client = OpenAI(api_key=os.getenv("grok"),base_url="https://api.x.ai/v1")

persona="""
you are a helpful friend supportive.
"""

input= input("what can i do for you")
completion = client.chat.completions.create(
  model="grok-2-latest",
  messages=[{"role": "system", "content": f"{persona}"},{"role": "user", "content": f"{input}"}]
); print(f"grok 답변: {completion.choices[0].message.content}")