# Methodology and measurement limits

The committed model contains one service record per snapshot row, not one unique person. Customer keys group normalized source customer labels; there is no independent identity registry to validate name collisions. Keys are scoped to this build, not stable across reordered extracts. Do not append independently keyed snapshots.

The model's configured snapshot date is 2026-09-12; the original export's actual snapshot date remains unconfirmed. Future public activation dates remain in the audit field and are excluded from valid tenure. The author confirms Activation Date means service activation. A private source comparison found zero original dates after the cutoff but 1,275 public dates differing from source; public tenure/cohort outputs therefore remain unsuitable for source-backed claims until reviewed restoration. See [source review](source_workbook_review.md). This is a snapshot study: inactive is a service status, not observed cancellation or a churn event. No predictive validation is available.

Listed fees are summed at service grain. Billing period/currency normalization and collections are unverified; therefore these totals are fee exposure, not recognized revenue or verified MRR. Partial-active fees indicate exposure, not demonstrated loss.

The service-state index uses analyst-assigned weights active=1, partial-active=0.5, inactive=0. It measures status mix, not utilization, throughput or downtime. Risk denotes partial-active/inactive status; it is not a probability.

Anomaly analysis standardizes OLT high-risk service share using 0.6745*(share-median)/MAD. Absolute scores above 3.5 are review flags. Only 12 OLT groups exist, their sizes differ, and a zero MAD produces undefined scores and no automatic flag. Review the raw rates and denominators before acting.

Privacy: public CSVs exclude direct source identifiers. Surrogate keys and retained plan/date/area attributes can still permit linkage with outside information. Legacy spreadsheets and screenshots were quarantined from the current checkout; old Git history needs separate review and remediation. No claim of historical erasure is made.

Validation: run the unittest suite, anomaly script, and SQLite analysis script. Power BI DAX and SQL Server DDL need their native engines for execution validation.
