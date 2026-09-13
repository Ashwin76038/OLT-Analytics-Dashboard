"""Create privacy-safe OLT service-health anomaly output from the star schema."""

from pathlib import Path

import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "data" / "powerbi_star_schema"

fact = pd.read_csv(MODEL_DIR / "fact_customer_service.csv")
state = pd.read_csv(MODEL_DIR / "dim_service_state.csv")

service_health = fact.merge(
    state[["service_state_key", "risk_level", "olt_performance_weight"]],
    on="service_state_key",
    how="left",
    validate="many_to_one",
)

if service_health[["risk_level", "olt_performance_weight"]].isna().any().any():
    raise ValueError("Service-state join failed; check model referential integrity.")

olt_stats = service_health.groupby("olt_key", as_index=False).agg(
    service_count=("service_snapshot_key", "count"),
    high_risk_service_count=("risk_level", lambda values: (values == "high").sum()),
    olt_performance_kpi=("olt_performance_weight", "mean"),
)
olt_stats["high_risk_service_rate"] = (
    olt_stats["high_risk_service_count"] / olt_stats["service_count"]
)

median = olt_stats["high_risk_service_rate"].median()
mad = np.median(np.abs(olt_stats["high_risk_service_rate"] - median))
if mad == 0:
    olt_stats["robust_z_score"] = np.nan
    olt_stats["is_anomaly"] = False
else:
    olt_stats["robust_z_score"] = (
        0.6745 * (olt_stats["high_risk_service_rate"] - median) / mad
    )
    olt_stats["is_anomaly"] = olt_stats["robust_z_score"].abs() > 3.5

output_path = BASE_DIR / "data" / "olt_anomaly_output.csv"
olt_stats.sort_values("high_risk_service_rate", ascending=False).to_csv(
    output_path, index=False, lineterminator="\n"
)
print(f"Saved privacy-safe OLT anomaly output to {output_path}.")
