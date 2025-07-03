# https://python.langchain.com/docs/tutorials/llm_chain/

from dotenv import load_dotenv; import os
load_dotenv(dotenv_path="C:/code-samples/.env", override=True)
      
from langchain.chat_models import init_chat_model
model = init_chat_model("gpt-4o-mini", model_provider="openai")
      
from langchain_core.messages import HumanMessage, SystemMessage
messages = [SystemMessage("You are one of a kind, a single, kind and welcoming frined of mine"),HumanMessage("What are you doing?")]

res=model.invoke(messages)
print(res.content)
