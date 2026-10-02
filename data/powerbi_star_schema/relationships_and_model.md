# Public model

`fact_customer_service`: unique service_snapshot_key, 1,280 service observations, not 1,280 unique customers. `dim_customer`: 1,193 normalized source-label groups. `dim_olt`: 12 source-address groups, not verified physical devices. `dim_plan`: subscription plan, sub-service and billing-period labels. `dim_service_state`: assumed A/D/E classification. `dim_date`: the single analyst reference date 2026-09-12.

In Desktop, each dimension filters the fact through a one-to-many, single-direction relationship: customer_key, olt_key, plan_key, service_state_key, and date_key to snapshot_date_key. There are no activation-date relationships; all public activation and tenure fields are null. Historical prepared future flags remain for audit only.

Use explicit measures from the committed PBIP. Do not sum distinct-customer subtotals, compare mixed-period fees as MRR, or use status weights as network performance. Legacy state fields `is_revenue_generating`, `network_quality_indicator`, `risk_level`, and `risk_reason` are old status-derived labels, not verified billing, telemetry or cancellation events; report measures do not use them for those claims.

See [dictionary](../../docs/data_dictionary.md), [methodology](../../docs/methodology.md), and [executed report validation](../../docs/powerbi_validation.md).
