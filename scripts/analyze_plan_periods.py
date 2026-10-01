"""Audit listed fees within reported plan periods; no revenue normalization."""

import argparse
import json
import sqlite3
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
PERIOD_LABELS = {
    "MONTHLY": "monthly", "ANNUALLY": "annual", "HALF YEARLY": "half_year",
    "QUARTERLY": "quarter", "13MONTHLY": "13_month", "13 MONTHLY": "13_month",
    "97DAYS": "97_day", "199DAYS": "199_day", "UNKNOWN": "unspecified",
}


def classify_period(values: pd.Series) -> pd.Series:
    labels = values.astype("string").str.strip().str.upper().fillna("UNKNOWN")
    # Preserve unexpected labels as unresolved; never default them to monthly.
    return labels.map(PERIOD_LABELS).fillna("unrecognized")


def audit_periods(root: Path = ROOT) -> dict:
    model = root / "data/powerbi_star_schema"
    fact = pd.read_csv(model / "fact_customer_service.csv")
    plans = pd.read_csv(model / "dim_plan.csv")
    states = pd.read_csv(model / "dim_service_state.csv")
    rows = fact.merge(plans[["plan_key", "plan_period"]], on="plan_key", validate="many_to_one")
    rows = rows.merge(states[["service_state_key", "service_status"]], on="service_state_key", validate="many_to_one")
    if len(rows) != len(fact):
        raise ValueError("Plan/state join changed service grain")
    rows["period_group"] = classify_period(rows.plan_period)
    rows["active_partial_listed_amount"] = rows.monthly_fee.where(rows.service_status.isin(["active", "partial_active"]), 0)
    grouped = rows.groupby("period_group").agg(
        service_rows=("service_snapshot_key", "size"),
        listed_amount_units=("monthly_fee", "sum"),
        active_partial_listed_amount_units=("active_partial_listed_amount", "sum"),
    ).reset_index()
    # SQL verifies period counts and sums without changing the amount's cadence.
    with sqlite3.connect(":memory:") as db:
        rows.to_sql("services", db, index=False)
        sql_rows = db.execute("SELECT period_group, COUNT(*), SUM(monthly_fee), SUM(active_partial_listed_amount) FROM services GROUP BY period_group ORDER BY period_group").fetchall()
    python_rows = list(grouped.itertuples(index=False, name=None))
    if sql_rows != python_rows:
        raise ValueError("Python/SQLite plan-period disagreement")
    return {
        "scope": "committed service snapshot; author confirms amounts relate to listed plan periods",
        "service_records": int(len(rows)),
        "source_period_label_counts": {str(k): int(v) for k, v in rows.plan_period.value_counts(dropna=False).sort_index().items()},
        "by_reported_period": [
            {"period_group": r.period_group, "service_rows": int(r.service_rows),
             "listed_amount_units": float(r.listed_amount_units),
             "active_partial_listed_amount_units": float(r.active_partial_listed_amount_units)}
            for r in grouped.itertuples()
        ],
        "fee_semantics": "listed plan amounts by source period, not recognized revenue or verified MRR",
        "currency": "not disclosed",
        "period_normalization": "text alias normalization only; no annual/day amounts divided into monthly revenue",
        "independent_sql_reconciliation": "passed for per-period counts and listed amounts",
        "power_bi_execution": "not executed",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    serialized = json.dumps(audit_periods(), indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
