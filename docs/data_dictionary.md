# Data dictionary

See the [model definitions](../data/powerbi_star_schema/relationships_and_model.md) and [methodology](methodology.md) for formulas and caveats.

| Table | Column | Stored type | Source / transformation |
|---|---|---|---|
| dim_customer | customer_key | object | Build-scoped surrogate key |
| dim_customer | customer_type | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_customer | connection_count | int64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_date | date | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_date | date_key | int64 | Build-scoped surrogate key |
| dim_date | year | int64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_date | quarter | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_date | month_number | int64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_date | month_name | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_date | year_month | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_date | week_start | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_date | is_future_at_extract | bool | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_olt | olt_key | object | Build-scoped surrogate key |
| dim_olt | exchange_count | int64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_olt | primary_exchange_code | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_olt | multi_exchange_flag | int64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_plan | plan_key | object | Build-scoped surrogate key |
| dim_plan | subscription_plan | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_plan | sub_service_type | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_plan | plan_period | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_service_state | service_state_key | object | Build-scoped surrogate key |
| dim_service_state | service_status | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_service_state | is_revenue_generating | int64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_service_state | network_quality_indicator | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_service_state | risk_level | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_service_state | risk_reason | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| dim_service_state | olt_performance_weight | float64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| fact_customer_service | service_snapshot_key | object | Build-scoped surrogate key |
| fact_customer_service | customer_key | object | Build-scoped surrogate key |
| fact_customer_service | olt_key | object | Build-scoped surrogate key |
| fact_customer_service | plan_key | object | Build-scoped surrogate key |
| fact_customer_service | service_state_key | object | Build-scoped surrogate key |
| fact_customer_service | activation_date_key | float64 | Build-scoped surrogate key |
| fact_customer_service | reported_activation_date_key | int64 | Build-scoped surrogate key |
| fact_customer_service | snapshot_date_key | int64 | Build-scoped surrogate key |
| fact_customer_service | monthly_fee | float64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| fact_customer_service | monthly_fee_band | object | ETL output; see build_powerbi_star_schema.py and model definitions |
| fact_customer_service | inactive_service_flag | int64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| fact_customer_service | valid_tenure_days | float64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| fact_customer_service | valid_tenure_months | float64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| fact_customer_service | dq_future_activation_flag | int64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| fact_customer_service | dq_missing_activation_flag | int64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| fact_customer_service | dq_invalid_fee_flag | int64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| fact_customer_service | dq_connection_count_flag | int64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| fact_customer_service | dq_unknown_plan_period_flag | int64 | ETL output; see build_powerbi_star_schema.py and model definitions |
| fact_customer_service | data_quality_flag | object | ETL output; see build_powerbi_star_schema.py and model definitions |
