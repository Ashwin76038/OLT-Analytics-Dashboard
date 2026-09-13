# OLT Analytics Dashboard

A privacy-safe telecom/ISP analytics project for monitoring service status, churn risk, commercial plan mix, and OLT-level customer impact in Power BI.

## Business problem

Operations and retention teams need to identify where inactive and partial-active services are concentrated, estimate recurring revenue at risk, and prioritize interventions by OLT, plan, and customer segment.

## Privacy and source data

Do not commit or publish raw customer extracts. The original source includes direct identifiers such as names, mobile numbers, email addresses, physical addresses, service numbers, staff names, and private OLT IP addresses.

The files in [`data/powerbi_star_schema`](data/powerbi_star_schema) are privacy-safe. Direct identifiers have been removed and relationship keys are synthetic. The current `OLT Dashboard.pbix` must be rebuilt from these safe tables before publishing because Power BI files may embed imported source rows. The PBIX is ignored for future commits; if a sensitive version was previously pushed, remove it from Git history before making the repository public.

## Rebuild the safe model

From the repository root, with the ignored source extract available locally:

```powershell
python scripts/build_powerbi_star_schema.py --source customers.csv --as-of-date 2026-09-12
python anomaly_detection.py
python -m unittest tests.test_star_schema -v
```

The build creates 1,280 service-snapshot rows for 1,193 distinct customers. It quarantines 810 future activation dates: the reported date remains available for audit, while the active validated date key and tenure fields stay blank for those rows.

## Power BI model

Import all CSV files in `data/powerbi_star_schema` and rename the tables as follows:

| CSV | Power BI table |
|---|---|
| `fact_customer_service.csv` | `Fact Customer Service` |
| `dim_customer.csv` | `Dim Customer` |
| `dim_olt.csv` | `Dim OLT` |
| `dim_plan.csv` | `Dim Plan` |
| `dim_service_state.csv` | `Dim Service State` |
| `dim_date.csv` | `Dim Date` |

Create one-to-many, single-direction relationships from each dimension to `Fact Customer Service`. The validated activation-date relationship is active; reported activation date and snapshot date are inactive. Exact keys, columns, types, and model constraints are documented in [`relationships_and_model.md`](data/powerbi_star_schema/relationships_and_model.md).

## Measures

Create the measures in [`churn_kpi_measures.dax`](data/powerbi_star_schema/churn_kpi_measures.dax). They include:

- Total, active, churned, and high-risk customers
- Churn rate, revenue (MRR), revenue at risk, and ARPU
- OLT performance and downtime-impact proxies
- Invalid activation and overall data-quality review counts

The supplied extract has no complaint, latency, packet-loss, or downtime-duration records. The complaint metric intentionally stays blank rather than showing a misleading zero. OLT performance and downtime impact are service-state proxies until network-event telemetry is added.

## Data quality caveat

The generated fact contains validated tenure, a quarantined reported-date key, and flags for future/missing activation dates, invalid fees, inconsistent connection counts, and unknown plan periods. Do not replace invalid dates with the extract date because that would create false activation events.

## Recommended report pages

1. **Executive Summary** — customer base, churn rate, MRR, revenue at risk, ARPU, and a data-quality warning.
2. **Churn Analysis** — churn and risk by plan, monthly-fee band, customer type, OLT, and valid tenure.
3. **OLT Performance** — service-state mix, OLT performance proxy, high-risk customers, and downtime-impact proxy.
4. **Customer Segmentation** — customer type, connection count, plan, monthly-fee band, tenure, and risk.

The detailed visual, KPI, and slicer specification is in [`dashboard_blueprint.md`](data/powerbi_star_schema/dashboard_blueprint.md).

## GitHub update plan

Commit the privacy-safe model CSVs, DAX, model documentation, dashboard blueprint, SQL DDL, ETL script, anomaly script, README, and `.gitignore`. Do not commit raw extracts, spreadsheets, local databases, or PBIX files until the PBIX has been rebuilt exclusively from reviewed safe inputs. Review screenshots for identifiers before committing them.

## Project structure

```text
data/powerbi_star_schema/  Reviewed fact/dimension CSVs, DAX, and implementation guides
scripts/                   Reproducible privacy-safe model build
sql/                       SQL Server reference DDL and constraints
anomaly_detection.py       Privacy-safe OLT anomaly analysis
Screenshots/               Dashboard screenshots; review before publishing
```
