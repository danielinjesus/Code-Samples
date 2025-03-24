# pip install -qU langchain-core langchain-upstage
from dotenv import load_dotenv;import os,time;load_dotenv();st=time.time()
from langchain_upstage import ChatUpstage;from langchain_core.messages import HumanMessage
chat=ChatUpstage(api_key=os.getenv("upstage"), model="solar-mini")
messages=[HumanMessage(content="Hi, how are you?")]
print(chat.invoke(messages).dict()['content'],round(time.time()-st,2))