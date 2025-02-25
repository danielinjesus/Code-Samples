from openai import OpenAI; import traceback;from dotenv import load_dotenv;import os;load_dotenv();
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"),base_url="https://api.openai.com/v1");
print(client.models.list())
