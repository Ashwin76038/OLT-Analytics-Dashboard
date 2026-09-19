"""Build privacy-safe Power BI star-schema CSVs from the ignored source extract.

The script never writes direct customer identifiers or private OLT addresses.
Surrogate keys are sequential and scoped to the generated model.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {
    "customer_clean",
    "customer_type",
    "connection_count_per_customer",
    "OLT IP",
    "exchange_code",
    "subscription_plan",
    "sub_service_type",
    "plan_period",
    "fmc",
    "status",
    "activation date",
}


def normalized_text(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip().str.lower()


def sequential_keys(values: pd.Series, prefix: str) -> pd.Series:
    unique_values = pd.Series(pd.unique(values), dtype="string")
    mapping = pd.DataFrame({"_business_key": unique_values})
    mapping["_surrogate_key"] = [f"{prefix}_{i:04d}" for i in range(1, len(mapping) + 1)]
    key_map = dict(zip(mapping["_business_key"], mapping["_surrogate_key"]))
    return values.map(key_map)


def build_model(source_path: Path, output_dir: Path, as_of_date: pd.Timestamp) -> None:
    source = pd.read_csv(source_path)
    missing = sorted(REQUIRED_COLUMNS - set(source.columns))
    if missing:
        raise ValueError(f"Missing required source columns: {', '.join(missing)}")

    if source.empty:
        raise ValueError("Source contains no service records")
    for key in ["customer_clean", "OLT IP", "status"]:
        if normalized_text(source[key]).fillna("").eq("").any():
            raise ValueError(f"Missing required identity/state field: {key}")
    output_dir.mkdir(parents=True, exist_ok=True)

    source["_customer_business_key"] = normalized_text(source["customer_clean"])
    source["_olt_business_key"] = normalized_text(source["OLT IP"])
    source["_status"] = normalized_text(source["status"])
    source["_customer_type"] = normalized_text(source["customer_type"])
    source["_activation_date"] = pd.to_datetime(source["activation date"], errors="coerce").dt.normalize()
    source["_monthly_fee"] = pd.to_numeric(source["fmc"], errors="coerce")
    source["_source_connection_count"] = pd.to_numeric(
        source["connection_count_per_customer"], errors="coerce"
    )

    allowed_statuses = {"active", "partial_active", "inactive"}
    unexpected_statuses = sorted(set(source["_status"].dropna()) - allowed_statuses)
    if unexpected_statuses:
        raise ValueError(f"Unexpected service status values: {unexpected_statuses}")

    source["customer_key"] = sequential_keys(source["_customer_business_key"], "CUST")
    source["olt_key"] = sequential_keys(source["_olt_business_key"], "OLT")

    plan_columns = ["subscription_plan", "sub_service_type", "plan_period"]
    plan_business = source[plan_columns].fillna("unknown").astype("string").apply(
        lambda col: col.str.strip().str.lower()
    )
    source["_plan_business_key"] = plan_business.agg("|".join, axis=1)
    source["plan_key"] = sequential_keys(source["_plan_business_key"], "PLAN")

    state_order = pd.Series(["active", "partial_active", "inactive"], dtype="string")
    state_key_map = {value: f"STATE_{i:04d}" for i, value in enumerate(state_order, 1)}
    source["service_state_key"] = source["_status"].map(state_key_map)

    future_activation = source["_activation_date"] > as_of_date
    missing_activation = source["_activation_date"].isna()
    invalid_fee = source["_monthly_fee"].isna() | (source["_monthly_fee"] < 0)

    actual_connections = source.groupby("_customer_business_key")["_customer_business_key"].transform("size")
    invalid_connection_count = (
        source["_source_connection_count"].isna()
        | (source["_source_connection_count"] < 1)
        | (source["_source_connection_count"] != actual_connections)
    )
    unknown_plan_period = normalized_text(source["plan_period"]).fillna("unknown").isin(
        {"", "unknown", "n/a", "na", "unspecified"}
    )

    valid_activation = source["_activation_date"].where(~future_activation & ~missing_activation)
    source["activation_date_key"] = valid_activation.dt.strftime("%Y%m%d").astype("Int64")
    source["reported_activation_date_key"] = (
        source["_activation_date"].dt.strftime("%Y%m%d").astype("Int64")
    )
    source["snapshot_date_key"] = int(as_of_date.strftime("%Y%m%d"))
    source["valid_tenure_days"] = (
        (as_of_date - valid_activation).dt.days.astype("Int64")
    )
    source["valid_tenure_months"] = np.floor(source["valid_tenure_days"] / 30.4375).astype("Int64")

    source["dq_future_activation_flag"] = future_activation.astype("int8")
    source["dq_missing_activation_flag"] = missing_activation.astype("int8")
    source["dq_invalid_fee_flag"] = invalid_fee.astype("int8")
    source["dq_connection_count_flag"] = invalid_connection_count.astype("int8")
    source["dq_unknown_plan_period_flag"] = unknown_plan_period.astype("int8")
    dq_columns = [
        "dq_future_activation_flag",
        "dq_missing_activation_flag",
        "dq_invalid_fee_flag",
        "dq_connection_count_flag",
        "dq_unknown_plan_period_flag",
    ]
    source["data_quality_flag"] = np.where(source[dq_columns].any(axis=1), "review", "valid")

    customer_dim = source.groupby("customer_key", sort=False).agg(
        customer_type=("_customer_type", "first"),
        connection_count=("_customer_business_key", "size"),
    ).reset_index()

    olt_dim = source.groupby("olt_key", sort=False).agg(
        exchange_count=("exchange_code", "nunique"),
        primary_exchange_code=("exchange_code", lambda s: s.mode().iloc[0] if not s.mode().empty else "unknown"),
    ).reset_index()
    olt_dim["multi_exchange_flag"] = (olt_dim["exchange_count"] > 1).astype("int8")

    plan_first = source.drop_duplicates("plan_key", keep="first")
    plan_dim = plan_first[["plan_key", *plan_columns]].copy()
    for column in plan_columns:
        plan_dim[column] = plan_dim[column].astype("string").str.strip()
    source["monthly_fee_band"] = pd.cut(
        source["_monthly_fee"],
        bins=[-np.inf, 399.9999, 700, np.inf],
        labels=["low", "medium", "high"],
    ).astype("string").fillna("unknown")

    state_dim = pd.DataFrame(
        {
            "service_state_key": [state_key_map[s] for s in state_order],
            "service_status": state_order,
            "is_revenue_generating": [1, 1, 0],
            "network_quality_indicator": [
                "telemetry_not_available",
                "degraded_service_state",
                "disconnected",
            ],
            "risk_level": ["low", "high", "high"],
            "risk_reason": [
                "no_observed_risk_signal",
                "partial_active_service",
                "disconnected_or_cancelled",
            ],
            "olt_performance_weight": [1.0, 0.5, 0.0],
        }
    )

    all_dates = pd.concat(
        [source["_activation_date"].dropna(), pd.Series([as_of_date])], ignore_index=True
    )
    calendar = pd.DataFrame({"date": pd.date_range(all_dates.min(), all_dates.max(), freq="D")})
    calendar["date_key"] = calendar["date"].dt.strftime("%Y%m%d").astype("int64")
    calendar["year"] = calendar["date"].dt.year
    calendar["quarter"] = "Q" + calendar["date"].dt.quarter.astype("string")
    calendar["month_number"] = calendar["date"].dt.month
    calendar["month_name"] = calendar["date"].dt.month_name()
    calendar["year_month"] = calendar["date"].dt.strftime("%Y-%m")
    calendar["week_start"] = calendar["date"] - pd.to_timedelta(calendar["date"].dt.weekday, unit="D")
    calendar["is_future_at_extract"] = calendar["date"] > as_of_date

    fact = source.assign(
        service_snapshot_key=[f"SERVICE_{i:06d}" for i in range(1, len(source) + 1)],
        monthly_fee=source["_monthly_fee"].where(~invalid_fee),
        inactive_service_flag=(source["_status"] == "inactive").astype("int8"),
    )[
        [
            "service_snapshot_key",
            "customer_key",
            "olt_key",
            "plan_key",
            "service_state_key",
            "activation_date_key",
            "reported_activation_date_key",
            "snapshot_date_key",
            "monthly_fee",
            "monthly_fee_band",
            "inactive_service_flag",
            "valid_tenure_days",
            "valid_tenure_months",
            *dq_columns,
            "data_quality_flag",
        ]
    ]

    outputs = {
        "fact_customer_service.csv": fact,
        "dim_customer.csv": customer_dim,
        "dim_olt.csv": olt_dim,
        "dim_plan.csv": plan_dim,
        "dim_service_state.csv": state_dim,
        "dim_date.csv": calendar,
    }
    for filename, frame in outputs.items():
        frame.to_csv(
            output_dir / filename,
            index=False,
            date_format="%Y-%m-%d",
            lineterminator="\n",
        )

    print(f"Built {len(fact):,} service rows and {len(customer_dim):,} customers.")
    print(f"Future activation dates quarantined: {int(future_activation.sum()):,}.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("customers.csv"))
    parser.add_argument(
        "--output", type=Path, default=Path("data/powerbi_star_schema")
    )
    parser.add_argument("--as-of-date", default="2026-09-12")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    build_model(args.source, args.output, pd.Timestamp(args.as_of_date).normalize())
