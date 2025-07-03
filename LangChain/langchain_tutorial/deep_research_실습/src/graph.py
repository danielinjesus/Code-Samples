from typing import Literal

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, Send, interrupt

from .configuration import WorkflowConfiguration
from .prompts import (
    final_section_writer_instructions,
    query_writer_instructions,
    report_planner_instructions,
    report_planner_query_writer_instructions,
    section_grader_instructions,
    section_writer_inputs,
    section_writer_instructions,
)
from .state import (
    Feedback,
    Queries,
    ReportState,
    ReportStateInput,
    ReportStateOutput,
    SectionOutputState,
    Sections,
    SectionState,
)
from .utils import (
    format_sections,
    get_config_value,
    get_search_params,
    get_today_str,
    select_and_execute_search,
)

## 노드 정의 --
# LangGraph 노드 문서: https://langchain-ai.github.io/langgraph/concepts/low_level/#nodes


async def generate_report_plan(state: ReportState, config: RunnableConfig):
    """Generate the initial report plan with sections.

    This node:
    1. Gets configuration for the report structure and search parameters
    2. Generates search queries to gather context for planning
    3. Performs web searches using those queries
    4. Uses an LLM to generate a structured plan with sections

    Args:
        state: Current graph state containing the report topic
        config: Configuration for models, search APIs, etc.

    Returns:
        Dict containing the generated sections
    """
    # 입력값
    topic = state["topic"]

    # 보고서 계획에 대한 피드백 목록 가져오기
    feedback_list = state.get("feedback_on_report_plan", [])

    # 보고서 계획에 대한 피드백을 하나의 문자열로 연결
    feedback = " /// ".join(feedback_list) if feedback_list else ""

    # 워크플로우 설정값 가져오기
    configurable = WorkflowConfiguration.from_runnable_config(config)
    report_structure = configurable.report_structure
    number_of_queries = configurable.number_of_queries
    search_api = get_config_value(configurable.search_api)
    search_api_config = (
        configurable.search_api_config or {}
    )  # Get the config dict, default to empty
    params_to_pass = get_search_params(
        search_api, search_api_config
    )  # Filter parameters

    # 필요한 경우 JSON 객체를 문자열로 변환
    if isinstance(report_structure, dict):
        report_structure = str(report_structure)

    # 작성자 모델 설정 (쿼리 작성에 사용되는 모델)
    writer_provider = get_config_value(configurable.writer_provider)
    writer_model_name = get_config_value(configurable.writer_model)
    writer_model_kwargs = get_config_value(configurable.writer_model_kwargs or {})
    writer_model = init_chat_model(
        model=writer_model_name,
        model_provider=writer_provider,
        model_kwargs=writer_model_kwargs,
    )
    structured_llm = writer_model.with_structured_output(Queries)

    # 시스템 지시사항 포맷팅
    system_instructions_query = report_planner_query_writer_instructions.format(
        topic=topic,
        report_organization=report_structure,
        number_of_queries=number_of_queries,
        today=get_today_str(),
    )

    # 쿼리 생성
    results = await structured_llm.ainvoke(
        [
            SystemMessage(content=system_instructions_query),
            HumanMessage(
                content="Generate search queries that will help with planning the sections of the report."
            ),
        ]
    )

    # 검색 쿼리 목록 추출
    query_list = [query.search_query for query in results.queries]

    # 매개변수를 사용하여 웹 검색
    source_str = await select_and_execute_search(search_api, query_list, params_to_pass)

    # 시스템 지시사항 포맷팅
    system_instructions_sections = report_planner_instructions.format(
        topic=topic,
        report_organization=report_structure,
        context=source_str,
        feedback=feedback,
    )

    # 플래너 설정
    planner_provider = get_config_value(configurable.planner_provider)
    planner_model = get_config_value(configurable.planner_model)
    planner_model_kwargs = get_config_value(configurable.planner_model_kwargs or {})

    # 보고서 플래너 지시사항
    planner_message = """Generate the sections of the report. Your response must include a 'sections' field containing a list of sections. 
                        Each section must have: name, description, research, and content fields."""

    # 플래너 실행
    if planner_model == "claude-3-7-sonnet-latest":
        # claude-3-7-sonnet-latest를 플래너 모델로 사용할 때 사고 예산 할당
        planner_llm = init_chat_model(
            model=planner_model,
            model_provider=planner_provider,
            max_tokens=20_000,
            thinking={"type": "enabled", "budget_tokens": 16_000},
        )

    else:
        # 다른 모델의 경우 사고 토큰이 특별히 할당되지 않음
        planner_llm = init_chat_model(
            model=planner_model,
            model_provider=planner_provider,
            model_kwargs=planner_model_kwargs,
        )

    # 보고서 섉션 생성
    structured_llm = planner_llm.with_structured_output(Sections)
    report_sections = await structured_llm.ainvoke(
        [
            SystemMessage(content=system_instructions_sections),
            HumanMessage(content=planner_message),
        ]
    )

    # 원래 계획의 섉션과 완성된 섉션 가져오기
    sections = report_sections.sections

    return {"sections": sections}


def human_feedback(
    state: ReportState, config: RunnableConfig
) -> Command[Literal["generate_report_plan", "build_section_with_web_research"]]:
    """Get human feedback on the report plan and route to next steps.

    This node:
    1. Formats the current report plan for human review
    2. Gets feedback via an interrupt
    3. Routes to either:
       - Section writing if plan is approved
       - Plan regeneration if feedback is provided

    Args:
        state: Current graph state with sections to review
        config: Configuration for the workflow

    Returns:
        Command to either regenerate plan or start section writing
    """
    # 원래 계획의 섉션과 완성된 섉션 가져오기
    topic = state["topic"]
    sections = state["sections"]
    sections_str = "\n\n".join(
        f"Section: {section.name}\n"
        f"Description: {section.description}\n"
        f"Research needed: {'Yes' if section.research else 'No'}\n"
        for section in sections
    )

    # interrupt를 통해 보고서 계획에 대한 피드백 받기
    # LangGraph Human-in-the-loop 문서: https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/
    interrupt_message = f"""Please provide feedback on the following report plan. 
                        \n\n{sections_str}\n
                        \nDoes the report plan meet your needs?\nPass 'true' to approve the report plan.\nOr, provide feedback to regenerate the report plan:"""

    feedback = interrupt(interrupt_message)

    # 사용자가 보고서 계획을 승인하면 섹션 작성 시작
    if isinstance(feedback, bool) and feedback is True:
        # 승인으로 처리하고 섹션 작성 시작
        # LangGraph Send API 문서: https://langchain-ai.github.io/langgraph/concepts/low_level/#send
        return Command(
            goto=[
                Send(
                    "build_section_with_web_research",
                    {"topic": topic, "section": s, "search_iterations": 0},
                )
                for s in sections
                if s.research
            ]
        )

    # 사용자가 피드백을 제공하면 보고서 계획 재생성
    elif isinstance(feedback, str):
        # 피드백으로 처리하고 기존 목록에 추가
        # LangGraph Command 문서: https://langchain-ai.github.io/langgraph/concepts/low_level/#command
        return Command(
            goto="generate_report_plan", update={"feedback_on_report_plan": [feedback]}
        )
    else:
        raise TypeError(f"Interrupt value of type {type(feedback)} is not supported.")


async def generate_queries(state: SectionState, config: RunnableConfig):
    """Generate search queries for researching a specific section.

    This node uses an LLM to generate targeted search queries based on the
    section topic and description.

    Args:
        state: Current state containing section details
        config: Configuration including number of queries to generate

    Returns:
        Dict containing the generated search queries
    """
    # 상태 가져오기
    topic = state["topic"]
    section = state["section"]

    # 워크플로우 설정값 가져오기
    configurable = WorkflowConfiguration.from_runnable_config(config)
    number_of_queries = configurable.number_of_queries

    # 쿼리 생성
    writer_provider = get_config_value(configurable.writer_provider)
    writer_model_name = get_config_value(configurable.writer_model)
    writer_model_kwargs = get_config_value(configurable.writer_model_kwargs or {})
    writer_model = init_chat_model(
        model=writer_model_name,
        model_provider=writer_provider,
        model_kwargs=writer_model_kwargs,
    )
    structured_llm = writer_model.with_structured_output(Queries)

    # 시스템 지시사항 포맷팅
    system_instructions = query_writer_instructions.format(
        topic=topic,
        section_topic=section.description,
        number_of_queries=number_of_queries,
        today=get_today_str(),
    )

    # 쿼리 생성
    queries = await structured_llm.ainvoke(
        [
            SystemMessage(content=system_instructions),
            HumanMessage(content="Generate search queries on the provided topic."),
        ]
    )

    return {"search_queries": queries.queries}


async def search_web(state: SectionState, config: RunnableConfig):
    """Execute web searches for the section queries.

    This node:
    1. Takes the generated queries
    2. Executes searches using configured search API
    3. Formats results into usable context

    Args:
        state: Current state with search queries
        config: Search API configuration

    Returns:
        Dict with search results and updated iteration count
    """
    # 상태 가져오기
    search_queries = state["search_queries"]

    # 워크플로우 설정값 가져오기
    configurable = WorkflowConfiguration.from_runnable_config(config)
    search_api = get_config_value(configurable.search_api)
    search_api_config = (
        configurable.search_api_config or {}
    )  # Get the config dict, default to empty
    params_to_pass = get_search_params(
        search_api, search_api_config
    )  # Filter parameters

    # 검색 쿼리 목록 추출
    query_list = [query.search_query for query in search_queries]

    # 매개변수를 사용하여 웹 검색
    source_str = await select_and_execute_search(search_api, query_list, params_to_pass)

    return {
        "source_str": source_str,
        "search_iterations": state["search_iterations"] + 1,
    }


async def write_section(
    state: SectionState, config: RunnableConfig
) -> Command[Literal[END, "search_web"]]:
    """Write a section of the report and evaluate if more research is needed.

    This node:
    1. Writes section content using search results
    2. Evaluates the quality of the section
    3. Either:
       - Completes the section if quality passes
       - Triggers more research if quality fails

    Args:
        state: Current state with search results and section info
        config: Configuration for writing and evaluation

    Returns:
        Command to either complete section or do more research
    """
    # 상태 가져오기
    topic = state["topic"]
    section = state["section"]
    source_str = state["source_str"]

    # 워크플로우 설정값 가져오기
    configurable = WorkflowConfiguration.from_runnable_config(config)

    # 시스템 지시사항 포맷팅
    section_writer_inputs_formatted = section_writer_inputs.format(
        topic=topic,
        section_name=section.name,
        section_topic=section.description,
        context=source_str,
        section_content=section.content,
    )

    # 섉션 생성
    writer_provider = get_config_value(configurable.writer_provider)
    writer_model_name = get_config_value(configurable.writer_model)
    writer_model_kwargs = get_config_value(configurable.writer_model_kwargs or {})
    writer_model = init_chat_model(
        model=writer_model_name,
        model_provider=writer_provider,
        model_kwargs=writer_model_kwargs,
    )

    section_content = await writer_model.ainvoke(
        [
            SystemMessage(content=section_writer_instructions),
            HumanMessage(content=section_writer_inputs_formatted),
        ]
    )

    # 섉션 객체에 내용 작성
    section.content = section_content.content

    # 평가 프롬프트
    section_grader_message = (
        "Grade the report and consider follow-up questions for missing information. "
        "If the grade is 'pass', return empty strings for all follow-up queries. "
        "If the grade is 'fail', provide specific search queries to gather missing information."
    )

    section_grader_instructions_formatted = section_grader_instructions.format(
        topic=topic,
        section_topic=section.description,
        section=section.content,
        number_of_follow_up_queries=configurable.number_of_queries,
    )

    # 성찰을 위해 플래너 모델 사용
    planner_provider = get_config_value(configurable.planner_provider)
    planner_model = get_config_value(configurable.planner_model)
    planner_model_kwargs = get_config_value(configurable.planner_model_kwargs or {})

    if planner_model == "claude-3-7-sonnet-latest":
        # claude-3-7-sonnet-latest를 플래너 모델로 사용할 때 사고 예산 할당
        reflection_model = init_chat_model(
            model=planner_model,
            model_provider=planner_provider,
            max_tokens=20_000,
            thinking={"type": "enabled", "budget_tokens": 16_000},
        ).with_structured_output(Feedback)
    else:
        reflection_model = init_chat_model(
            model=planner_model,
            model_provider=planner_provider,
            model_kwargs=planner_model_kwargs,
        ).with_structured_output(Feedback)
    # 피드백 생성
    feedback = await reflection_model.ainvoke(
        [
            SystemMessage(content=section_grader_instructions_formatted),
            HumanMessage(content=section_grader_message),
        ]
    )

    # 섉션이 통과하거나 최대 검색 깊이에 도달하면 완료된 섉션으로 게시
    if (
        feedback.grade == "pass"
        or state["search_iterations"] >= configurable.max_search_depth
    ):
        # 완료된 섉션으로 게시
        update = {"completed_sections": [section]}
        if configurable.include_source_str:
            update["source_str"] = source_str
        return Command(update=update, goto=END)

    # 기존 섉션을 새 내용으로 업데이트하고 검색 쿼리 업데이트
    else:
        return Command(
            update={"search_queries": feedback.follow_up_queries, "section": section},
            goto="search_web",
        )


async def write_final_sections(state: SectionState, config: RunnableConfig):
    """Write sections that don't require research using completed sections as context.

    This node handles sections like conclusions or summaries that build on
    the researched sections rather than requiring direct research.

    Args:
        state: Current state with completed sections as context
        config: Configuration for the writing model

    Returns:
        Dict containing the newly written section
    """
    # 워크플로우 설정값 가져오기
    configurable = WorkflowConfiguration.from_runnable_config(config)

    # 상태 가져오기
    topic = state["topic"]
    section = state["section"]
    completed_report_sections = state["report_sections_from_research"]

    # 시스템 지시사항 포맷팅
    system_instructions = final_section_writer_instructions.format(
        topic=topic,
        section_name=section.name,
        section_topic=section.description,
        context=completed_report_sections,
    )

    # 섉션 생성
    writer_provider = get_config_value(configurable.writer_provider)
    writer_model_name = get_config_value(configurable.writer_model)
    writer_model_kwargs = get_config_value(configurable.writer_model_kwargs or {})
    writer_model = init_chat_model(
        model=writer_model_name,
        model_provider=writer_provider,
        model_kwargs=writer_model_kwargs,
    )

    section_content = await writer_model.ainvoke(
        [
            SystemMessage(content=system_instructions),
            HumanMessage(
                content="Generate a report section based on the provided sources."
            ),
        ]
    )

    # 섉션에 내용 작성
    section.content = section_content.content

    # 업데이트된 섉션을 완료된 섉션으로 작성
    return {"completed_sections": [section]}


def gather_completed_sections(state: ReportState):
    """Format completed sections as context for writing final sections.

    This node takes all completed research sections and formats them into
    a single context string for writing summary sections.

    Args:
        state: Current state with completed sections

    Returns:
        Dict with formatted sections as context
    """
    # 완료된 섉션 목록
    completed_sections = state["completed_sections"]

    # 완료된 섉션을 최종 섉션의 컨텍스트로 사용하기 위해 문자열로 포맷
    completed_report_sections = format_sections(completed_sections)

    return {"report_sections_from_research": completed_report_sections}


def compile_final_report(state: ReportState, config: RunnableConfig):
    """Compile all sections into the final report.

    This node:
    1. Gets all completed sections
    2. Orders them according to original plan
    3. Combines them into the final report

    Args:
        state: Current state with all completed sections

    Returns:
        Dict containing the complete report
    """
    # 워크플로우 설정값 가져오기
    configurable = WorkflowConfiguration.from_runnable_config(config)

    # 원래 계획의 섉션과 완성된 섉션 가져오기
    sections = state["sections"]
    completed_sections = {s.name: s.content for s in state["completed_sections"]}

    # 원래 계획의 순서를 유지하면서 완성된 내용으로 섉션 업데이트
    for section in sections:
        section.content = completed_sections[section.name]

    # 모든 섉션을 하나의 최종 보고서로 결합
    all_sections = "\n\n".join([s.content for s in sections])

    if configurable.include_source_str:
        return {"final_report": all_sections, "source_str": state["source_str"]}
    else:
        return {"final_report": all_sections}


def initiate_final_section_writing(state: ReportState):
    """Create parallel tasks for writing non-research sections.

    This edge function identifies sections that don't need research and
    creates parallel writing tasks for each one.

    Args:
        state: Current state with all sections and research context

    Returns:
        List of Send commands for parallel section writing
    """
    # 연구가 필요하지 않은 섉션(예: 결론)에 대해 Send API를 사용하여 병렬로 작성 시작
    # 각 섉션은 독립적으로 처리되므로 동시 실행이 가능합니다
    return [
        Send(
            "write_final_sections",
            {
                "topic": state["topic"],
                "section": s,
                "report_sections_from_research": state["report_sections_from_research"],
            },
        )
        for s in state["sections"]
        if not s.research
    ]


# 보고서 섉션 서브그래프 --
# 서브그래프는 재사용 가능한 그래프 컴포넌트로, 각 섉션 작성을 위한 독립적인 워크플로우입니다.
# LangGraph 서브그래프 문서: https://langchain-ai.github.io/langgraph/concepts/low_level/#subgraphs

# 섉션 작성을 위한 노드 추가
section_builder = StateGraph(SectionState, output=SectionOutputState)
section_builder.add_node("generate_queries", generate_queries)
section_builder.add_node("search_web", search_web)
section_builder.add_node("write_section", write_section)

# 섉션 작성 워크플로우의 엣지 추가
# 엣지는 노드 간의 실행 순서를 정의합니다
# LangGraph 엣지 문서: https://langchain-ai.github.io/langgraph/concepts/low_level/#edges
section_builder.add_edge(START, "generate_queries")
section_builder.add_edge("generate_queries", "search_web")
section_builder.add_edge("search_web", "write_section")

# 메인 그래프 정의 --
# 이 그래프는 전체 보고서 생성 프로세스를 관리하고 섉션 서브그래프를 조율합니다

# 섉션 작성을 위한 노드 추가
builder = StateGraph(
    ReportState,
    input=ReportStateInput,
    output=ReportStateOutput,
    config_schema=WorkflowConfiguration,
)
builder.add_node("generate_report_plan", generate_report_plan)
builder.add_node("human_feedback", human_feedback)
builder.add_node("build_section_with_web_research", section_builder.compile())
builder.add_node("gather_completed_sections", gather_completed_sections)
builder.add_node("write_final_sections", write_final_sections)
builder.add_node("compile_final_report", compile_final_report)

# 섉션 작성 워크플로우의 엣지 추가
# 엣지는 노드 간의 실행 순서를 정의합니다
# LangGraph 엣지 문서: https://langchain-ai.github.io/langgraph/concepts/low_level/#edges
builder.add_edge(START, "generate_report_plan")
builder.add_edge("generate_report_plan", "human_feedback")
builder.add_edge("build_section_with_web_research", "gather_completed_sections")
builder.add_conditional_edges(
    "gather_completed_sections",
    initiate_final_section_writing,
    ["write_final_sections"],
)
builder.add_edge("write_final_sections", "compile_final_report")
builder.add_edge("compile_final_report", END)

graph = builder.compile()
