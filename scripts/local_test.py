import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from framework.cdc import ChangeRecord, apply_changes


def main() -> None:
    result = apply_changes([], [ChangeRecord("1", "insert", {"value": "ok"}, 1)])
    assert result == [{"id": "1", "value": "ok"}]
    print("local platform smoke test passed")


if __name__ == "__main__":
    main()
