from dotenv import load_dotenv;load_dotenv();import anthropic,os,base64

# For base64-encoded images
image_path=r"C:\code-samples\Document\img\side_project.png"
image_media_type="image/png"

with open(image_path, "rb") as image_file:
    image_data = base64.b64encode(image_file.read()).decode("utf-8")
    
client = anthropic.Anthropic(api_key=os.getenv("claude"))
message = client.messages.create(
    model="claude-3-7-sonnet-20250219",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": image_media_type,
                        "data": image_data,
                    },
                },
                {
                    "type": "text",
                    "text": "what is it about?"
                }
            ],
        }
    ],
)
print(message)