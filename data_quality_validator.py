"""Reusable data-quality validation utilities for analytics and ETL testing."""

from __future__ import annotations

import pandas as pd


class DataQualityValidator:
    """Run common validation checks against a pandas DataFrame."""

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

    def missing_values(self) -> pd.DataFrame:
        counts = self.df.isna().sum()
        result = pd.DataFrame({
            "column": counts.index,
            "missing_count": counts.values,
        })
        result["missing_percent"] = (
            result["missing_count"] / max(len(self.df), 1) * 100
        ).round(2)
        return result

    def duplicate_rows(self) -> pd.DataFrame:
        return self.df[self.df.duplicated(keep=False)].copy()

    def validate_unique_key(self, column: str) -> dict:
        if column not in self.df.columns:
            raise KeyError(f"Column '{column}' not found")
        return {
            "column": column,
            "null_keys": int(self.df[column].isna().sum()),
            "duplicate_keys": int(self.df[column].duplicated().sum()),
            "is_valid": bool(
                self.df[column].notna().all() and self.df[column].is_unique
            ),
        }

    def validate_required_columns(self, required_columns: list[str]) -> dict:
        missing = [c for c in required_columns if c not in self.df.columns]
        return {"missing_columns": missing, "is_valid": not missing}

    def validate_numeric_range(self, column: str, minimum=None, maximum=None) -> pd.DataFrame:
        if column not in self.df.columns:
            raise KeyError(f"Column '{column}' not found")
        values = pd.to_numeric(self.df[column], errors="coerce")
        invalid = values.isna()
        if minimum is not None:
            invalid |= values < minimum
        if maximum is not None:
            invalid |= values > maximum
        return self.df[invalid].copy()

    def summary(self) -> dict:
        return {
            "rows": int(len(self.df)),
            "columns": int(len(self.df.columns)),
            "missing_cells": int(self.df.isna().sum().sum()),
            "duplicate_rows": int(self.df.duplicated().sum()),
        }


if __name__ == "__main__":
    sample = pd.DataFrame(
        {
            "record_id": [101, 102, 102, 104],
            "status": ["PASS", "PASS", None, "FAIL"],
            "amount": [125.0, 200.0, 200.0, -5.0],
        }
    )

    validator = DataQualityValidator(sample)
    print("Summary:", validator.summary())
    print("\nMissing values:\n", validator.missing_values())
    print("\nKey validation:", validator.validate_unique_key("record_id"))
    print("\nInvalid amounts:\n", validator.validate_numeric_range("amount", minimum=0))
