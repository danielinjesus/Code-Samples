# pip install google-genai
from google import genai;from dotenv import load_dotenv;import os;load_dotenv()

client = genai.Client(api_key=os.getenv('gemini'))
response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain how AI works",)

print(response.text)