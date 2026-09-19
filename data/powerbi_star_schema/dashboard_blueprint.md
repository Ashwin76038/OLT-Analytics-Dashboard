# Power BI dashboard blueprint

Use a 16:9 canvas, a consistent top slicer bar, and synced slicers for date, customer type, monthly-fee band, OLT, and service state. Keep technical keys hidden.

## 1. Executive Summary

- KPI cards: Total Customers, Active Customers, Inactive-only Customers, Inactive-only Customer Share, Listed Fee Exposure, Partial-active Listed Fees, Listed Fees per Active Customer.
- Line chart: customer activations by `Dim Date[year_month]`; the active validated date relationship prevents future records from appearing.
- Clustered bar: Partial-active Listed Fees by OLT.
- Donut or 100% stacked bar: customers by service status.
- Small warning card: Invalid Activation Records; show only when greater than zero.

## 2. Service Status & Risk

- KPI cards: Inactive-only Customers, Inactive-only Customer Share, High Risk Customers, Partial-active Listed Fees.
- Ranked bar: Inactive-only Customer Share by monthly-fee band and plan.
- Matrix: customer type x monthly-fee band with Total Customers, Inactive-only Customers, Inactive-only Customer Share, and Partial-active Listed Fees.
- Column chart: High Risk Customers by valid tenure band.
- Decomposition tree: Partial-active Listed Fees by OLT, monthly-fee band, customer type, and service status.

## 3. OLT Performance

- KPI cards: Service State Index, High Risk Customers, At-risk Listed Fees, Partial-active Listed Fees.
- Ranked bar: Service State Index by OLT; apply conditional colors to emphasize low scores.
- Matrix: OLT with Total Customers, Active Customers, Inactive-only Customers, High Risk Customers, Partial-active Listed Fees, and performance KPI.
- 100% stacked bar: service-state mix by OLT.
- Tooltip page: OLT customer mix, plan mix, and data-quality flags.

`Service State Index` and `At-risk Listed Fees` are service-state proxies. Label them accordingly until network-event telemetry supplies downtime minutes, latency, packet loss, and outage duration.

## 4. Customer Segmentation

- KPI cards: Total Customers, Listed Fees per Active Customer, Listed Fee Exposure, High Risk Customers.
- Treemap: customers by customer type and monthly-fee band.
- Scatter: plan-level Listed Fees per Active Customer versus Inactive-only Customer Share; bubble size = Total Customers.
- Stacked bar: customer count by connection-count band and service status.
- Detail table: synthetic customer key, customer type, connection count, plan, OLT key, service state, valid tenure months, and Partial-active Listed Fees. Do not add direct identifiers.

## Slicer behavior

- Date slicer uses only `Dim Date[date]` through the active validated activation relationship.
- Use dropdown slicers for high-cardinality plan and OLT fields; enable search.
- Sync common slicers across pages, but keep service-status slicers page-specific where they could change KPI meaning.
- Add a reset-filters bookmark on each page.
- Do not expose `reported_activation_date_key` except on a restricted data-quality audit page.
