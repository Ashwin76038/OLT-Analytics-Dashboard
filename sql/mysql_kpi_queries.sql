-- MySQL 8: run against the loaded public model tables.
-- services
SELECT COUNT(*) FROM fact_customer_service;
-- customers
SELECT COUNT(DISTINCT customer_key) FROM fact_customer_service;
-- active
SELECT COUNT(*) FROM fact_customer_service f JOIN dim_service_state s USING(service_state_key) WHERE s.service_status="active";
-- withheld
SELECT SUM(activation_date_withheld_flag) FROM fact_customer_service;
-- legacy_future
SELECT SUM(legacy_prepared_future_activation_flag) FROM fact_customer_service;
-- unknown_period
SELECT SUM(dq_unknown_plan_period_flag) FROM fact_customer_service;
-- monthly_exposure
SELECT SUM(f.monthly_fee) FROM fact_customer_service f JOIN dim_plan p USING(plan_key) JOIN dim_service_state s USING(service_state_key) WHERE p.plan_period="MONTHLY" AND s.service_status IN ("active","partial_active");
