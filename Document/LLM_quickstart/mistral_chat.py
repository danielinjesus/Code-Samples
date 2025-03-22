from mistralai import Mistral;import os
from dotenv import load_dotenv;load_dotenv()
client=Mistral(api_key=os.environ["mistral"])
model = "mistral-large-latest" 

chat_response = client.chat.complete(
    model= model,
    messages = [
        {
            "role": "user",
            "content": "What is the best French cheese?",
        },
    ]
)
print(chat_response.choices[0].message.content)