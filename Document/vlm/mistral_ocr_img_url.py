from mistralai import Mistral;import os
from dotenv import load_dotenv;load_dotenv()

client=Mistral(api_key=os.environ["mistral"])

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "image_url",
        "image_url": "https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/mistral/ocr/receipt.png"
    }
)
print(ocr_response)