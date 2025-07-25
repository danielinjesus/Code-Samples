import os  # noqa: D100
from dataclasses import dataclass, fields
from typing import Any, Dict, Literal, Optional

from langchain_core.runnables import RunnableConfig

from ..configuration import DEFAULT_REPORT_STRUCTURE, SearchAPI


@dataclass(kw_only=True)
class WorkflowConfiguration:
    """Configuration for the workflow/graph-based implementation (graph.py)."""

    # Common configuration
    report_structure: str = DEFAULT_REPORT_STRUCTURE
    search_api: SearchAPI = SearchAPI.TAVILY
    search_api_config: Optional[Dict[str, Any]] = None
    clarify_with_user: bool = False
    sections_user_approval: bool = False
    process_search_results: Literal["summarize", "split_and_rerank"] | None = (
        "summarize"
    )
    summarization_model_provider: str = "openai"
    summarization_model: str = "gpt-4.1-mini"
    max_structured_output_retries: int = 3
    include_source_str: bool = False

    # Workflow-specific configuration
    number_of_queries: int = 2  # Number of search queries to generate per iteration
    max_search_depth: int = 2  # Maximum number of reflection + search iterations
    planner_provider: str = "openai"
    planner_model: str = "gpt-4.1"
    planner_model_kwargs: Optional[Dict[str, Any]] = None
    writer_provider: str = "openai"
    writer_model: str = "gpt-4.1"
    writer_model_kwargs: Optional[Dict[str, Any]] = None

    @classmethod
    def from_runnable_config(
        cls, config: Optional[RunnableConfig] = None
    ) -> "WorkflowConfiguration":
        """Create a WorkflowConfiguration instance from a RunnableConfig."""
        configurable = (
            config["configurable"] if config and "configurable" in config else {}
        )
        values: dict[str, Any] = {
            f.name: os.environ.get(f.name.upper(), configurable.get(f.name))
            for f in fields(cls)
            if f.init
        }
        return cls(**{k: v for k, v in values.items() if v})
