
from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()

print(os.getenv("OPENAI_API_KEY"))

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.openai.com/v1")

text="전극점의 강도가 4π * 10^-4 웨버인 경우, 10 cm 떨어진 곳에 배치된 4π * 1.5 * 10^-4 웨버의 전극점에 대한 뉴턴 단위의 힘은 15 N입니다.\n\n전극점의 강도는 전자기장의 세기를 나타내는 값으로, 웨버(Wb)로 표시됩니다. 전극점 사이의 거리가 멀어질수록 전극점에 작용하는 힘은 감소합니다.\n\n뉴턴(N)은 힘의 단위로, 물체에 가해지는 힘의 크기를 측정하는 데 사용됩니다. 전극점에 작용하는 힘은 전극점의 강도와 거리에 따라 결정됩니다.\n\n따라서, 전극점의 강도가 4π * 10^-4 웨버이고, 10 cm 떨어진 곳에 배치된 4π * 1.5 * 10^-4 웨버의 전극점에 대한 뉴턴 단위의 힘은 15 N입니다."

response=client.embeddings.create(
    input=text,
    model="text-embedding-3-small"
); print(response.data[0].embedding)

# 4200개 문서 Embedding 벡터화
# embeddings = []
# for doc in documents:
#     embedding = get_embedding(doc['content'])
#     embeddings.append((doc['docid'], embedding))  
