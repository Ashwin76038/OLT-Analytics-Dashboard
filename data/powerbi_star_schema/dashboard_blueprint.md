# Power BI dashboard blueprint

Use a 16:9 canvas, a consistent top slicer bar, and synced slicers for date, customer type, monthly-fee band, OLT, and service state. Keep technical keys hidden.

## 1. Executive Summary

- KPI cards: Total Customers, Active Customers, Churned Customers, Churn Rate, Revenue (MRR), Revenue at Risk, ARPU.
- Line chart: customer activations by `Dim Date[year_month]`; the active validated date relationship prevents future records from appearing.
- Clustered bar: Revenue at Risk by OLT.
- Donut or 100% stacked bar: customers by service status.
- Small warning card: Invalid Activation Records; show only when greater than zero.

## 2. Churn Analysis

- KPI cards: Churned Customers, Churn Rate, High Risk Customers, Revenue at Risk.
- Ranked bar: Churn Rate by monthly-fee band and plan.
- Matrix: customer type x monthly-fee band with Total Customers, Churned Customers, Churn Rate, and Revenue at Risk.
- Column chart: High Risk Customers by valid tenure band.
- Decomposition tree: Revenue at Risk by OLT, monthly-fee band, customer type, and service status.

## 3. OLT Performance

- KPI cards: OLT Performance KPI, High Risk Customers, Downtime Impact, Revenue at Risk.
- Ranked bar: OLT Performance KPI by OLT; apply conditional colors to emphasize low scores.
- Matrix: OLT with Total Customers, Active Customers, Churned Customers, High Risk Customers, Revenue at Risk, and performance KPI.
- 100% stacked bar: service-state mix by OLT.
- Tooltip page: OLT customer mix, plan mix, and data-quality flags.

`OLT Performance KPI` and `Downtime Impact` are service-state proxies. Label them accordingly until network-event telemetry supplies downtime minutes, latency, packet loss, and outage duration.

## 4. Customer Segmentation

- KPI cards: Total Customers, ARPU, Revenue (MRR), High Risk Customers.
- Treemap: customers by customer type and monthly-fee band.
- Scatter: plan-level ARPU versus Churn Rate; bubble size = Total Customers.
- Stacked bar: customer count by connection-count band and service status.
- Detail table: synthetic customer key, customer type, connection count, plan, OLT key, service state, valid tenure months, and Revenue at Risk. Do not add direct identifiers.

## Slicer behavior

- Date slicer uses only `Dim Date[date]` through the active validated activation relationship.
- Use dropdown slicers for high-cardinality plan and OLT fields; enable search.
- Sync common slicers across pages, but keep service-status slicers page-specific where they could change KPI meaning.
- Add a reset-filters bookmark on each page.
- Do not expose `reported_activation_date_key` except on a restricted data-quality audit page.
