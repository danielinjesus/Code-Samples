1. 설치:
bash
복사
편집
pip install torch transformers sentence-transformers
2. 예제 코드:
SBERT 모델 로드 및 문서 벡터화:
python
복사
편집
from sentence_transformers import SentenceTransformer

# SBERT 모델 로드 (paraphrase-multilingual-MiniLM-L12-v2: 다국어 지원)
model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

# 문서 리스트 (4200개 문서를 여기에 추가)
documents = [
    {"docid": "1", "content": "말론산 라디칼의 스핀 밀도..."},
    {"docid": "2", "content": "전자 전이란..."},
    {"docid": "3", "content": "효소의 작용 기작..."}
]

# 문서 Embedding 생성
embeddings = []
for doc in documents:
    embedding = model.encode(doc['content'], convert_to_tensor=True)
    embeddings.append((doc['docid'], embedding))

# 확인
print(embeddings[:3])  # 상위 3개 Embedding 확인
3. 사용자 질문 Embedding 및 유사도 검색:
python
복사
편집
import torch
from torch.nn import functional as F

def get_top_k_documents(query, embeddings, top_k=5):
    # 사용자 질문 Embedding
    query_embedding = model.encode(query, convert_to_tensor=True)

    # 코사인 유사도 계산
    scores = []
    for docid, doc_embedding in embeddings:
        cosine_sim = F.cosine_similarity(query_embedding, doc_embedding, dim=0)
        scores.append((docid, cosine_sim.item()))

    # 유사도 높은 순서로 정렬 후 Top-k 선택
    top_k_docs = sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]
    return top_k_docs

# 사용자 질문
user_question = "말론산 라디칼의 스핀 밀도는?"

# Top-k 문서 검색
top_k_docs = get_top_k_documents(user_question, embeddings)
print("Top-k 관련 문서:", top_k_docs)
4. Top-k 문서만 LLM에 입력:
python
복사
편집
import openai
openai.api_key = "YOUR_OPENAI_API_KEY"

# Top-k 문서 내용 결합
relevant_docs = [doc['content'] for doc in documents if doc['docid'] in [doc[0] for doc in top_k_docs]]
combined_content = "\n".join(relevant_docs)

# LLM에 입력하여 답변 생성
response = openai.ChatCompletion.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "user", "content": combined_content},
        {"role": "user", "content": user_question}
    ]
)

print("LLM 응답:", response['choices'][0]['message']['content'])
이 방법의 장점:
SBERT로 벡터화하면 문맥을 정확히 이해하여 **의미 기반 검색(Semantic Search)**에서 뛰어난 성능.
Top-k 문서만 LLM에 입력하여 비용 절감과 응답 속도 향상.
Hugging Face Transformers와 Sentence-Transformers 라이브러리 사용으로 빠른 개발 및 유지보수.
추천 모델:
paraphrase-multilingual-MiniLM-L12-v2: 다국어 지원 + 빠른 속도 + 높은 정확도
all-MiniLM-L6-v2: 영어 전용 + 가볍고 빠름 + 비용 효율적
paraphrase-MPNet-base-v2: 높은 정확도 + 대규모 문서 검색에 유리
SBERT vs OpenAI Embedding 비교:
특징	SBERT	OpenAI Embedding (text-embedding-ada-002)
성능	문맥 이해 및 의미 기반 검색 탁월	빠르고 저렴하지만 문맥 이해는 SBERT보다 떨어짐
속도	빠르지만 GPU 사용 시 더 빠름	매우 빠름 (API 호출)
비용	무료 (로컬), 서버 비용만 발생	유료 (토큰당 비용)
다국어 지원	강력함 (다국어 모델 사용 시)	언어별로 성능 차이 있음
설치 및 유지보수	로컬 설치 필요, 모델 관리 필요	클라우드 기반, 설치 불필요