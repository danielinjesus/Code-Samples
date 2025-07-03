import os
from dataclasses import dataclass, fields
from enum import Enum
from typing import Any, Dict, Literal, Optional

from langchain_core.runnables import RunnableConfig

# 기본 보고서 구조 템플릿
# 사용자가 제공한 주제에 대한 보고서 생성 시 이 구조를 사용합니다.
DEFAULT_REPORT_STRUCTURE = """Use this structure to create a report on the user-provided topic:

1. Introduction (no research needed)
   - Brief overview of the topic area

2. Main Body Sections:
   - Each section should focus on a sub-topic of the user-provided topic
   
3. Conclusion
   - Aim for 1 structural element (either a list or table) that distills the main body sections 
   - Provide a concise summary of the report"""


class SearchAPI(Enum):
    """지원되는 검색 API 열거형.

    다양한 검색 소스에서 정보를 수집하기 위한 API 옵션들입니다.
    """

    PERPLEXITY = "perplexity"
    TAVILY = "tavily"
    EXA = "exa"
    ARXIV = "arxiv"
    PUBMED = "pubmed"
    LINKUP = "linkup"
    DUCKDUCKGO = "duckduckgo"
    GOOGLESEARCH = "googlesearch"
    NONE = "none"


@dataclass(kw_only=True)
class WorkflowConfiguration:
    """워크플로우/그래프 기반 구현(graph.py)을 위한 구성 클래스.

    LangGraph의 StateGraph를 사용하여 계획-실행 워크플로우를 구성합니다.

    참고:
        LangGraph StateGraph: https://python.langchain.com/docs/langgraph/concepts/low_level#stategraph
        LangGraph 구성: https://python.langchain.com/docs/langgraph/how-tos/configuration
    """

    # 공통 구성 옵션
    report_structure: str = DEFAULT_REPORT_STRUCTURE
    search_api: SearchAPI = SearchAPI.TAVILY
    search_api_config: Optional[Dict[str, Any]] = None
    process_search_results: Literal["summarize", "split_and_rerank"] | None = None
    summarization_model_provider: str = "anthropic"
    summarization_model: str = "claude-3-5-haiku-latest"
    max_structured_output_retries: int = 3
    include_source_str: bool = False

    # 워크플로우 전용 구성 옵션
    number_of_queries: int = 2  # 반복당 생성할 검색 쿼리 수
    max_search_depth: int = 2  # 반성 + 검색 반복의 최대 횟수
    planner_provider: str = "anthropic"
    planner_model: str = "claude-3-7-sonnet-latest"
    planner_model_kwargs: Optional[Dict[str, Any]] = None
    writer_provider: str = "anthropic"
    writer_model: str = "claude-3-7-sonnet-latest"
    writer_model_kwargs: Optional[Dict[str, Any]] = None

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "WorkflowConfiguration":
        """RunnableConfig에서 WorkflowConfiguration 인스턴스를 생성합니다.

        LangGraph의 RunnableConfig를 통해 런타임에 구성을 동적으로 설정할 수 있습니다.

        Args:
            config: LangGraph RunnableConfig 객체

        Returns:
            WorkflowConfiguration: 구성된 워크플로우 설정 객체

        참고:
            RunnableConfig: https://python.langchain.com/docs/langgraph/concepts/low_level#runnableconfig
        """
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})


@dataclass(kw_only=True)
class MultiAgentConfiguration:
    """멀티 에이전트 구현(multi_agent.py)을 위한 구성 클래스.

    슈퍼바이저-연구원 아키텍처를 사용하여 병렬 연구를 수행합니다.

    참고:
        LangGraph 멀티 에이전트: https://python.langchain.com/docs/langgraph/concepts/multi_agent
        LangGraph 에이전트: https://python.langchain.com/docs/langgraph/concepts/agentic_concepts
    """

    # 공통 구성 옵션
    search_api: SearchAPI = SearchAPI.TAVILY
    search_api_config: Optional[Dict[str, Any]] = None
    process_search_results: Literal["summarize", "split_and_rerank"] | None = None
    summarization_model_provider: str = "anthropic"
    summarization_model: str = "claude-3-5-haiku-latest"
    include_source_str: bool = False

    # 멀티 에이전트 전용 구성 옵션
    number_of_queries: int = 2  # 섹션당 생성할 검색 쿼리 수
    supervisor_model: str = "anthropic:claude-3-7-sonnet-latest"
    researcher_model: str = "anthropic:claude-3-7-sonnet-latest"
    ask_for_clarification: bool = False  # 사용자에게 명확한 설명을 요청할지 여부
    # MCP(Model Context Protocol) 서버 구성
    mcp_server_config: Optional[Dict[str, Any]] = None
    mcp_prompt: Optional[str] = None
    mcp_tools_to_include: Optional[list[str]] = None

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "MultiAgentConfiguration":
        """RunnableConfig에서 MultiAgentConfiguration 인스턴스를 생성합니다.

        LangGraph의 RunnableConfig를 통해 런타임에 구성을 동적으로 설정할 수 있습니다.

        Args:
            config: LangGraph RunnableConfig 객체

        Returns:
            MultiAgentConfiguration: 구성된 멀티 에이전트 설정 객체

        참고:
            RunnableConfig: https://python.langchain.com/docs/langgraph/concepts/low_level#runnableconfig
        """
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})


# 하위 호환성을 위해 이전 Configuration 클래스 유지
Configuration = WorkflowConfiguration
