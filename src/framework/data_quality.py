from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Mapping, Sequence

Row = Mapping[str, Any]
Check = Callable[[Sequence[Row]], "CheckResult"]


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    observed: int
    failed: int = 0
    message: str = ""


@dataclass
class DataQualityReport:
    results: list[CheckResult] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(result.passed for result in self.results)

    def add(self, result: CheckResult) -> None:
        self.results.append(result)

    def raise_for_failure(self) -> None:
        failures = [result.name for result in self.results if not result.passed]
        if failures:
            raise ValueError(f"data quality checks failed: {', '.join(failures)}")


def _rows(data: Iterable[Row] | Any) -> list[Row]:
    if hasattr(data, "toLocalIterator"):
        return [row.asDict(recursive=True) for row in data.toLocalIterator()]
    return list(data)


def not_null(column: str) -> Check:
    def check(data: Sequence[Row]) -> CheckResult:
        failed = sum(row.get(column) is None for row in data)
        return CheckResult(f"not_null:{column}", failed == 0, len(data), failed)
    return check


def unique(column: str) -> Check:
    def check(data: Sequence[Row]) -> CheckResult:
        values = [row.get(column) for row in data]
        failed = len(values) - len(set(values))
        return CheckResult(f"unique:{column}", failed == 0, len(data), failed)
    return check


def accepted_values(column: str, allowed: set[Any]) -> Check:
    def check(data: Sequence[Row]) -> CheckResult:
        failed = sum(row.get(column) not in allowed for row in data)
        return CheckResult(f"accepted_values:{column}", failed == 0, len(data), failed)
    return check


def evaluate(data: Iterable[Row] | Any, checks: Iterable[Check]) -> DataQualityReport:
    rows = _rows(data)
    report = DataQualityReport()
    for check in checks:
        report.add(check(rows))
    return report
