# Power BI star schema

Import all six CSV files in this folder and rename the Power BI tables exactly as shown below. The model is a service-snapshot star: one fact row represents one privacy-safe customer service record in the supplied extract.

## Tables

| Power BI table | Role | Grain / contents |
|---|---|---|
| `Fact Customer Service` | Fact | One customer-service snapshot; monthly fee, connection count, and churn flag |
| `Dim Customer` | Dimension | One synthetic customer key and current customer type |
| `Dim OLT` | Dimension | One synthetic OLT and observed exchange code |
| `Dim Plan` | Dimension | One plan configuration and plan-fee usage proxy |
| `Dim Service State` | Dimension | Service status, network-quality proxy, risk level, and reason |
| `Dim Date` | Dimension | Calendar dates from the source activation-date range |

## Relationships

Create these active, one-to-many relationships, with single-direction filtering from dimension to fact:

| From (1) | To (*) | Cross-filter | Active |
|---|---|---|---|
| `Dim Customer[customer_key]` | `Fact Customer Service[customer_key]` | Single | Yes |
| `Dim OLT[olt_key]` | `Fact Customer Service[olt_key]` | Single | Yes |
| `Dim Plan[plan_key]` | `Fact Customer Service[plan_key]` | Single | Yes |
| `Dim Service State[service_state_key]` | `Fact Customer Service[service_state_key]` | Single | Yes |
| `Dim Date[date_key]` | `Fact Customer Service[activation_date_key]` | Single | Yes |

Do not relate dimensions to each other and do not enable bidirectional filtering. Mark `Dim Date` as the date table using `Dim Date[date]`. Hide technical key columns in report view after relationships are validated.

## Data types

- Key columns: Text, except `date_key` and `activation_date_key` (Whole number).
- `monthly_fee`: Fixed decimal number or currency (INR).
- `connection_count` and `churn_flag`: Whole number.
- `Dim Date[date]`: Date.

## Important caveats

- `usage_category` is a monthly-fee proxy, not actual network usage.
- `network_quality_indicator` is derived from service status, not network telemetry.
- Complaint counts are unavailable in this extract; no complaint KPI should be displayed as zero.
- 810 activation records are future-dated relative to 2026-09-12. Resolve this before using activation-date trends, tenure, or cohorts.

## Extension path

When operational data is available, add a `Fact Network Events` table at OLT-date (or customer-date) grain for downtime minutes, packet loss, latency, outages, and complaints. It should connect to `Dim Date`, `Dim OLT`, and, if customer-level, `Dim Customer`; do not join it directly to `Fact Customer Service`.

