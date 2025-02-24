from openai import OpenAI;import os;from dotenv import load_dotenv;load_dotenv()
 
upstage = OpenAI(api_key=os.getenv("upstage"), base_url="https://api.upstage.ai/v1/solar")
 
query = "How to find problems in code?"
query_embedding = upstage.embeddings.create(model = "embedding-query",input = query).data[0].embedding
print(query_embedding)