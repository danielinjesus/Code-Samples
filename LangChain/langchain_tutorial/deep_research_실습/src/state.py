"""상태 정의 모듈.

이 모듈은 LangGraph 워크플로우에서 사용되는 모든 상태 클래스를 정의합니다.
상태는 그래프의 노드 간에 전달되는 데이터를 표현합니다.

참고:
    LangGraph 상태: https://langchain-ai.github.io/langgraph/concepts/low_level/#state
    LangGraph 상태 스키마: https://langchain-ai.github.io/langgraph/concepts/low_level/#schema
    TypedDict: https://docs.python.org/3/library/typing.html#typing.TypedDict
"""

import operator
from typing import Annotated, List, Literal, TypedDict

from pydantic import BaseModel, Field


# 보고서 섹션 모델
class Section(BaseModel):
    """보고서의 각 섹션을 나타내는 데이터 모델."""

    name: str = Field(
        description="이 보고서 섹션의 이름.",
    )
    description: str = Field(
        description="이 섹션에서 다룰 주요 주제와 개념에 대한 간략한 개요.",
    )
    research: bool = Field(description="이 보고서 섹션에 대해 웹 연구를 수행할지 여부.")
    content: str = Field(description="섹션의 내용.")


# 섹션 목록 모델
class Sections(BaseModel):
    """보고서의 여러 섹션을 담는 컨테이너 모델."""

    sections: List[Section] = Field(
        description="보고서의 섹션들.",
    )


# 검색 쿼리 모델
class SearchQuery(BaseModel):
    """웹 검색을 위한 쿼리 모델."""

    search_query: str = Field(None, description="웹 검색을 위한 쿼리.")


# 쿼리 목록 모델
class Queries(BaseModel):
    """여러 검색 쿼리를 담는 컨테이너 모델."""

    queries: List[SearchQuery] = Field(
        description="검색 쿼리 목록.",
    )


# 피드백 모델
class Feedback(BaseModel):
    """섹션 품질 평가와 후속 쿼리를 담는 모델."""

    grade: Literal["pass", "fail"] = Field(
        description="응답이 요구사항을 충족하는지('pass') 수정이 필요한지('fail')를 나타내는 평가 결과."
    )
    follow_up_queries: List[SearchQuery] = Field(
        description="후속 검색 쿼리 목록.",
    )


# 보고서 상태 입력 타입
# LangGraph 그래프의 입력 스키마를 정의합니다.
class ReportStateInput(TypedDict):
    topic: str  # 보고서 주제


# 보고서 상태 출력 타입
# LangGraph 그래프의 출력 스키마를 정의합니다.
class ReportStateOutput(TypedDict):
    final_report: str  # 최종 보고서
    # 평가 목적으로만 사용
    # configurable.include_source_str이 True인 경우에만 포함됨
    source_str: str  # 웹 검색에서 가져온 포맷된 소스 콘텐츠 문자열


# 메인 보고서 상태
# 전체 보고서 생성 프로세스의 상태를 추적합니다.
# 참고: https://langchain-ai.github.io/langgraph/concepts/low_level/#state-annotations
class ReportState(TypedDict):
    topic: str  # 보고서 주제
    feedback_on_report_plan: Annotated[
        list[str], operator.add
    ]  # 보고서 계획에 대한 피드백 목록 (누적)
    sections: list[Section]  # 보고서 섹션 목록
    completed_sections: Annotated[
        list, operator.add
    ]  # Send API를 위한 키 (병렬 작업 결과 집계)
    report_sections_from_research: (
        str  # 최종 섹션 작성을 위해 연구에서 완성된 섹션들의 문자열
    )
    final_report: str  # 최종 보고서
    # 평가 목적으로만 사용
    # configurable.include_source_str이 True인 경우에만 포함됨
    source_str: Annotated[
        str, operator.add
    ]  # 웹 검색에서 가져온 포맷된 소스 콘텐츠 문자열 (누적)


# 섹션 상태
# 각 섉션 작성을 위한 서브그래프의 상태를 정의합니다.
# 참고: https://langchain-ai.github.io/langgraph/concepts/low_level/#subgraphs
class SectionState(TypedDict):
    topic: str  # 보고서 주제
    section: Section  # 현재 작업 중인 보고서 섉션
    search_iterations: int  # 수행된 검색 반복 횟수
    search_queries: list[SearchQuery]  # 검색 쿼리 목록
    source_str: str  # 웹 검색에서 가져온 포맷된 소스 콘텐츠 문자열
    report_sections_from_research: (
        str  # 최종 섉션 작성을 위해 연구에서 완성된 섉션들의 문자열
    )
    completed_sections: list[Section]  # Send API를 위해 외부 상태에 복사하는 최종 키


# 섉션 출력 상태
# 서브그래프에서 메인 그래프로 전달되는 출력 상태를 정의합니다.
class SectionOutputState(TypedDict):
    completed_sections: list[Section]  # Send API를 위해 외부 상태에 복사하는 최종 키
    # 평가 목적으로만 사용
    # configurable.include_source_str이 True인 경우에만 포함됨
    source_str: str  # 웹 검색에서 가져온 포맷된 소스 콘텐츠 문자열
