# Deep Research 실습 예제

### Getting Started

```bash
cp .env.example .env
```

> **중요**: 이 프로젝트는 uv 패키지 매니저를 사용합니다. 모든 명령어는 `uv run`을 통해 실행해야 올바른 가상환경과 패키지 버전이 사용됩니다.

LangGraph 서버를 로컬에서 시작하세요:

#### Mac

```bash
# uv 패키지 매니저 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 의존성 설치 및 LangGraph 서버 시작
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.12 langgraph dev --allow-blocking
```

#### Windows

##### uv 패키지 매니저 설치 (Windows)

**방법 1: PowerShell 사용 (권장)**

```powershell
# PowerShell을 관리자 권한으로 실행한 후:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 설치 확인
uv --version
```

**방법 2: 사전 빌드된 바이너리 다운로드**

1. <https://github.com/astral-sh/uv/releases> 에서 최신 릴리스 페이지로 이동
2. `uv-x86_64-pc-windows-msvc.zip` 파일 다운로드
3. 원하는 위치에 압축 해제 (예: `C:\Program Files\uv`)
4. 시스템 환경 변수 PATH에 해당 경로 추가
5. 새 명령 프롬프트나 PowerShell을 열고 `uv --version`으로 확인

**방법 3: Scoop 패키지 매니저 사용**

```powershell
# Scoop이 설치되어 있는 경우:
scoop install uv
```

##### LangGraph 서버 시작 (Windows)

```powershell
# uv로 의존성 설치 및 서버 시작
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.12 langgraph dev --allow-blocking

# 또는 기존 pip 사용
pip install -e .
pip install -U "langgraph-cli[inmem]" 
langgraph dev
```

#### Linux

```bash
# uv 패키지 매니저 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 의존성 설치 및 LangGraph 서버 시작
uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.12 langgraph dev --allow-blocking
```

### Jupyter 노트북 실행 (uv 사용)

#### Mac / Linux

```bash
# uv가 설치되어 있는지 확인
# 설치되어 있지 않다면 위의 명령으로 설치

# 프로젝트 의존성 설치 (Jupyter 포함)
uv pip install -e .

# Jupyter 노트북 실행
uv run jupyter notebook

# 또는 Jupyter Lab 실행
uv run jupyter lab
```

#### Windows

```powershell
# uv가 설치되어 있는지 확인
uv --version

# uv가 설치되어 있지 않다면 위의 "uv 패키지 매니저 설치 (Windows)" 섹션 참조

# 프로젝트 의존성 설치 (Jupyter 포함)
uv pip install -e .

# Jupyter 노트북 실행
uv run jupyter notebook

# 또는 Jupyter Lab 실행
uv run jupyter lab

# 특정 포트로 실행하려면
uv run jupyter notebook --port=8889
```

노트북 파일:

- `graph.ipynb`: 그래프 기반 워크플로우 구현 예제
- `multi_agent.ipynb`: 멀티 에이전트 구현 예제

### 패키지 업데이트

모든 패키지를 최신 버전으로 업데이트하려면:

```bash
# 패키지 업데이트
uv pip install -U -e .

# 업데이트 확인
uv pip list
```

### 프로젝트 실행 시 주의사항

**중요**: 이 프로젝트의 모든 Python 명령은 `uv run`을 통해 실행해야 합니다:

```bash
# 일반 Python 스크립트 실행
uv run python script.py

# pytest 실행
uv run pytest

# 대화형 Python 셸
uv run python

# LangGraph 개발 서버
uv run langgraph dev
```

이렇게 하면 uv가 관리하는 가상환경에서 올바른 패키지 버전으로 실행됩니다.

#### 멀티 에이전트

(1) 관심 있는 주제에 대해 에이전트와 채팅하면 보고서 생성이 시작됩니다:
(2) 보고서는 마크다운으로 생성됩니다.

#### 워크플로우

(1) `주제(Topic)`를 제공하세요:
(2) 보고서 계획이 생성되어 사용자 검토를 위해 제시됩니다.
(3) 피드백과 함께 문자열(`"..."`)을 전달하여 피드백에 기반해 계획을 재생성할 수 있습니다.
(4) 또는 Studio의 JSON 입력 상자에 `true`를 전달하여 계획을 승인할 수 있습니다.
(5) 승인되면 보고서 섹션들이 생성됩니다.

보고서는 마크다운으로 생성됩니다.

### 검색 도구

사용 가능한 검색 도구:

- [Tavily API](https://tavily.com/) - 일반 웹 검색
- [Perplexity API](https://www.perplexity.ai/hub/blog/introducing-the-sonar-pro-api) - 일반 웹 검색
- [Exa API](https://exa.ai/) - 웹 콘텐츠를 위한 강력한 신경망 검색
- [ArXiv](https://arxiv.org/) - 물리학, 수학, 컴퓨터 과학 등의 학술 논문
- [DuckDuckGo API](https://duckduckgo.com/) - 일반 웹 검색
- [Google Search API/Scrapper](https://google.com/) - 맞춤 검색 엔진을 [여기서](https://programmablesearchengine.google.com/controlpanel/all) 만들고 API 키를 [여기서](https://developers.google.com/custom-search/v1/introduction) 받으세요
- [Microsoft Azure AI Search](https://azure.microsoft.com/en-us/products/ai-services/ai-search) - 클라우드 기반 벡터 데이터베이스 솔루션

Deep Research 예제는 다양한 LLM과 호환됩니다:

- [`init_chat_model()` API와 통합된](https://python.langchain.com/docs/how_to/chat_models_universal_init/) 모든 모델을 선택할 수 있습니다
- 지원되는 통합의 전체 목록은 [여기](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html)를 참조하세요

## Deep Research 구현 방식

Deep Research는 각각 고유한 장점을 가진 두 가지 구별되는 구현 방식을 제공합니다:

## 1. 그래프 기반 워크플로우 구현 (`src/graph.py`)

그래프 기반 구현은 구조화된 계획-실행 워크플로우를 따릅니다:

- **계획 단계**: 계획자 모델을 사용하여 주제를 분석하고 구조화된 보고서 계획을 생성
- **인간 참여 루프**: 진행하기 전에 보고서 계획에 대한 인간의 피드백과 승인 허용
- **순차적 연구 과정**: 검색 반복 간 반성과 함께 섹션을 하나씩 생성
- **섹션별 연구**: 각 섹션에 전용 검색 쿼리와 콘텐츠 검색
- **다중 검색 도구 지원**: 모든 검색 제공업체(Tavily, Perplexity, Exa, ArXiv, PubMed, Linkup 등)와 작동

이 구현은 보고서 구조에 대한 더 큰 제어력과 함께 더 상호작용적인 경험을 제공하므로,
보고서 품질과 정확성이 중요한 상황에 이상적입니다.

여러 매개변수를 통해 연구 도우미 워크플로우를 사용자 정의할 수 있습니다:

- `report_structure`: 보고서의 맞춤 구조 정의 (기본값: 표준 연구 보고서 형식)
- `number_of_queries`: 섹션당 생성할 검색 쿼리 수 (기본값: 2)
- `max_search_depth`: 최대 반성 및 검색 반복 횟수 (기본값: 2)
- `planner_provider`: 계획 단계의 모델 제공업체 (기본값: "openai", [여기](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html)에 나열된 `init_chat_model`의 지원 통합에서 모든 제공업체 가능)
- `planner_model`: 계획을 위한 특정 모델 (기본값: "gpt-4.1")
- `planner_model_kwargs`: planner_model의 추가 매개변수
- `writer_provider`: 작성 단계의 모델 제공업체 (기본값: "openai", [여기](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html)에 나열된 `init_chat_model`의 지원 통합에서 모든 제공업체 가능)
- `writer_model`: 보고서 작성을 위한 모델 (기본값: "gpt-4.1")
- `writer_model_kwargs`: writer_model의 추가 매개변수
- `search_api`: 웹 검색에 사용할 API (기본값: "tavily", "perplexity", "exa", "arxiv", "pubmed", "linkup" 옵션 포함)

## 2. 멀티 에이전트 구현 (`src/multi_agent.py`)

멀티 에이전트 구현은 감독자-연구자 아키텍처를 사용합니다:

- **감독자 에이전트**: 전체 연구 과정을 관리하고 섹션을 계획하며 최종 보고서를 조립
- **연구자 에이전트**: 여러 독립적인 에이전트가 병렬로 작업하며, 각각 특정 섹션 연구 및 작성 담당
- **병렬 처리**: 모든 섹션이 동시에 연구되어 보고서 생성 시간을 크게 단축
- **전문화된 도구 설계**: 각 에이전트는 역할에 맞는 특정 도구에 액세스 (연구자용 검색, 감독자용 섹션 계획)
- **검색 및 MCP 지원**: 웹 검색을 위한 Tavily/DuckDuckGo, 로컬/외부 데이터 액세스를 위한 MCP 서버와 작동하거나 MCP 도구만 사용하여 검색 도구 없이 작동 가능

이 구현은 효율성과 병렬화에 초점을 맞춰 직접적인 사용자 개입 없이 더 빠른 보고서 생성에 이상적입니다.

여러 매개변수를 통해 멀티 에이전트 구현을 사용자 정의할 수 있습니다:

- `supervisor_model`: 감독자 에이전트를 위한 모델 (기본값: "openai:gpt-4.1")
- `researcher_model`: 연구자 에이전트를 위한 모델 (기본값: "openai:gpt-4.1")
- `number_of_queries`: 섹션당 생성할 검색 쿼리 수 (기본값: 2)
- `search_api`: 웹 검색에 사용할 API (기본값: "tavily", "duckduckgo", "none" 옵션)
- `ask_for_clarification`: 연구 전에 감독자가 명확화 질문을 해야 하는지 여부 (기본값: false) - **중요**: 감독자 에이전트의 질문 도구를 활성화하려면 `true`로 설정
- `mcp_server_config`: MCP 서버 구성 (선택사항)
- `mcp_prompt`: MCP 도구 사용을 위한 추가 지침 (선택사항)
- `mcp_tools_to_include`: 포함할 특정 MCP 도구 (선택사항)

## MCP (Model Context Protocol) 지원

멀티 에이전트 구현(`src/multi_agent.py`)은 웹 검색을 넘어 연구 기능을 확장하기 위해 MCP 서버를 지원합니다.
MCP 도구는 기존 검색 도구와 함께 또는 대신하여 연구 에이전트에게 제공되어 로컬 파일, 데이터베이스, API 및 기타 데이터 소스에 액세스할 수 있습니다.

**참고**: MCP 지원은 현재 멀티 에이전트(`src/multi_agent.py`) 구현에서만 사용 가능하며, 워크플로우 기반 워크플로우 구현(`src/graph.py`)에서는 사용할 수 없습니다.

### 주요 기능

- **도구 통합**: MCP 도구가 기존 검색 및 섹션 작성 도구와 원활하게 통합
- **연구 에이전트 액세스**: 연구 에이전트만 MCP 도구에 액세스 (감독자는 제외)
- **유연한 구성**: MCP 도구를 단독으로 사용하거나 웹 검색과 결합
- **기본 검색 비활성화**: `search_api: "none"`으로 설정하여 웹 검색 도구를 완전히 비활성화
- **맞춤 프롬프트**: MCP 도구 사용을 위한 특정 지침 추가

### 파일시스템 서버 예제

#### SDK

```python
config = {
    "configurable": {
        "search_api": "none",  # 웹 검색과 결합하려면 "tavily" 또는 "duckduckgo" 사용
        "mcp_server_config": {
            "filesystem": {
                "command": "npx",
                "args": [
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    "/path/to/your/files"
                ],
                "transport": "stdio"
            }
        },
        "mcp_prompt": "1단계: `list_allowed_directories` 도구를 사용하여 허용된 디렉토리 목록을 가져오세요. 2단계: `read_file` 도구를 사용하여 허용된 디렉토리의 파일을 읽으세요.",
        "mcp_tools_to_include": ["list_allowed_directories", "list_directory", "read_file"]  # 선택사항: 포함할 도구 지정
    }
}
```

#### Studio

MCP 서버 구성:

```json
{
  "filesystem": {
    "command": "npx",
    "args": [
      "-y",
      "@modelcontextprotocol/server-filesystem",
      "/Users/rlm/Desktop/Code/src/files"
    ],
    "transport": "stdio"
  }
}
```

MCP 프롬프트:

```text
중요: 파일시스템 도구를 사용할 때 이 정확한 순서를 반드시 따르세요:

1. 먼저: `list_allowed_directories` 도구를 호출하여 허용된 디렉토리를 찾으세요
2. 두 번째: 1단계에서 찾은 특정 디렉토리에 대해 `list_directory` 도구를 호출하여 사용 가능한 파일을 확인하세요
3. 세 번째: 2단계에서 찾은 특정 파일을 읽기 위해 `read_file` 도구를 호출하세요

`list_allowed_directories`를 먼저 호출하기 전까지는 `list_directory`나 `read_file`을 호출하지 마세요. 파일을 탐색하거나 읽기를 시도하기 전에 허용된 디렉토리를 먼저 찾아야 합니다.
```

MCP 도구:

```text
list_allowed_directories
list_directory 
read_file
```

포함된 파일을 참조하는 예제 테스트 주제와 후속 피드백:

주제:

```text
바이브 코딩에 대한 개요를 원합니다
```

연구 에이전트가 질문한 것에 대한 후속 답변:

```text
흥미롭고 재미있는 예제를 강조하는 바이브 코딩에 대한 단일 섹션 보고서를 원합니다
```

### 구성 옵션

- **`mcp_server_config`**: MCP 서버 구성을 정의하는 딕셔너리 ([langchain-mcp-adapters 예제](https://github.com/langchain-ai/langchain-mcp-adapters#client-1) 참조)
- **`mcp_prompt`**: MCP 도구 사용을 위해 연구 에이전트 프롬프트에 추가되는 선택적 지침
- **`mcp_tools_to_include`**: 포함할 특정 MCP 도구 이름의 선택적 목록 (설정하지 않으면 모든 서버의 모든 도구가 포함됨)
- **`search_api`**: MCP 도구만 사용하려면 `"none"`으로 설정하거나 기존 검색 API를 유지하여 둘 다 결합

### 일반적인 사용 사례

- **로컬 문서**: 프로젝트 문서, 코드 파일 또는 지식 베이스에 액세스
- **데이터베이스 쿼리**: 특정 데이터 검색을 위한 데이터베이스 연결
- **API 통합**: 외부 API 및 서비스에 액세스
- **파일 분석**: 연구 중 로컬 파일 읽기 및 분석

MCP 통합을 통해 연구 에이전트는 로컬 지식과 외부 데이터 소스를 연구 과정에 포함시켜 더 포괄적이고 상황에 맞는 보고서를 작성할 수 있습니다.

## 검색 API 구성

모든 검색 API가 추가 구성 매개변수를 지원하는 것은 아닙니다.
지원하는 것들은 다음과 같습니다:

- **Exa**: `max_characters`, `num_results`, `include_domains`, `exclude_domains`, `subpages`
  - 참고: `include_domains`와 `exclude_domains`는 함께 사용할 수 없습니다
  - 특정 신뢰할 수 있는 소스로 연구를 좁혀야 하거나, 정보 정확성을 보장하거나, 지정된 도메인(예: 학술 저널, 정부 사이트)을 사용해야 하는 연구에 특히 유용합니다
  - 특정 쿼리에 맞춘 AI 생성 요약을 제공하여 검색 결과에서 관련 정보를 더 쉽게 추출할 수 있습니다
- **ArXiv**: `load_max_docs`, `get_full_documents`, `load_all_available_meta`

Exa 구성 예제:

```python
thread = {"configurable": {"thread_id": str(uuid.uuid4()),
                           "search_api": "exa",
                           "search_api_config": {
                               "num_results": 5,
                               "include_domains": ["nature.com", "sciencedirect.com"]
                           },
                           # 기타 구성...
                           }}
```

## 모델 고려사항

(1) [`init_chat_model()` API](https://python.langchain.com/docs/how_to/chat_models_universal_init/)로 지원되는 모델을 사용할 수 있습니다. 지원되는 통합의 전체 목록은 [여기](https://python.langchain.com/api_reference/langchain/chat_models/langchain.chat_models.base.init_chat_model.html)를 참조하세요.

(2) ***워크플로우 계획자 및 작성자 모델은 구조화된 출력을 지원해야 합니다***: 사용하는 모델이 구조화된 출력을 지원하는지 [여기](https://python.langchain.com/docs/integrations/chat/)에서 확인하세요.

(3) ***에이전트 모델은 도구 호출을 지원해야 합니다:*** 도구 호출이 잘 지원되는지 확인하세요; gpt4.1로 테스트했습니다

## 평가 시스템

Open Deep Research는 보고서 품질과 성능을 평가하기 위한 두 가지 포괄적인 평가 시스템을 포함합니다:

### 1. Pytest 기반 평가 시스템

개발 및 테스트 사이클 동안 즉각적인 피드백을 제공하는 개발자 친화적인 테스트 프레임워크입니다.

#### **기능:**

- **풍부한 콘솔 출력**: 형식화된 표, 진행률 표시기, 색상 코드화된 결과
- **이진 통과/실패 테스트**: CI/CD 통합을 위한 명확한 성공/실패 기준
- **LangSmith 통합**: 자동 실험 추적 및 로깅
- **유연한 구성**: 다양한 테스트 시나리오를 위한 광범위한 CLI 옵션
- **실시간 피드백**: 테스트 실행 중 라이브 출력

#### **평가 기준:**

시스템은 9가지 포괄적인 품질 차원에 대해 보고서를 평가합니다:

- 주제 관련성 (전체 및 섹션 수준)
- 구조 및 논리적 흐름
- 서론 및 결론 품질
- 구조적 요소의 적절한 사용 (헤더, 인용)
- 마크다운 형식 준수
- 인용 품질 및 소스 속성
- 전체 연구 깊이 및 정확성

#### **사용법:**

```bash
# 기본 설정으로 모든 에이전트 실행
uv run python tests/run_test.py --all

# 사용자 정의 모델로 특정 에이전트 테스트
uv run python tests/run_test.py --agent multi_agent \
  --supervisor-model "anthropic:claude-3-7-sonnet-latest" \
  --search-api tavily

# OpenAI o3 모델로 테스트
uv run python tests/run_test.py --all \
  --supervisor-model "openai:o3" \
  --researcher-model "openai:o3" \
  --planner-provider "openai" \
  --planner-model "o3" \
  --writer-provider "openai" \
  --writer-model "o3" \
  --eval-model "openai:o3" \
  --search-api "tavily"
```

#### **주요 파일:**

- `tests/run_test.py`: 풍부한 CLI 인터페이스를 가진 메인 테스트 러너
- `tests/test_report_quality.py`: 핵심 테스트 구현
- `tests/conftest.py`: Pytest 구성 및 CLI 옵션

### 2. LangSmith Evaluate API 시스템

상세한 분석과 비교 연구를 위해 설계된 포괄적인 배치 평가 시스템입니다.

#### **기능:**

- **다차원 점수**: 1-5 척도 평가를 가진 4개의 전문화된 평가자
- **가중 기준**: 다양한 품질 측면에 대한 사용자 정의 가능한 가중치를 가진 상세한 점수
- **데이터셋 기반 평가**: 여러 테스트 사례에 걸친 배치 처리
- **성능 최적화**: 평가자 프롬프트에 대한 확장된 TTL을 가진 캐싱
- **전문적 보고**: 개선 권장사항이 포함된 구조화된 분석

#### **평가 차원:**

1. **전체 품질** (7가지 가중 기준):
   - 연구 깊이 및 소스 품질 (20%)
   - 분석적 엄격함 및 비판적 사고 (15%)
   - 구조 및 조직 (20%)
   - 실용적 가치 및 실행 가능성 (10%)
   - 균형 및 객관성 (15%)
   - 작성 품질 및 명확성 (10%)
   - 전문적 표현 (10%)

2. **관련성**: 엄격한 기준을 가진 섹션별 주제 관련성 분석

3. **구조**: 논리적 흐름, 형식화, 인용 관행의 평가

4. **근거**: 검색된 컨텍스트 및 소스와의 정렬 평가

#### **사용법:**

```bash
# LangSmith 데이터셋에서 포괄적인 평가 실행
uv run python tests/evals/run_evaluate.py
```

#### **주요 파일:**

- `tests/evals/run_evaluate.py`: 메인 평가 스크립트
- `tests/evals/evaluators.py`: 4개의 전문화된 평가자 함수
- `tests/evals/prompts.py`: 각 차원에 대한 상세한 평가 프롬프트
- `tests/evals/target.py`: 보고서 생성 워크플로우

### 각 시스템을 언제 사용할지

**Pytest 시스템 사용:**

- 개발 및 디버깅 사이클
- CI/CD 파이프라인 통합
- 빠른 모델 비교 실험
- 즉각적인 피드백을 가진 대화형 테스트
- 프로덕션 배포 전 게이트키핑

**LangSmith 시스템 사용:**

- 데이터셋에 걸친 포괄적인 모델 평가
- 시스템 성능의 연구 및 분석
- 상세한 성능 프로파일링 및 벤치마킹
- 다양한 구성 간의 비교 연구
- 프로덕션 모니터링 및 품질 보증

두 평가 시스템은 서로를 보완하며 다양한 사용 사례와 개발 단계에 대한 포괄적인 적용 범위를 제공합니다.

### 호스팅된 배포

[LangGraph Platform](https://langchain-ai.github.io/langgraph/concepts/#deployment-options)에 쉽게 배포할 수 있습니다.
