"""Response models for AndesContext backend services."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


@dataclass(frozen=True)
class RememberResult:
    """Result of a remember() operation."""

    dataset_name: str
    items_sent: int
    raw_result: Any = None


@dataclass(frozen=True)
class RecallResult:
    """A single result from a recall() operation."""

    kind: str
    search_type: str
    text: str
    score: float
    dataset_name: str
    raw: Any = None


@dataclass(frozen=True)
class RecallResponse:
    """Aggregated result of a recall() operation."""

    query: str
    dataset: str
    results: list[RecallResult] = field(default_factory=list)

    @property
    def count(self) -> int:
        return len(self.results)


@dataclass
class IndexingProgress:
    """Progress information for a repository indexing operation."""

    total_files: int = 0
    processed_files: int = 0
    skipped_files: int = 0
    failed_files: int = 0
    current_batch: int = 0
    total_batches: int = 0
    failed_paths: list[str] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return self.current_batch >= self.total_batches and self.total_batches > 0

    def summary(self) -> str:
        return (
            f"Indexed {self.processed_files}/{self.total_files} files "
            f"({self.skipped_files} skipped, {self.failed_files} failed) "
            f"in {self.total_batches} batches"
        )


class SectionType(str, Enum):
    """Types of sections in a Context Package."""

    TASK = "task"
    OVERVIEW = "overview"
    FILES = "files"
    KNOWLEDGE = "knowledge"
    ARCHITECTURE = "architecture"
    APIS = "apis"
    CONVENTIONS = "conventions"
    DECISIONS = "decisions"
    REFERENCES = "references"


@dataclass(frozen=True)
class PackageSection:
    """A single section in a Context Package."""

    section_type: SectionType
    heading: str
    content: str


@dataclass(frozen=True)
class ContextPackage:
    """A structured Markdown Context Package for AI coding assistants."""

    task: str
    markdown: str
    sections: list[PackageSection] = field(default_factory=list)
    source_count: int = 0
    dataset: str = ""

    @property
    def section_count(self) -> int:
        return len(self.sections)

    @property
    def token_estimate(self) -> int:
        """Rough word-based estimate (1 token ~ 4 chars)."""
        return len(self.markdown) // 4
