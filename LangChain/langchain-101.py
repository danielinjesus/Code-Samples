from dotenv import load_dotenv; import os
from langchain_openai import ChatOpenAI
load_dotenv(dotenv_path="C:/code-samples/.env")

llm = ChatOpenAI(model="gpt-3.5-turbo")  # 또는 model="gpt-4"
response = llm.invoke("LangChain이 뭐야?")
print(response.content)
