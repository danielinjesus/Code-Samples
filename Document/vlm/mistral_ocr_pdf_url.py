from mistralai import Mistral;import os
from dotenv import load_dotenv;load_dotenv()

client=Mistral(api_key=os.environ["mistral"])

ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": "https://arxiv.org/pdf/2201.04234"
    },
    include_image_base64=True
)
print(ocr_response)