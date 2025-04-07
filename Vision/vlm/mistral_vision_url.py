from mistralai import Mistral;import os
from dotenv import load_dotenv;load_dotenv()
client=Mistral(api_key=os.environ["mistral"])

model = "pixtral-12b-2409" 

# Define the messages for the chat
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "explain the contents of the image in detail"
            },
            {
                "type": "image_url",            
                "image_url": "https://www.president.go.kr/images/2023/01/wkvWdGLGMyny63ca4efb184a16.84032054.png"
                
                # "image_url": "https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/mistral/ocr/receipt.png"
                #    "image_url": r"C:\code-samples\Vision\img\python_vis_code.png"
            }
        ]
    }
]

# Get the chat response
chat_response = client.chat.complete(
    model=model,
    messages=messages
)

# Print the content of the response
print(chat_response.choices[0].message.content)