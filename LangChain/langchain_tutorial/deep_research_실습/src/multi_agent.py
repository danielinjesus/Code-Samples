import operator
import warnings
from typing import Annotated, List, Literal, TypedDict, cast

from langchain.chat_models import init_chat_model
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, tool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.types import Command, Send
from pydantic import BaseModel, Field

from .configuration import MultiAgentConfiguration
from .prompts import RESEARCH_INSTRUCTIONS, SUPERVISOR_INSTRUCTIONS
from .utils import (
    duckduckgo_search,
    get_config_value,
    get_today_str,
    tavily_search,
)


## 도구 팩토리 - 설정에 따라 초기화됨
# LangGraph 도구 문서: https://langchain-ai.github.io/langgraph/concepts/low_level/#tools
def get_search_tool(config: RunnableConfig):
    """설정에 따라 적절한 검색 도구를 가져옴.

    LangGraph 설정 문서: https://langchain-ai.github.io/langgraph/concepts/configuration/
    """
    configurable = MultiAgentConfiguration.from_runnable_config(config)
    search_api = get_config_value(configurable.search_api)

    # 검색 도구가 요청되지 않은 경우 None 반환
    if search_api.lower() == "none":
        return None

    # TODO: 다른 검색 기능을 도구로 구성
    if search_api.lower() == "tavily":
        search_tool = tavily_search
    elif search_api.lower() == "duckduckgo":
        search_tool = duckduckgo_search
    else:
        raise NotImplementedError(
            f"The search API '{search_api}' is not yet supported in the multi-agent implementation. "
            f"Currently, only Tavily/DuckDuckGo/None is supported. Please use the graph-based implementation in "
            f"src/graph.py for other search APIs, or set search_api to 'tavily', 'duckduckgo', or 'none'."
        )

    tool_metadata = {**(search_tool.metadata or {}), "type": "search"}
    search_tool.metadata = tool_metadata
    return search_tool


class Section(BaseModel):
    """보고서의 섹션."""

    name: str = Field(
        description="보고서의 이 섹션 이름",
    )
    description: str = Field(
        description="보고서의 이 섹션에 대한 연구 범위",
    )
    content: str = Field(description="섹션의 내용")


class Sections(BaseModel):
    """보고서의 섹션 제목 목록."""

    sections: List[str] = Field(
        description="보고서의 섹션들",
    )


class Introduction(BaseModel):
    """보고서의 서론."""

    name: str = Field(
        description="보고서 이름",
    )
    content: str = Field(description="보고서 개요를 제공하는 서론의 내용")


class Conclusion(BaseModel):
    """보고서의 결론."""

    name: str = Field(
        description="보고서 결론의 이름",
    )
    content: str = Field(description="보고서를 요약하는 결론의 내용")


class Question(BaseModel):
    """보고서 범위를 명확히 하기 위한 후속 질문."""

    question: str = Field(
        description="보고서의 범위, 초점 또는 요구사항을 명확히 하기 위해 사용자에게 묻는 구체적인 질문"
    )


# 연구가 완료되었음을 나타내는 No-op 도구
class FinishResearch(BaseModel):
    """연구 완료."""


# 보고서 작성이 완료되었음을 나타내는 No-op 도구
class FinishReport(BaseModel):
    """보고서 작성 완료."""


## 상태 정의
# LangGraph 상태 문서: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
class ReportStateOutput(MessagesState):
    final_report: str  # 최종 보고서
    # 평가 목적으로만 사용
    # configurable.include_source_str이 True인 경우에만 포함됨
    source_str: str  # 웹 검색에서 가져온 포맷된 소스 콘텐츠 문자열


class ReportState(MessagesState):
    sections: list[str]  # 보고서 섉션 목록
    completed_sections: Annotated[list[Section], operator.add]  # Send() API 키
    final_report: str  # 최종 보고서
    # 평가 목적으로만 사용
    # configurable.include_source_str이 True인 경우에만 포함됨
    source_str: Annotated[
        str, operator.add
    ]  # 웹 검색에서 가져온 포맷된 소스 콘텐츠 문자열


class SectionState(MessagesState):
    section: str  # 보고서 섉션
    completed_sections: list[Section]  # Send() API를 위해 외부 상태에 복사하는 최종 키
    # 평가 목적으로만 사용
    # configurable.include_source_str이 True인 경우에만 포함됨
    source_str: str  # 웹 검색에서 가져온 포맷된 소스 콘텐츠 문자열


class SectionOutputState(TypedDict):
    completed_sections: list[Section]  # Send() API를 위해 외부 상태에 복사하는 최종 키
    # 평가 목적으로만 사용
    # configurable.include_source_str이 True인 경우에만 포함됨
    source_str: str  # 웹 검색에서 가져온 포맷된 소스 콘텐츠 문자열


async def _load_mcp_tools(
    config: RunnableConfig,
    existing_tool_names: set[str],
) -> list[BaseTool]:
    configurable = MultiAgentConfiguration.from_runnable_config(config)
    if not configurable.mcp_server_config:
        return []

    mcp_server_config = configurable.mcp_server_config
    client = MultiServerMCPClient(mcp_server_config)
    mcp_tools = await client.get_tools()
    filtered_mcp_tools: list[BaseTool] = []
    for tool in mcp_tools:
        # TODO: this will likely be hard to manage
        # on a remote server that's not controlled by the developer
        # best solution here is allowing tool name prefixes in MultiServerMCPClient
        if tool.name in existing_tool_names:
            warnings.warn(
                f"Trying to add MCP tool with a name {tool.name} that is already in use - this tool will be ignored."
            )
            continue

        if (
            configurable.mcp_tools_to_include
            and tool.name not in configurable.mcp_tools_to_include
        ):
            continue

        filtered_mcp_tools.append(tool)

    return filtered_mcp_tools


# 도구 목록은 설정에 따라 동적으로 구성됨
# LangGraph 도구 통합: https://langchain-ai.github.io/langgraph/concepts/low_level/#tools
async def get_supervisor_tools(config: RunnableConfig) -> list[BaseTool]:
    """설정에 따라 감독자 도구를 가져옴."""
    configurable = MultiAgentConfiguration.from_runnable_config(config)
    search_tool = get_search_tool(config)
    tools = [tool(Sections), tool(Introduction), tool(Conclusion), tool(FinishReport)]
    if configurable.ask_for_clarification:
        tools.append(tool(Question))
    if search_tool is not None:
        tools.append(search_tool)  # Add search tool, if available
    existing_tool_names = {cast(BaseTool, tool).name for tool in tools}
    mcp_tools = await _load_mcp_tools(config, existing_tool_names)
    tools.extend(mcp_tools)
    return tools


async def get_research_tools(config: RunnableConfig) -> list[BaseTool]:
    """설정에 따라 연구 도구를 가져옴."""
    search_tool = get_search_tool(config)
    tools = [tool(Section), tool(FinishResearch)]
    if search_tool is not None:
        tools.append(search_tool)  # Add search tool, if available
    existing_tool_names = {cast(BaseTool, tool).name for tool in tools}
    mcp_tools = await _load_mcp_tools(config, existing_tool_names)
    tools.extend(mcp_tools)
    return tools


async def supervisor(state: ReportState, config: RunnableConfig):
    """LLM이 도구를 호출할지 여부를 결정.

    LangGraph 노드 문서: https://langchain-ai.github.io/langgraph/concepts/low_level/#nodes
    """
    # 메시지
    messages = state["messages"]

    # 설정 가져오기
    configurable = MultiAgentConfiguration.from_runnable_config(config)
    supervisor_model = get_config_value(configurable.supervisor_model)

    # 모델 초기화
    llm = init_chat_model(model=supervisor_model)

    # 섹션이 완료되었지만 최종 보고서가 아직 없는 경우, 서론과 결론 작성을 시작해야 함
    if state.get("completed_sections") and not state.get("final_report"):
        research_complete_message = {
            "role": "user",
            "content": "연구가 완료되었습니다. 이제 보고서의 서론과 결론을 작성하세요. 다음은 완료된 본문 섹션들입니다: \n\n"
            + "\n\n".join([s.content for s in state["completed_sections"]]),
        }
        messages = messages + [research_complete_message]

    # 설정에 따라 도구 가져오기
    supervisor_tool_list = await get_supervisor_tools(config)

    llm_with_tools = llm.bind_tools(
        supervisor_tool_list,
        parallel_tool_calls=False,
        # 최소 하나의 도구 호출 강제
        tool_choice="any",
    )

    # 시스템 프롬프트 가져오기
    system_prompt = SUPERVISOR_INSTRUCTIONS.format(today=get_today_str())
    if configurable.mcp_prompt:
        system_prompt += f"\n\n{configurable.mcp_prompt}"

    # 호출
    return {
        "messages": [
            await llm_with_tools.ainvoke(
                [{"role": "system", "content": system_prompt}] + messages
            )
        ]
    }


async def supervisor_tools(
    state: ReportState, config: RunnableConfig
) -> Command[Literal["supervisor", "research_team", "__end__"]]:
    """도구 호출을 수행하고 연구 에이전트로 전송.

    LangGraph Command 문서: https://langchain-ai.github.io/langgraph/concepts/low_level/#command
    """
    configurable = MultiAgentConfiguration.from_runnable_config(config)

    result = []
    sections_list = []
    intro_content = None
    conclusion_content = None
    source_str = ""

    # 설정에 따라 도구 가져오기
    supervisor_tool_list = await get_supervisor_tools(config)
    supervisor_tools_by_name = {tool.name: tool for tool in supervisor_tool_list}
    search_tool_names = {
        tool.name
        for tool in supervisor_tool_list
        if tool.metadata is not None and tool.metadata.get("type") == "search"
    }

    # 먼저 모든 도구 호출을 처리하여 각각에 응답하도록 함 (OpenAI에 필요)
    for tool_call in state["messages"][-1].tool_calls:
        # 도구 가져오기
        tool = supervisor_tools_by_name[tool_call["name"]]
        # 도구 호출 수행 - 비동기 도구의 경우 ainvoke 사용
        try:
            observation = await tool.ainvoke(tool_call["args"], config)
        except NotImplementedError:
            observation = tool.invoke(tool_call["args"], config)

        # 메시지에 추가
        result.append(
            {
                "role": "tool",
                "content": observation,
                "name": tool_call["name"],
                "tool_call_id": tool_call["id"],
            }
        )

        # 모든 도구가 호출된 후 처리를 위해 특별한 도구 결과 저장
        if tool_call["name"] == "Question":
            # Question 도구가 호출됨 - 질문을 하기 위해 감독자로 돌아감
            question_obj = cast(Question, observation)
            result.append({"role": "assistant", "content": question_obj.question})
            return Command(goto=END, update={"messages": result})
        elif tool_call["name"] == "Sections":
            sections_list = cast(Sections, observation).sections
        elif tool_call["name"] == "Introduction":
            # 이미 포맷되지 않은 경우 적절한 H1 제목으로 서론 포맷
            observation = cast(Introduction, observation)
            if not observation.content.startswith("# "):
                intro_content = f"# {observation.name}\n\n{observation.content}"
            else:
                intro_content = observation.content
        elif tool_call["name"] == "Conclusion":
            # 이미 포맷되지 않은 경우 적절한 H2 제목으로 결론 포맷
            observation = cast(Conclusion, observation)
            if not observation.content.startswith("## "):
                conclusion_content = f"## {observation.name}\n\n{observation.content}"
            else:
                conclusion_content = observation.content
        elif tool_call["name"] in search_tool_names and configurable.include_source_str:
            source_str += cast(str, observation)

    # 모든 도구 호출 처리 후 다음 작업 결정
    if sections_list:
        # 섹션을 연구 에이전트로 전송
        # LangGraph Send API: https://langchain-ai.github.io/langgraph/concepts/low_level/#send
        return Command(
            goto=[Send("research_team", {"section": s}) for s in sections_list],
            update={"messages": result},
        )
    elif intro_content:
        # 결론을 기다리는 동안 서론 저장
        # LLM이 다음에 결론을 작성하도록 메시지에 추가
        result.append(
            {
                "role": "user",
                "content": "서론이 작성되었습니다. 이제 결론 섹션을 작성하세요.",
            }
        )
        state_update = {
            "final_report": intro_content,
            "messages": result,
        }
    elif conclusion_content:
        # 모든 섹션을 가져와서 적절한 순서로 결합: 서론, 본문 섹션, 결론
        intro = state.get("final_report", "")
        body_sections = "\n\n".join([s.content for s in state["completed_sections"]])

        # 올바른 순서로 최종 보고서 조립
        complete_report = f"{intro}\n\n{body_sections}\n\n{conclusion_content}"

        # 완료를 나타내기 위해 메시지에 추가
        result.append(
            {
                "role": "user",
                "content": "보고서가 서론, 본문 섹션, 결론으로 완성되었습니다.",
            }
        )

        state_update = {
            "final_report": complete_report,
            "messages": result,
        }
    else:
        # 기본 케이스 (검색 도구 등)
        state_update = {"messages": result}

    # 평가를 위한 소스 문자열 포함
    if configurable.include_source_str and source_str:
        state_update["source_str"] = source_str

    return Command(goto="supervisor", update=state_update)


async def supervisor_should_continue(state: ReportState) -> str:
    """LLM이 도구 호출을 했는지 여부에 따라 루프를 계속할지 중단할지 결정.

    LangGraph 조건부 엣지: https://langchain-ai.github.io/langgraph/concepts/low_level/#conditional-edges
    """
    messages = state["messages"]
    last_message = messages[-1]
    # 감독자가 질문을 했거나 완료되어서 종료
    if not last_message.tool_calls or (
        len(last_message.tool_calls) == 1
        and last_message.tool_calls[0]["name"] == "FinishReport"
    ):
        # 그래프 종료
        return END

    # LLM이 도구 호출을 하면 작업 수행
    return "supervisor_tools"


async def research_agent(state: SectionState, config: RunnableConfig):
    """LLM이 도구를 호출할지 여부를 결정."""
    # 설정 가져오기
    configurable = MultiAgentConfiguration.from_runnable_config(config)
    researcher_model = get_config_value(configurable.researcher_model)

    # 모델 초기화
    llm = init_chat_model(model=researcher_model)

    # 설정에 따라 도구 가져오기
    research_tool_list = await get_research_tools(config)
    system_prompt = RESEARCH_INSTRUCTIONS.format(
        section_description=state["section"],
        number_of_queries=configurable.number_of_queries,
        today=get_today_str(),
    )
    if configurable.mcp_prompt:
        system_prompt += f"\n\n{configurable.mcp_prompt}"

    # 최소 하나의 사용자 메시지가 있는지 확인 (Anthropic에 필요)
    messages = state.get("messages", [])
    if not messages:
        messages = [
            {
                "role": "user",
                "content": f"다음 섹션을 연구하고 작성해주세요: {state['section']}",
            }
        ]

    return {
        "messages": [
            # 더 많은 검색을 수행하거나 Section 도구를 호출하여 섉션을 작성하도록 도구 호출 강제
            await llm.bind_tools(
                research_tool_list,
                parallel_tool_calls=False,
                # 최소 하나의 도구 호출 강제
                tool_choice="any",
            ).ainvoke([{"role": "system", "content": system_prompt}] + messages)
        ]
    }


async def research_agent_tools(state: SectionState, config: RunnableConfig):
    """도구 호출을 수행하고 감독자로 라우팅하거나 연구 루프를 계속."""
    configurable = MultiAgentConfiguration.from_runnable_config(config)

    result = []
    completed_section = None
    source_str = ""

    # 설정에 따라 도구 가져오기
    research_tool_list = await get_research_tools(config)
    research_tools_by_name = {tool.name: tool for tool in research_tool_list}
    search_tool_names = {
        tool.name
        for tool in research_tool_list
        if tool.metadata is not None and tool.metadata.get("type") == "search"
    }

    # 먼저 모든 도구 호출 처리 (OpenAI에 필요)
    for tool_call in state["messages"][-1].tool_calls:
        # 도구 가져오기
        tool = research_tools_by_name[tool_call["name"]]
        # 도구 호출 수행 - 비동기 도구의 경우 ainvoke 사용
        try:
            observation = await tool.ainvoke(tool_call["args"], config)
        except NotImplementedError:
            observation = tool.invoke(tool_call["args"], config)

        # 메시지에 추가
        result.append(
            {
                "role": "tool",
                "content": observation,
                "name": tool_call["name"],
                "tool_call_id": tool_call["id"],
            }
        )

        # Section 도구가 호출된 경우 섹션 관찰 저장
        if tool_call["name"] == "Section":
            completed_section = cast(Section, observation)

        # 검색 도구가 호출된 경우 소스 문자열 저장
        if tool_call["name"] in search_tool_names and configurable.include_source_str:
            source_str += cast(str, observation)

    # 모든 도구 처리 후 다음 작업 결정
    state_update = {"messages": result}
    if completed_section:
        # 완료된 섹션을 상태에 작성하고 감독자로 돌아감
        state_update["completed_sections"] = [completed_section]
    if configurable.include_source_str and source_str:
        state_update["source_str"] = source_str

    return state_update


async def research_agent_should_continue(state: SectionState) -> str:
    """LLM이 도구 호출을 했는지 여부에 따라 루프를 계속할지 중단할지 결정."""
    messages = state["messages"]
    last_message = messages[-1]

    if last_message.tool_calls[0]["name"] == "FinishResearch":
        # 연구 완료 - 감독자로 돌아감
        return END
    else:
        return "research_agent_tools"


"""멀티 에이전트 워크플로우 구축

LangGraph 그래프 구축 문서: https://langchain-ai.github.io/langgraph/concepts/low_level/#graph
"""

# 연구 에이전트 워크플로우
research_builder = StateGraph(
    SectionState, output=SectionOutputState, config_schema=MultiAgentConfiguration
)
research_builder.add_node("research_agent", research_agent)
research_builder.add_node("research_agent_tools", research_agent_tools)
research_builder.add_edge(START, "research_agent")
research_builder.add_conditional_edges(
    "research_agent", research_agent_should_continue, ["research_agent_tools", END]
)
research_builder.add_edge("research_agent_tools", "research_agent")

# 감독자 워크플로우
supervisor_builder = StateGraph(
    ReportState,
    input=MessagesState,
    output=ReportStateOutput,
    config_schema=MultiAgentConfiguration,
)
supervisor_builder.add_node("supervisor", supervisor)
supervisor_builder.add_node("supervisor_tools", supervisor_tools)
supervisor_builder.add_node("research_team", research_builder.compile())

# 감독자 에이전트의 흐름
supervisor_builder.add_edge(START, "supervisor")
supervisor_builder.add_conditional_edges(
    "supervisor", supervisor_should_continue, ["supervisor_tools", END]
)
supervisor_builder.add_edge("research_team", "supervisor")

graph = supervisor_builder.compile()
