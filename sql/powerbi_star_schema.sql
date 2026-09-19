-- SQL Server reference DDL for the privacy-safe Power BI semantic model.
-- Load only the generated CSV fields; never load direct customer identifiers or OLT IP addresses.

CREATE TABLE dbo.Dim_Customer (
    customer_key varchar(20) NOT NULL PRIMARY KEY,
    customer_type varchar(50) NOT NULL,
    connection_count int NOT NULL,
    CONSTRAINT CK_Dim_Customer_Connection_Count CHECK (connection_count >= 1)
);

CREATE TABLE dbo.Dim_OLT (
    olt_key varchar(20) NOT NULL PRIMARY KEY,
    primary_exchange_code varchar(50) NULL,
    exchange_count int NOT NULL,
    multi_exchange_flag bit NOT NULL
);

CREATE TABLE dbo.Dim_Plan (
    plan_key varchar(20) NOT NULL PRIMARY KEY,
    subscription_plan varchar(100) NOT NULL,
    sub_service_type varchar(100) NOT NULL,
    plan_period varchar(50) NOT NULL
);

CREATE TABLE dbo.Dim_Service_State (
    service_state_key varchar(20) NOT NULL PRIMARY KEY,
    service_status varchar(30) NOT NULL,
    is_revenue_generating bit NOT NULL,
    network_quality_indicator varchar(50) NOT NULL,
    risk_level varchar(20) NOT NULL,
    risk_reason varchar(100) NOT NULL,
    olt_performance_weight decimal(5,4) NOT NULL
);

CREATE TABLE dbo.Dim_Date (
    date_key int NOT NULL PRIMARY KEY,
    [date] date NOT NULL UNIQUE,
    [year] smallint NOT NULL,
    [quarter] char(2) NOT NULL,
    month_number tinyint NOT NULL,
    month_name varchar(10) NOT NULL,
    year_month char(7) NOT NULL,
    week_start date NOT NULL,
    is_future_at_extract bit NOT NULL
);

CREATE TABLE dbo.Fact_Customer_Service (
    service_snapshot_key varchar(30) NOT NULL PRIMARY KEY,
    customer_key varchar(20) NOT NULL,
    olt_key varchar(20) NOT NULL,
    plan_key varchar(20) NOT NULL,
    service_state_key varchar(20) NOT NULL,
    activation_date_key int NULL,
    reported_activation_date_key int NULL,
    snapshot_date_key int NOT NULL,
    monthly_fee decimal(12,2) NULL,
    monthly_fee_band varchar(20) NOT NULL,
    inactive_service_flag bit NOT NULL,
    valid_tenure_days int NULL,
    valid_tenure_months int NULL,
    dq_future_activation_flag bit NOT NULL,
    dq_missing_activation_flag bit NOT NULL,
    dq_invalid_fee_flag bit NOT NULL,
    dq_connection_count_flag bit NOT NULL,
    dq_unknown_plan_period_flag bit NOT NULL,
    data_quality_flag varchar(10) NOT NULL,
    CONSTRAINT FK_Fact_Customer FOREIGN KEY (customer_key) REFERENCES dbo.Dim_Customer(customer_key),
    CONSTRAINT FK_Fact_OLT FOREIGN KEY (olt_key) REFERENCES dbo.Dim_OLT(olt_key),
    CONSTRAINT FK_Fact_Plan FOREIGN KEY (plan_key) REFERENCES dbo.Dim_Plan(plan_key),
    CONSTRAINT FK_Fact_State FOREIGN KEY (service_state_key) REFERENCES dbo.Dim_Service_State(service_state_key),
    CONSTRAINT FK_Fact_Activation_Date FOREIGN KEY (activation_date_key) REFERENCES dbo.Dim_Date(date_key),
    CONSTRAINT FK_Fact_Reported_Activation_Date FOREIGN KEY (reported_activation_date_key) REFERENCES dbo.Dim_Date(date_key),
    CONSTRAINT FK_Fact_Snapshot_Date FOREIGN KEY (snapshot_date_key) REFERENCES dbo.Dim_Date(date_key),
    CONSTRAINT CK_Fact_Monthly_Fee CHECK (monthly_fee IS NULL OR monthly_fee >= 0),
    CONSTRAINT CK_Fact_Tenure CHECK (valid_tenure_days IS NULL OR valid_tenure_days >= 0)
);

CREATE INDEX IX_Fact_Customer_Service_Customer ON dbo.Fact_Customer_Service(customer_key);
CREATE INDEX IX_Fact_Customer_Service_OLT ON dbo.Fact_Customer_Service(olt_key);
CREATE INDEX IX_Fact_Customer_Service_Plan ON dbo.Fact_Customer_Service(plan_key);
CREATE INDEX IX_Fact_Customer_Service_State ON dbo.Fact_Customer_Service(service_state_key);
CREATE INDEX IX_Fact_Customer_Service_Activation_Date ON dbo.Fact_Customer_Service(activation_date_key);

-- Expected result for the supplied extract: 810 quarantined future dates and zero
-- future dates in the validated activation key.
SELECT
    SUM(CAST(dq_future_activation_flag AS int)) AS future_date_records,
    SUM(CASE WHEN dq_future_activation_flag = 1 AND activation_date_key IS NOT NULL THEN 1 ELSE 0 END)
        AS future_dates_not_quarantined,
    SUM(CASE WHEN valid_tenure_days < 0 THEN 1 ELSE 0 END) AS negative_valid_tenure_records
FROM dbo.Fact_Customer_Service;
