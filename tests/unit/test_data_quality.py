from framework.data_quality import evaluate, not_null


def test_required_value_quality_rule() -> None:
    assert evaluate([{"id": 1}], [not_null("id")]).passed
