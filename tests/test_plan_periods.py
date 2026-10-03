import json
import sys
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from analyze_plan_periods import audit_periods, classify_period


class PlanPeriodTests(unittest.TestCase):
    def test_unresolved_cadence_is_never_assumed_monthly(self):
        periods = classify_period(pd.Series([None, "unknown", "unverified renewal", "13MONTHLY", "13 MONTHLY", "ANNUALLY"]))
        self.assertEqual(periods.tolist(), ["unspecified", "unspecified", "unrecognized", "13_month", "13_month", "annual"])

    def test_period_receipt_reconciles_counts_and_fee_denominators(self):
        result = audit_periods()
        saved = json.loads((ROOT / "docs/plan_period_receipt.json").read_text())
        self.assertEqual(result, saved)
        groups = {r["period_group"]: r for r in result["by_reported_period"]}
        self.assertEqual(groups["monthly"]["service_rows"], 1188)
        self.assertEqual(groups["annual"]["service_rows"], 6)
        self.assertEqual(groups["13_month"]["service_rows"], 14)
        self.assertEqual(groups["unspecified"]["service_rows"], 58)
        self.assertEqual(sum(r["service_rows"] for r in groups.values()), 1280)
        self.assertEqual(sum(r["listed_amount_units"] for r in groups.values()), 3328525)
        self.assertEqual(sum(r["active_partial_listed_amount_units"] for r in groups.values()), 3282809)


if __name__ == "__main__":
    unittest.main()
