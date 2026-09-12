from silver.process_claim import process_silver


def run_silver(records: list[dict]) -> list[dict]:
    """Run silver cleansing and fail the task when quality checks do not pass."""

    cleaned, report = process_silver(records, required=("id",), unique_key="id")
    print({"quality_results": [result.__dict__ for result in report.results]})
    return cleaned


if __name__ == "__main__":
    print(run_silver([{"id": 1, "status": "ready"}]))
