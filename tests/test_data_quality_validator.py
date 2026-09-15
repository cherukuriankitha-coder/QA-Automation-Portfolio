import pandas as pd

from data_quality_validator import DataQualityValidator


def test_valid_unique_key():
    df = pd.DataFrame({"id": [1, 2, 3]})
    result = DataQualityValidator(df).validate_unique_key("id")
    assert result["is_valid"] is True
    assert result["duplicate_keys"] == 0


def test_duplicate_key_is_detected():
    df = pd.DataFrame({"id": [1, 2, 2]})
    result = DataQualityValidator(df).validate_unique_key("id")
    assert result["is_valid"] is False
    assert result["duplicate_keys"] == 1


def test_missing_required_column():
    df = pd.DataFrame({"id": [1], "name": ["A"]})
    result = DataQualityValidator(df).validate_required_columns(["id", "status"])
    assert result["is_valid"] is False
    assert result["missing_columns"] == ["status"]


def test_numeric_range_validation():
    df = pd.DataFrame({"amount": [10, 20, -1, 101]})
    invalid = DataQualityValidator(df).validate_numeric_range(
        "amount", minimum=0, maximum=100
    )
    assert invalid["amount"].tolist() == [-1, 101]
