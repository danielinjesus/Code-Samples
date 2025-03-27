from openai import OpenAI;from dotenv import load_dotenv;import os;load_dotenv()
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url="https://api.openai.com/v1")
o1_answer = openai.chat.completions.create(model="o1-preview",messages=[    
    {"role": "user", "content": """    
- 답변은 json 형식으로 항목은 intent와 query로 구성되어 있다.
- [주어진 대화]를 자세히 읽고 user의 intent를 일반대화를 원하는지와 과학상식 지식을 궁금해 하는지의 두 가지로 분류하라
- intent는 0 또는 1의 값을 가지며, 0은 일반대화, 1은 과학상식을 의미한다.
- query는 intent가 1일 경우, 사용자의 질문과 관련된 과학상식을 내부 데이터베이스에서 elasticsearch로 sparse retrieval 하기 위해 필요한 query를 한국어로 작성하여 query에 삽입하라.

[주어진 대화]
[{"role": "user", "content": "요새 너무 힘들다."}]
"""}
]); print(f"openai-o1 답변: {o1_answer.choices[0].message.content}")