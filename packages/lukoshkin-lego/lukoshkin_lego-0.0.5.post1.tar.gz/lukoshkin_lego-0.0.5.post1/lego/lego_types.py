"""Types common to all lego submodules."""

from typing import Any, DefaultDict, NewType, Protocol, TypeAlias, TypeVar

T = TypeVar("T")
# -- mypy contradicts with pyright here?
OneOrMany = T | list[T]  # type: ignore[misc]
MilvusParamConfig: TypeAlias = dict[str, str | dict[str, int]]

JSONDict: TypeAlias = dict[str, Any]  # type: ignore[misc]
FlatParamConfig: TypeAlias = dict[str, str | int | float | bool]

UseProfiler = NewType("UseProfiler", bool)
ProfilerSessions = NewType(
    "ProfilerSessions", DefaultDict[str, dict[str, float]]
)

Messages: TypeAlias = list[dict[str, str]]


class LegoLLMRouter(Protocol):
    """Protocol for LLM routers available in Lego."""

    def __call__(
        self,
        messages: list[dict[str, str]],
        **kwargs: Any,  # type: ignore[misc]
    ) -> Any:
        """Make a ChatCompletion request."""
