"""Independent, privacy-safe audit of the committed service snapshot.

This script never reads the private source extract. It reconciles public CSV
metrics in pandas and SQLite and emits only aggregate results.
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "data" / "powerbi_star_schema"


def audit(model_dir: Path = MODEL) -> dict:
    tables = {path.stem: pd.read_csv(path) for path in model_dir.glob("*.csv")}
    required = {
        "fact_customer_service", "dim_customer", "dim_olt", "dim_plan",
        "dim_service_state", "dim_date",
    }
    if set(tables) != required:
        raise ValueError(f"Expected six model tables; missing={sorted(required-set(tables))}, extra={sorted(set(tables)-required)}")

    fact = tables["fact_customer_service"]
    state = tables["dim_service_state"]
    plan = tables["dim_plan"]
    if fact.service_snapshot_key.isna().any() or fact.service_snapshot_key.duplicated().any():
        raise ValueError("Service snapshot keys must be unique and non-null")
    if fact.snapshot_date_key.nunique() != 1 or fact.snapshot_date_key.isna().any():
        raise ValueError("This audit expects exactly one non-null snapshot date")
    if not fact.data_quality_flag.isin(["valid", "review"]).all():
        raise ValueError("Unexpected data-quality flag")
    for name, key in [
        ("dim_customer", "customer_key"), ("dim_olt", "olt_key"),
        ("dim_plan", "plan_key"), ("dim_service_state", "service_state_key"),
    ]:
        dim = tables[name]
        if dim[key].isna().any() or dim[key].duplicated().any():
            raise ValueError(f"Invalid dimension key: {name}.{key}")
        if not fact[key].isin(dim[key]).all():
            raise ValueError(f"Orphan fact key: {key}")

    date_keys = set(tables["dim_date"].date_key)
    for field in ("activation_date_key", "reported_activation_date_key", "snapshot_date_key"):
        if not fact[field].dropna().astype("int64").isin(date_keys).all():
            raise ValueError(f"Unresolved date key: {field}")
    future = fact.dq_future_activation_flag.eq(1)
    if not fact.loc[future, "activation_date_key"].isna().all():
        raise ValueError("Future activations must not enter validated tenure")
    if not fact.loc[future, "valid_tenure_days"].isna().all():
        raise ValueError("Future activations must not have tenure")

    joined = fact.merge(
        state[["service_state_key", "service_status", "is_revenue_generating", "olt_performance_weight"]],
        on="service_state_key", validate="many_to_one"
    )
    if len(joined) != len(fact):
        raise ValueError("Service-state join changed the fact grain")
    customer_status = joined.groupby("customer_key").agg(
        revenue_service=("is_revenue_generating", "max"),
        inactive_service=("inactive_service_flag", "max"),
    )
    state_counts = joined.service_status.value_counts().sort_index().to_dict()
    review = fact.data_quality_flag.eq("review")
    receipt = {
        "scope": "committed customer-source sample; author identifies a confidential government export; public activation dates require reconciliation",
        "snapshot_date_key": int(fact.snapshot_date_key.iloc[0]),
        "service_records": int(len(fact)),
        "customer_keys": int(fact.customer_key.nunique()),
        "olt_groups": int(fact.olt_key.nunique()),
        "service_status_records": {k: int(v) for k, v in state_counts.items()},
        "active_service_share": float(joined.service_status.eq("active").mean()),
        "active_or_partial_customer_keys": int(customer_status.revenue_service.eq(1).sum()),
        "inactive_only_customer_keys": int((customer_status.revenue_service.eq(0) & customer_status.inactive_service.eq(1)).sum()),
        "listed_fee_exposure_unverified_units": float(joined.loc[joined.is_revenue_generating.eq(1), "monthly_fee"].sum()),
        "partial_active_listed_fees_unverified_units": float(joined.loc[joined.service_status.eq("partial_active"), "monthly_fee"].sum()),
        "service_state_index_status_proxy": float(joined.olt_performance_weight.mean()),
        "future_activation_records": int(future.sum()),
        "future_activation_share": float(future.mean()),
        "future_by_status": {k: int(v) for k, v in joined.loc[future].service_status.value_counts().sort_index().items()},
        "valid_tenure_records": int(fact.valid_tenure_days.notna().sum()),
        "reported_activation_min_key": int(fact.reported_activation_date_key.min()),
        "reported_activation_max_key": int(fact.reported_activation_date_key.max()),
        "unknown_plan_period_records": int(fact.dq_unknown_plan_period_flag.sum()),
        "review_records": int(review.sum()),
        "review_share": float(review.mean()),
        "plan_period_categories": int(plan.plan_period.nunique(dropna=False)),
        "power_bi_execution": "not verified by this Python/SQLite audit",
    }

    # A separate SQL engine verifies the headline snapshot and quality counts.
    with sqlite3.connect(":memory:") as db:
        fact.to_sql("fact", db, index=False)
        state.to_sql("state", db, index=False)
        sql = db.execute("""
            SELECT COUNT(*), COUNT(DISTINCT customer_key), COUNT(DISTINCT olt_key),
                   SUM(dq_future_activation_flag),
                   SUM(CASE WHEN data_quality_flag='review' THEN 1 ELSE 0 END)
            FROM fact
        """).fetchone()
        expected = (
            receipt["service_records"], receipt["customer_keys"], receipt["olt_groups"],
            receipt["future_activation_records"], receipt["review_records"],
        )
        if sql != expected:
            raise ValueError(f"Python/SQLite headline disagreement: {expected} != {sql}")
        states_sql = dict(db.execute("""
            SELECT s.service_status, COUNT(*) FROM fact f
            JOIN state s ON f.service_state_key=s.service_state_key
            GROUP BY s.service_status
        """).fetchall())
        if states_sql != receipt["service_status_records"]:
            raise ValueError("Python/SQLite status disagreement")
    receipt["independent_sql_reconciliation"] = "passed for headline counts and service statuses"
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, help="Optional JSON receipt path")
    args = parser.parse_args()
    result = audit()
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    print(serialized, end="")


if __name__ == "__main__":
    main()
