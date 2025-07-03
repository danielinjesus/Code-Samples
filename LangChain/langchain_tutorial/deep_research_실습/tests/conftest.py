"""
open_deep_research 테스트를 위한 Pytest 설정.

이 파일은 pytest의 기본 설정과 커스텀 옵션을 정의합니다.
테스트 실행 시 사용할 수 있는 다양한 커맨드라인 옵션을 제공합니다.

참고:
    pytest 설정: https://docs.pytest.org/en/stable/reference/customize.html
    pytest 플러그인: https://docs.pytest.org/en/stable/how-to/plugins.html
"""


def pytest_addoption(parser):
    """pytest에 커맨드라인 옵션 추가.

    이 함수는 테스트 실행 시 사용할 수 있는 커스텀 옵션들을 정의합니다.
    각 옵션은 연구 에이전트의 동작을 제어하는 데 사용됩니다.
    """
    parser.addoption(
        "--research-agent", action="store", help="에이전트 타입: multi_agent 또는 graph"
    )
    parser.addoption("--search-api", action="store", help="사용할 검색 API")
    parser.addoption("--eval-model", action="store", help="평가용 모델")
    parser.addoption(
        "--supervisor-model", action="store", help="슈퍼바이저 에이전트용 모델"
    )
    parser.addoption(
        "--researcher-model", action="store", help="연구원 에이전트용 모델"
    )
    parser.addoption(
        "--planner-provider", action="store", help="플래너 모델 프로바이더"
    )
    parser.addoption("--planner-model", action="store", help="계획 수립용 모델")
    parser.addoption("--writer-provider", action="store", help="작성자 모델 프로바이더")
    parser.addoption("--writer-model", action="store", help="작성용 모델")
    parser.addoption("--max-search-depth", action="store", help="최대 검색 깊이")
