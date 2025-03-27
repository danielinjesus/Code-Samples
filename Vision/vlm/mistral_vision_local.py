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
                "text": "Return coordinates of bounding boxes for all the texts in this image"
            },
            {
                "type": "image_url",
                "image_url": "https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/mistral/ocr/receipt.png"
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