# pip install -qU langchain-core langchain-upstage
from dotenv import load_dotenv;import os,time;load_dotenv();st=time.time()
from langchain_upstage import ChatUpstage;from langchain_core.messages import HumanMessage,SystemMessage
chat=ChatUpstage(api_key=os.getenv("upstage"), model="solar-mini")
messages=[
    SystemMessage(content="Respond like a casual friend."),
    HumanMessage(content="Hi, how are you?")]
print(chat.invoke(messages).to_dict()['content'],round(time.time()-st,2))