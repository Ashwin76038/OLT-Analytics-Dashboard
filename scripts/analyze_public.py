"""Recompute portfolio evidence from published tables using SQLite."""
from pathlib import Path
import json, sqlite3
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
def analyze():
    db = sqlite3.connect(":memory:")
    for p in (ROOT / "data/powerbi_star_schema").glob("*.csv"):
        pd.read_csv(p).to_sql(p.stem, db, index=False)
    totals = db.execute("SELECT COUNT(*), COUNT(DISTINCT customer_key), COUNT(DISTINCT olt_key), SUM(dq_future_activation_flag) FROM fact_customer_service").fetchone()
    states = db.execute("SELECT s.service_status, COUNT(*), SUM(f.monthly_fee) FROM fact_customer_service f JOIN dim_service_state s USING(service_state_key) GROUP BY s.service_status").fetchall()
    result = dict(service_records=totals[0], customer_keys=totals[1], olts=totals[2], future_dates=totals[3], states=[dict(status=s, records=n, listed_fees=v) for s,n,v in states])
    (ROOT / "docs/validated_metrics.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    return result
if __name__ == "__main__":
    analyze()
