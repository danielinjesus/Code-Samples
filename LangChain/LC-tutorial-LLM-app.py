# https://python.langchain.com/docs/tutorials/llm_chain/

from dotenv import load_dotenv; import os
load_dotenv(dotenv_path="C:/code-samples/.env", override=True)
# print(os.getenv("OPENAI_API_KEY"))
      
from langchain.chat_models import init_chat_model
model = init_chat_model("gpt-4o-mini", model_provider="openai")
res=model.invoke("Hello, world!")
print(res.content)
