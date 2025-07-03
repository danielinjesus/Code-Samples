#!/usr/bin/env python
import argparse
import os
import subprocess
import sys

from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

console = Console()

"""
Open Deep Research의 Rich 콘솔 출력을 포함한 단순화된 테스트 러너.

사용 예시:
python tests/run_test.py --all  # 모든 에이전트를 Rich 출력과 함께 실행
python tests/run_test.py --agent multi_agent --supervisor-model "anthropic:claude-3-7-sonnet-latest"
python tests/run_test.py --agent graph --search-api tavily

참고:
    pytest 사용법: https://docs.pytest.org/en/stable/how-to/usage.html
    Rich 라이브러리: https://rich.readthedocs.io/en/stable/
"""


def main():
    # 커맨드라인 인자 파싱
    parser = argparse.ArgumentParser(
        description="Open Deep Research의 테스트를 Rich 콘솔 출력과 함께 실행"
    )
    parser.add_argument(
        "--rich-output",
        action="store_true",
        default=True,
        help="터미널에 Rich 출력 표시 (기본값: True)",
    )
    parser.add_argument("--experiment-name", help="LangSmith 실험 이름")
    parser.add_argument(
        "--agent",
        choices=["multi_agent", "graph"],
        help="특정 에이전트에 대한 테스트 실행",
    )
    parser.add_argument(
        "--all", action="store_true", help="모든 에이전트에 대한 테스트 실행"
    )

    # 모델 설정 옵션
    parser.add_argument(
        "--supervisor-model",
        help="스퍼바이저 에이전트용 모델 (예: 'anthropic:claude-3-7-sonnet-latest')",
    )
    parser.add_argument(
        "--researcher-model",
        help="연구원 에이전트용 모델 (예: 'anthropic:claude-3-5-sonnet-latest')",
    )
    parser.add_argument(
        "--planner-provider", help="플래너 모델 프로바이더 (예: 'anthropic')"
    )
    parser.add_argument(
        "--planner-model",
        help="그래프 기반 에이전트의 플래너 모델 (예: 'claude-3-7-sonnet-latest')",
    )
    parser.add_argument(
        "--writer-provider", help="작성자 모델 프로바이더 (예: 'anthropic')"
    )
    parser.add_argument(
        "--writer-model",
        help="그래프 기반 에이전트의 작성자 모델 (예: 'claude-3-5-sonnet-latest')",
    )
    parser.add_argument(
        "--eval-model",
        help="보고서 품질 평가용 모델 (기본값: openai:claude-3-7-sonnet-latest)",
    )
    parser.add_argument("--max-search-depth", help="그래프 에이전트의 최대 검색 깊이")

    # 검색 API 설정
    parser.add_argument(
        "--search-api",
        choices=["tavily", "duckduckgo"],
        help="콘텐츠 검색에 사용할 검색 API",
    )

    args = parser.parse_args()

    # 사용 가능한 에이전트와 테스트 설정 정의
    agents = {
        "multi_agent": {
            "test": "tests/test_report_quality.py::test_response_criteria_evaluation",
            "topic": "Model Context Protocol",
            "description": "전체 MCP 보고서로 multi_agent 테스트",
            "needs_research_agent_param": True,
        },
        "graph": {
            "test": "tests/test_report_quality.py::test_response_criteria_evaluation",
            "topic": "Model Context Protocol",
            "description": "전체 MCP 보고서로 graph 에이전트 테스트",
            "needs_research_agent_param": True,
        },
    }

    # 테스트할 에이전트 결정
    if args.agent:
        if args.agent in agents:
            agents_to_test = [args.agent]
        else:
            console.print(f"[red]오류: 알 수 없는 에이전트 '{args.agent}'[/red]")
            console.print(f"사용 가능한 에이전트: {', '.join(agents.keys())}")
            return 1
    elif args.all:
        agents_to_test = list(agents.keys())
    else:
        # 기본값으로 모든 에이전트 테스트
        agents_to_test = list(agents.keys())

    # 각 에이전트에 대한 테스트 실행
    for agent in agents_to_test:
        console.print(
            Rule(f"[bold blue]{agent.upper()} 에이전트 테스트 중[/bold blue]")
        )

        agent_config = agents[agent]

        # 이 에이전트를 위한 LangSmith 환경 설정
        project_name = "ODR: Pytest"
        os.environ["LANGSMITH_PROJECT"] = project_name
        os.environ["LANGSMITH_TEST_SUITE"] = project_name

        # 추적이 활성화되었는지 확인
        os.environ["LANGCHAIN_TRACING_V2"] = "true"

        # 실험 이름 설정
        experiment_name = (
            args.experiment_name if args.experiment_name else f"{agent_config['topic']}"
        )
        os.environ["LANGSMITH_EXPERIMENT"] = experiment_name

        console.print(f"[dim]프로젝트: {project_name}[/dim]")
        console.print(f"[dim]테스트: {agent_config['description']}[/dim]")
        console.print(f"[dim]실험: {experiment_name}[/dim]")

        # 테스트 실행
        console.print(f"\n[green]{agent} 에이전트 테스트 실행 중...[/green]")
        run_test(agent, agent_config, args)

    console.print(Rule("[bold green]모든 테스트 완료[/bold green]"))


def run_test(agent, agent_config, args):
    """Rich 콘솔 포맷팅으로 pytest 실행."""
    # 기본 pytest 옵션 (-s를 추가하여 출력 캡처 비활성화)
    base_pytest_options = ["-v", "-s", "--disable-warnings", "--langsmith-output"]

    # 커맨드 구성
    cmd = ["python", "-m", "pytest", agent_config["test"]] + base_pytest_options

    # 필요한 경우 연구 에이전트 매개변수 추가
    if agent_config["needs_research_agent_param"]:
        cmd.append(f"--research-agent={agent}")

    # 제공된 경우 모델 설정 추가
    add_model_configs(cmd, args)

    # 명령어를 보기 좋은 패널로 표시
    console.print(
        Panel(
            f"[bold]실행 명령어:[/bold]\n[dim]{' '.join(cmd)}[/dim]",
            style="blue",
            title="pytest 실행",
        )
    )

    # 실시간 출력으로 명령어 실행 (캡처 없음)
    console.print("\n[yellow]테스트 실행 시작...[/yellow]\n")
    result = subprocess.run(cmd)

    # Rich 포맷팅으로 결과 표시
    console.print("\n[yellow]테스트 실행 완료.[/yellow]")
    if result.returncode == 0:
        console.print(
            Panel(
                f"[bold green]✅ {agent} 테스트 통과[/bold green]",
                style="green",
                title="테스트 결과",
            )
        )
    else:
        console.print(
            Panel(
                f"[bold red]❌ {agent} 테스트 실패[/bold red]\n[red]반환 코드: {result.returncode}[/red]",
                style="red",
                title="테스트 결과",
            )
        )


def add_model_configs(cmd, args):
    """모델 설정 인자를 명령어에 추가."""
    if args.supervisor_model:
        cmd.append(f"--supervisor-model={args.supervisor_model}")
    if args.researcher_model:
        cmd.append(f"--researcher-model={args.researcher_model}")
    if args.planner_provider:
        cmd.append(f"--planner-provider={args.planner_provider}")
    if args.planner_model:
        cmd.append(f"--planner-model={args.planner_model}")
    if args.writer_provider:
        cmd.append(f"--writer-provider={args.writer_provider}")
    if args.writer_model:
        cmd.append(f"--writer-model={args.writer_model}")
    if args.eval_model:
        cmd.append(f"--eval-model={args.eval_model}")
    if args.search_api:
        cmd.append(f"--search-api={args.search_api}")
    if args.max_search_depth:
        cmd.append(f"--max-search-depth={args.max_search_depth}")


if __name__ == "__main__":
    sys.exit(main() or 0)
