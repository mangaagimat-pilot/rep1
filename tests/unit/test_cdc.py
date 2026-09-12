from framework.cdc import ChangeRecord, apply_changes


def test_insert_change() -> None:
    assert apply_changes([], [ChangeRecord("1", "insert", {"x": 1}, 1)]) == [{"id": "1", "x": 1}]
