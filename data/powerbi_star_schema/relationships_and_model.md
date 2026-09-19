# Power BI semantic model

The model is a periodic service snapshot. One row in `Fact Customer Service` represents one service as observed on the extract date. Customer KPIs use distinct customer keys; revenue and service-health KPIs use service rows.

## Table definitions

### Fact Customer Service

| Column | Type | Role |
|---|---|---|
| `service_snapshot_key` | Text | Primary key; hide |
| `customer_key` | Text | FK to `Dim Customer`; hide |
| `olt_key` | Text | FK to `Dim OLT`; hide |
| `plan_key` | Text | FK to `Dim Plan`; hide |
| `service_state_key` | Text | FK to `Dim Service State`; hide |
| `activation_date_key` | Whole number, nullable | Validated activation-date FK; future/missing dates are blank |
| `reported_activation_date_key` | Whole number, nullable | Raw reported-date FK for audit only; hide |
| `snapshot_date_key` | Whole number | Extract-date FK; hide |
| `monthly_fee` | Fixed decimal/currency | Supplied service-level fee; billing-period normalization unverified |
| `monthly_fee_band` | Text | Fee-derived segment; kept at service grain because fees vary within plan configurations |
| `inactive_service_flag` | Whole number | 1 only for an inactive service |
| `valid_tenure_days` | Whole number, nullable | Days from valid activation date to extract date |
| `valid_tenure_months` | Whole number, nullable | Completed 30.4375-day months; use for bands, not billing |
| `dq_*_flag` | Whole number | Row-level quality flags (0/1) |
| `data_quality_flag` | Text | `valid` or `review` |

### Dim Customer

Primary key: `customer_key`. Columns: `customer_type`, `connection_count`. The count belongs here because it is a customer-level attribute and would be double-counted in the service fact.

### Dim OLT

Primary key: `olt_key`. Columns: `primary_exchange_code`, `exchange_count`, `multi_exchange_flag`. Private OLT addresses are deliberately excluded. An OLT can map to multiple exchange codes in the supplied extract, so the mode is labeled as the primary exchange rather than presented as a guaranteed one-to-one attribute.

### Dim Plan

Primary key: `plan_key`. Columns: `subscription_plan`, `sub_service_type`, `plan_period`. Fee-derived categories were removed from this dimension because monthly fees vary within otherwise identical plan configurations; `monthly_fee_band` stays in the fact.

### Dim Service State

Primary key: `service_state_key`. Columns: `service_status`, `is_revenue_generating`, `network_quality_indicator`, `risk_level`, `risk_reason`, `olt_performance_weight`. The performance weight is 1.0 for active, 0.5 for partial-active, and 0 for inactive.

### Dim Date

Primary key: `date_key`. Columns: `date`, `year`, `quarter`, `month_number`, `month_name`, `year_month`, `week_start`, `is_future_at_extract`. Mark this table as the date table using `Dim Date[date]`; sort `month_name` by `month_number` and `year_month` by a dedicated year-month number (year * 100 + month_number).

## Relationships

All relationships are `1:*`, dimension-to-fact, single-direction. Do not enable bidirectional filtering and do not relate dimensions to one another.

| From (1) | To (*) | Active | Purpose |
|---|---|---:|---|
| `Dim Customer[customer_key]` | `Fact Customer Service[customer_key]` | Yes | Customer slicing |
| `Dim OLT[olt_key]` | `Fact Customer Service[olt_key]` | Yes | OLT slicing |
| `Dim Plan[plan_key]` | `Fact Customer Service[plan_key]` | Yes | Plan slicing |
| `Dim Service State[service_state_key]` | `Fact Customer Service[service_state_key]` | Yes | Service-state slicing |
| `Dim Date[date_key]` | `Fact Customer Service[activation_date_key]` | Yes | Default cohort/tenure date; invalid dates cannot filter facts |
| `Dim Date[date_key]` | `Fact Customer Service[reported_activation_date_key]` | No | Data-quality audit of reported dates |
| `Dim Date[date_key]` | `Fact Customer Service[snapshot_date_key]` | No | Snapshot trend once multiple extracts are appended |

Only one date relationship can be active. Measures that intentionally use reported or snapshot dates must call `USERELATIONSHIP`.

## Optimization and governance

- Use Import mode for this dataset and disable Auto date/time.
- Keep numeric keys as Whole number and surrogate entity keys as Text; never summarize keys.
- Hide fact foreign keys, quality helper fields not used in visuals, and all technical columns.
- Put measures in a dedicated `_Measures` table with display folders: Customer, Revenue, OLT, and Data Quality.
- Use explicit measures rather than implicit aggregation.
- Preserve `BLANK()` for unavailable complaint data and undefined ratios.
- Do not publish the existing PBIX until its imported source is replaced with these privacy-safe tables; PBIX files can retain embedded source rows.

## Data-quality policy

The extract date is 2026-09-12. The 810 later activation dates are retained only in `reported_activation_date_key`, flagged, and excluded from `activation_date_key`, tenure, cohorts, and default date filtering. Do not coerce them to the extract date because that would invent activation events.
