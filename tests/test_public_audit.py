"""Regression checks for the interview-facing snapshot claims."""

import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from audit_public import audit  # noqa: E402


class PublicAuditTests(unittest.TestCase):
    def test_committed_receipt_recomputes_and_keeps_grains_distinct(self):
        current = audit()
        receipt = json.loads((ROOT / "docs/public_audit.json").read_text(encoding="utf-8"))
        self.assertEqual(current, receipt)
        self.assertEqual(current["service_records"], 1280)
        self.assertEqual(current["customer_keys"], 1193)
        self.assertEqual(current["inactive_only_customer_keys"], 22)
        self.assertEqual(current["future_activation_records"], 0)
        self.assertEqual(current["legacy_prepared_future_activation_records"], 810)
        self.assertEqual(current["withheld_activation_records"], 1280)
        self.assertEqual(current["valid_tenure_records"], 0)
        self.assertAlmostEqual(current["active_service_share"], 1210 / 1280)
        self.assertEqual(current["independent_sql_reconciliation"].split()[0], "passed")

    def test_audit_rejects_join_fanout(self):
        real_read_csv = pd.read_csv

        def duplicate_state(path, *args, **kwargs):
            frame = real_read_csv(path, *args, **kwargs)
            if Path(path).name == "dim_service_state.csv":
                return pd.concat([frame, frame.iloc[[0]]], ignore_index=True)
            return frame

        with patch("audit_public.pd.read_csv", side_effect=duplicate_state):
            with self.assertRaisesRegex(ValueError, "Invalid dimension key"):
                audit()

    def test_future_dates_stay_out_of_tenure_and_review_is_not_just_future(self):
        fact = pd.read_csv(ROOT / "data/powerbi_star_schema/fact_customer_service.csv")
        future = fact.dq_future_activation_flag.eq(1)
        self.assertTrue(fact.loc[future, ["activation_date_key", "valid_tenure_days"]].isna().all().all())
        self.assertGreater(int(fact.data_quality_flag.eq("review").sum()), int(future.sum()))
        self.assertEqual(int(fact.dq_unknown_plan_period_flag.sum()), 58)


if __name__ == "__main__":
    unittest.main()
