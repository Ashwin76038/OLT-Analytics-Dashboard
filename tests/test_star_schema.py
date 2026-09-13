"""Integrity and privacy checks for the generated Power BI model."""

import re
import unittest
from pathlib import Path

import pandas as pd


MODEL_DIR = Path(__file__).resolve().parents[1] / "data" / "powerbi_star_schema"


class StarSchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fact = pd.read_csv(MODEL_DIR / "fact_customer_service.csv")
        cls.dimensions = {
            "customer_key": pd.read_csv(MODEL_DIR / "dim_customer.csv"),
            "olt_key": pd.read_csv(MODEL_DIR / "dim_olt.csv"),
            "plan_key": pd.read_csv(MODEL_DIR / "dim_plan.csv"),
            "service_state_key": pd.read_csv(MODEL_DIR / "dim_service_state.csv"),
            "date_key": pd.read_csv(MODEL_DIR / "dim_date.csv"),
        }

    def test_primary_keys_are_unique_and_not_null(self) -> None:
        self.assertFalse(self.fact["service_snapshot_key"].isna().any())
        self.assertFalse(self.fact["service_snapshot_key"].duplicated().any())
        for key, dimension in self.dimensions.items():
            self.assertFalse(dimension[key].isna().any(), key)
            self.assertFalse(dimension[key].duplicated().any(), key)

    def test_foreign_keys_resolve(self) -> None:
        for key in ["customer_key", "olt_key", "plan_key", "service_state_key"]:
            self.assertTrue(self.fact[key].isin(self.dimensions[key][key]).all(), key)
        valid_dates = set(self.dimensions["date_key"]["date_key"])
        for key in ["activation_date_key", "reported_activation_date_key", "snapshot_date_key"]:
            values = self.fact[key].dropna().astype("int64")
            self.assertTrue(values.isin(valid_dates).all(), key)

    def test_future_dates_are_quarantined(self) -> None:
        future = self.fact["dq_future_activation_flag"].eq(1)
        self.assertEqual(int(future.sum()), 810)
        self.assertTrue(self.fact.loc[future, "activation_date_key"].isna().all())
        self.assertTrue(self.fact.loc[future, "valid_tenure_days"].isna().all())
        self.assertFalse((self.fact["valid_tenure_days"].dropna() < 0).any())

    def test_customer_connection_count_matches_fact_grain(self) -> None:
        expected = self.fact.groupby("customer_key").size().rename("expected")
        customer = self.dimensions["customer_key"].set_index("customer_key")
        comparison = customer.join(expected, how="left")
        self.assertTrue(comparison["connection_count"].eq(comparison["expected"]).all())

    def test_no_direct_identifier_columns_or_values(self) -> None:
        forbidden_columns = {
            "customer",
            "customer_clean",
            "mobile",
            "email",
            "address",
            "service_number",
            "assign_to",
            "olt ip",
            "olt_ip",
        }
        patterns = [
            re.compile(r"\b[^\s@]+@[^\s@]+\.[^\s@]+\b"),
            re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        ]
        for path in MODEL_DIR.glob("*.csv"):
            frame = pd.read_csv(path, dtype="string")
            self.assertFalse(forbidden_columns.intersection(map(str.lower, frame.columns)), path.name)
            for column in frame.columns:
                values = frame[column].dropna()
                for pattern in patterns:
                    self.assertFalse(values.str.contains(pattern, regex=True).any(), f"{path.name}:{column}")


if __name__ == "__main__":
    unittest.main()
