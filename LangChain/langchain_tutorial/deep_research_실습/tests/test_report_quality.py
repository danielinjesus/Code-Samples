#!/usr/bin/env python

import asyncio
import os
import uuid

import pytest
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from langsmith import testing as t
from pydantic import BaseModel, Field
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table

# 보고서 생성 에이전트 임포트
from src.graph import builder
from src.multi_agent import supervisor_builder

# pytest가 stdout을 캡처하더라도 출력을 보장하기 위해 force_terminal로 rich 콘솔 초기화
console = Console(force_terminal=True, width=120)


class CriteriaGrade(BaseModel):
    """특정 기준에 대해 응답을 평가."""

    grade: bool = Field(description="응답이 제공된 기준을 충족하는가?")
    justification: str = Field(
        description="응답의 구체적인 예시를 포함한 등급과 점수에 대한 정당화"
    )


# 테스트 시점에 평가 LLM을 생성하는 함수
def get_evaluation_llm(eval_model=None):
    """평가 LLM을 생성하고 반환.

    Args:
        eval_model: 평가에 사용할 모델 식별자
                    형식: "provider:model_name" (예: "anthropic:claude-3-7-sonnet-latest")
                    None인 경우 환경 변수 또는 기본값 사용

    Returns:
        평가 등급을 생성하기 위한 구조화된 LLM

    참고:
        LangChain 모델 초기화: https://python.langchain.com/docs/how_to/chat_models_universal_init/
    """
    # 제공된 모델 사용, 그 다음 환경 변수, 마지막으로 기본값
    model_to_use = eval_model or os.environ.get(
        "EVAL_MODEL", "anthropic:claude-3-7-sonnet-latest"
    )

    criteria_eval_llm = init_chat_model(model_to_use)
    return criteria_eval_llm.with_structured_output(CriteriaGrade)


RESPONSE_CRITERIA_SYSTEM_PROMPT = """
You are evaluating the quality of a research report. Please assess the report against the following criteria, being especially strict about section relevance.

1. Topic Relevance (Overall): Does the report directly address the user's input topic thoroughly?

2. Section Relevance (Critical): CAREFULLY assess each individual section for relevance to the main topic:
   - Identify each section by its ## header
   - For each section, determine if it is directly relevant to the primary topic
   - Flag any sections that seem tangential, off-topic, or only loosely connected to the main topic
   - A high-quality report should have NO irrelevant sections

3. Structure and Flow: Do the sections flow logically from one to the next, creating a cohesive narrative?

4. Introduction Quality: Does the introduction effectively provide context and set up the scope of the report?

5. Conclusion Quality: Does the conclusion meaningfully summarize key findings and insights from the report?

6. Structural Elements: Does the report use structural elements (e.g., tables, lists) to effectively convey information?

7. Section Headers: Are section headers properly formatted with Markdown (# for title, ## for sections, ### for subsections)?

8. Citations: Does the report properly cite sources in each main body section?

9. Overall Quality: Is the report well-researched, accurate, and professionally written?

Evaluation Instructions:
- Be STRICT about section relevance - ALL sections must clearly connect to the primary topic
- A report with even ONE irrelevant section should be considered flawed
- You must individually mention each section by name and assess its relevance
- Provide specific examples from the report to justify your evaluation for each criterion
- The report fails if any sections are irrelevant to the main topic, regardless of other qualities
"""


# 테스트 구성을 위한 픽스처 정의
@pytest.fixture
def research_agent(request):
    """커맨드라인이나 환경 변수에서 연구 에이전트 타입 가져오기."""
    return request.config.getoption("--research-agent") or os.environ.get(
        "RESEARCH_AGENT", "multi_agent"
    )


@pytest.fixture
def search_api(request):
    """커맨드라인이나 환경 변수에서 검색 API 가져오기."""
    return request.config.getoption("--search-api") or os.environ.get(
        "SEARCH_API", "tavily"
    )


@pytest.fixture
def eval_model(request):
    """커맨드라인이나 환경 변수에서 평가 모델 가져오기."""
    return request.config.getoption("--eval-model") or os.environ.get(
        "EVAL_MODEL", "anthropic:claude-3-7-sonnet-latest"
    )


@pytest.fixture
def models(request, research_agent):
    """에이전트 타입에 따른 모델 구성 가져오기."""
    if research_agent == "multi_agent":
        return {
            "supervisor_model": (
                request.config.getoption("--supervisor-model")
                or os.environ.get(
                    "SUPERVISOR_MODEL", "anthropic:claude-3-7-sonnet-latest"
                )
            ),
            "researcher_model": (
                request.config.getoption("--researcher-model")
                or os.environ.get(
                    "RESEARCHER_MODEL", "anthropic:claude-3-5-sonnet-latest"
                )
            ),
        }
    else:  # graph agent
        return {
            "planner_provider": (
                request.config.getoption("--planner-provider")
                or os.environ.get("PLANNER_PROVIDER", "anthropic")
            ),
            "planner_model": (
                request.config.getoption("--planner-model")
                or os.environ.get("PLANNER_MODEL", "claude-3-7-sonnet-latest")
            ),
            "writer_provider": (
                request.config.getoption("--writer-provider")
                or os.environ.get("WRITER_PROVIDER", "anthropic")
            ),
            "writer_model": (
                request.config.getoption("--writer-model")
                or os.environ.get("WRITER_MODEL", "claude-3-5-sonnet-latest")
            ),
            "max_search_depth": int(
                request.config.getoption("--max-search-depth")
                or os.environ.get("MAX_SEARCH_DEPTH", "2")
            ),
        }


# 참고: 커맨드라인 옵션은 conftest.py에 정의되어 있음
# 이 픽스처들은 거기에 정의된 옵션들과 함께 작동함


@pytest.mark.langsmith
def test_response_criteria_evaluation(research_agent, search_api, models, eval_model):
    """
    보고서가 지정된 품질 기준을 충족하는지 테스트.

    이 테스트는 선택된 에이전트를 사용하여 MCP에 대한 보고서를 생성하고,
    9가지 품질 기준에 대해 평가합니다.

    참고:
        LangSmith 테스팅: https://docs.smith.langchain.com/how_to_guides/evaluation/integrate_expts_in_app
    """
    console.print(
        Panel.fit(
            f"[bold blue]Testing {research_agent} report generation with {search_api} search[/bold blue]",
            title="Test Configuration",
        )
    )

    # 모델 구성을 위한 테이블 생성
    models_table = Table(title="Model Configuration")
    models_table.add_column("Parameter", style="cyan")
    models_table.add_column("Value", style="green")

    for key, value in models.items():
        models_table.add_row(key, str(value))
    models_table.add_row("eval_model", eval_model)

    console.print(models_table)

    # LangSmith에 입력값 로깅
    t.log_inputs(
        {
            "agent_type": research_agent,
            "search_api": search_api,
            "models": models,
            "eval_model": eval_model,
            "test": "report_quality_evaluation",
            "description": f"Testing report quality for {research_agent} with {search_api}",
        }
    )

    # 매개변수에 따라 적절한 에이전트 실행
    if research_agent == "multi_agent":
        # 초기 메시지
        initial_msg = [
            {
                "role": "user",
                "content": "Give me a high-level overview of MCP (model context protocol). Keep the report to 3 main body sections. One section on the origins of MPC, one section on interesting examples of MCP servers, and one section on the future roadmap for MCP. Report should be written for a developer audience.",
            }
        ]

        # 멀티 에이전트 접근을 위한 체크포인터
        checkpointer = MemorySaver()
        graph = supervisor_builder.compile(checkpointer=checkpointer)

        # 제공된 매개변수로 구성 생성
        config = {
            "thread_id": str(uuid.uuid4()),
            "search_api": search_api,
            "supervisor_model": models.get("supervisor_model"),
            "researcher_model": models.get("researcher_model"),
            "ask_for_clarification": False,  # 사용자에게 명확화를 요청하지 않고 보고서 작성 진행
            "process_search_results": "summarize",  # 선택적으로 요약
        }

        thread_config = {"configurable": config}

        # asyncio로 워크플로우 실행
        asyncio.run(graph.ainvoke({"messages": initial_msg}, config=thread_config))

        # 두 호출이 완료되면 최종 상태 가져오기
        final_state = graph.get_state(thread_config)
        report = final_state.values.get("final_report", "No report generated")
        console.print(
            f"[bold green]Report generated with length: {len(report)} characters[/bold green]"
        )

    elif research_agent == "graph":
        # 토픽 쿼리
        topic_query = "Give me a high-level overview of MCP (model context protocol). Keep the report to 3 main body sections. One section on the origins of MPC, one section on interesting examples of MCP servers, and one section on the future roadmap for MCP. Report should be written for a developer audience."

        # 그래프 접근을 위한 체크포인터
        checkpointer = MemorySaver()
        graph = builder.compile(checkpointer=checkpointer)

        # 제공된 매개변수로 그래프 에이전트 구성
        thread = {
            "configurable": {
                "thread_id": str(uuid.uuid4()),
                "search_api": search_api,
                "planner_provider": models.get("planner_provider", "anthropic"),
                "planner_model": models.get(
                    "planner_model", "claude-3-7-sonnet-latest"
                ),
                "writer_provider": models.get("writer_provider", "anthropic"),
                "writer_model": models.get("writer_model", "claude-3-5-sonnet-latest"),
                "max_search_depth": models.get("max_search_depth", 2),
            }
        }

        async def run_graph_agent(thread):
            # 중단까지 그래프 실행
            async for event in graph.astream(
                {"topic": topic_query}, thread, stream_mode="updates"
            ):
                if "__interrupt__" in event:
                    pass  # interrupt_value = event["__interrupt__"][0].value

            # True를 전달하여 보고서 계획을 승인하고 보고서 작성 진행
            async for event in graph.astream(
                Command(resume=True), thread, stream_mode="updates"
            ):
                # console.print(f"[dim]{event}[/dim]")
                # console.print()
                None

            final_state = graph.get_state(thread)
            report = final_state.values.get("final_report", "No report generated")
            return report

        report = asyncio.run(run_graph_agent(thread))

    # 지정된 모델을 사용하여 평가 LLM 가져오기
    criteria_eval_structured_llm = get_evaluation_llm(eval_model)

    # 품질 기준에 대해 보고서 평가
    eval_result = criteria_eval_structured_llm.invoke(
        [
            {"role": "system", "content": RESPONSE_CRITERIA_SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""\n\n Report: \n\n{report}\n\nEvaluate whether the report meets the criteria and provide detailed justification for your evaluation.""",
            },
        ]
    )

    # 분석을 위해 섹션 헤더 추출
    import re

    section_headers = re.findall(r"##\s+([^\n]+)", report)

    # 생성된 보고서 표시
    console.print(
        Panel(Markdown(report), title="Generated Report", border_style="blue")
    )

    # 평가 결과 표시 생성
    result_color = "green" if eval_result.grade else "red"
    result_text = "PASSED" if eval_result.grade else "FAILED"

    console.print(
        Panel.fit(
            f"[bold {result_color}]{result_text}[/bold {result_color}]",
            title="Evaluation Result",
        )
    )

    # 섹션 테이블 생성
    sections_table = Table(title="Report Structure Analysis")
    sections_table.add_column("Section", style="cyan")
    sections_table.add_column("Header", style="yellow")

    for i, header in enumerate(section_headers, 1):
        sections_table.add_row(f"Section {i}", header)

    console.print(sections_table)
    console.print(f"[bold]Total sections found: {len(section_headers)}[/bold]")

    # 패널에 정당화 표시
    console.print(
        Panel(
            eval_result.justification,
            title="Evaluation Justification",
            border_style="yellow",
        )
    )

    # LangSmith에 출력값 로깅
    t.log_outputs(
        {
            "report": report,
            "evaluation_result": eval_result.grade,
            "justification": eval_result.justification,
            "report_length": len(report),
            "section_count": len(section_headers),
            "section_headers": section_headers,
        }
    )

    # 평가 기준이 충족되면 테스트 통과
    assert eval_result.grade
