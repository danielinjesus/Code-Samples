**Sentence-BERT (SBERT)**는 문장(문맥)을 벡터화하는 데 매우 효율적이며, RAG 시스템에서 **의미 기반 검색(Semantic Search)**에 최적화된 모델입니다.

Sentence-BERT가 무엇인가?
**Sentence-BERT (SBERT)**는 BERT의 변형으로, 문장을 **고차원 벡터(Sentence Embedding)**로 변환합니다.
문장의 의미와 문맥을 반영한 고유한 벡터를 생성하여 의미 기반 검색에서 뛰어난 성능을 발휘합니다.
Hugging Face Transformers 라이브러리에서 쉽게 사용할 수 있습니다.
왜 Sentence-BERT를 써야 할까?
문맥 이해 및 유사도 계산:

일반적인 BERT는 토큰 레벨의 임베딩만 제공하지만, SBERT는 문장 레벨의 고유한 벡터를 생성하여 문맥 이해가 뛰어납니다.
예:
"고양이가 나무에 올라갔다" vs "나무에 고양이가 올라갔다" → 의미는 같지만 순서가 다름 → SBERT는 같은 벡터에 가깝게 매핑.
빠른 유사도 계산:

SBERT는 Cosine Similarity 또는 Euclidean Distance를 사용하여 빠르게 문장 유사도를 계산.
특히, **문장 검색(Semantic Search)**에서 Top-k 문장을 빠르게 추출할 수 있습니다.
RAG 시스템에 최적화:

SBERT로 4200개 문서를 벡터화하고, 유사도 검색으로 관련 문서만 추출 → LLM에 입력.
비용 절감과 응답 속도를 동시에 개선.
어떻게 사용할까?
Hugging Face Transformers와 Sentence-Transformers 라이브러리를 사용하여 간단하게 적용할 수 있습니다.
