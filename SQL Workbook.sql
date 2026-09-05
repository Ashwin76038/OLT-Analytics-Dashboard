CREATE DATABASE isp_analysis;

USE isp_analysis;

CREATE TABLE customers (
    frservice_code VARCHAR(50),
    category VARCHAR(50),
    exchange_code VARCHAR(50),
    service_number VARCHAR(50),
    sub_service_type VARCHAR(100),
    subscription_plan VARCHAR(100),
    plan_period VARCHAR(50),
    fmc DECIMAL(10,2),
    customer VARCHAR(150),
    mobile VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    assign_to VARCHAR(100),
    activation_date DATE,
    olt_ip VARCHAR(50),
    status VARCHAR(50),
    customer_type VARCHAR(50),
    connection_count_per_customer INT,
    customer_clean VARCHAR(150),
    plan_category VARCHAR(50)
);


select count(*) from customers;


SELECT 
    status,
    COUNT(*) AS total_customers
FROM customers
GROUP BY status;

SELECT 
    status,
    COUNT(*) AS total,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customers), 2) AS percentage
FROM customers
GROUP BY status;


SELECT 
    CASE 
        WHEN fmc = 0 THEN 'free_plan'
        WHEN fmc < 400 THEN 'low_value'
        WHEN fmc BETWEEN 400 AND 700 THEN 'mid_value'
        ELSE 'high_value'
    END AS plan_category,
    COUNT(*) AS total_customers
FROM customers
GROUP BY 
    CASE 
        WHEN fmc = 0 THEN 'free_plan'
        WHEN fmc < 400 THEN 'low_value'
        WHEN fmc BETWEEN 400 AND 700 THEN 'mid_value'
        ELSE 'high_value'
    END;
    
SELECT 
    CASE 
        WHEN fmc = 0 THEN 'free_plan'
        WHEN fmc < 400 THEN 'low_value'
        WHEN fmc BETWEEN 400 AND 700 THEN 'mid_value'
        ELSE 'high_value'
    END AS plan_category,
    status,
    COUNT(*) AS total_customers
FROM customers
GROUP BY 
    CASE 
        WHEN fmc = 0 THEN 'free_plan'
        WHEN fmc < 400 THEN 'low_value'
        WHEN fmc BETWEEN 400 AND 700 THEN 'mid_value'
        ELSE 'high_value'
    END,
    status
ORDER BY plan_category;


SELECT 
    plan_category,
    status,
    COUNT(*) AS total,
    ROUND(
        COUNT(*) * 100.0 / 
        SUM(COUNT(*)) OVER (PARTITION BY plan_category), 
    2) AS percentage
FROM (
    SELECT 
        CASE 
            WHEN fmc = 0 THEN 'free_plan'
            WHEN fmc < 400 THEN 'low_value'
            WHEN fmc BETWEEN 400 AND 700 THEN 'mid_value'
            ELSE 'high_value'
        END AS plan_category,
        status
    FROM customers
) t
GROUP BY plan_category, status;


SELECT 
    olt_ip,
    COUNT(*) AS total_customers
FROM customers
GROUP BY olt_ip
ORDER BY total_customers DESC;




SELECT 
    olt_ip,
    status,
    COUNT(*) AS total
FROM customers
GROUP BY olt_ip, status
ORDER BY olt_ip;




SELECT 
    olt_ip,
    COUNT(*) AS total,
    SUM(CASE WHEN status = 'inactive' THEN 1 ELSE 0 END) AS inactive_count,
    SUM(CASE WHEN status = 'partial_active' THEN 1 ELSE 0 END) AS partial_count,
    ROUND(
        (SUM(CASE WHEN status != 'active' THEN 1 ELSE 0 END) * 100.0) / COUNT(*),
    2) AS problem_percentage
FROM customers
GROUP BY olt_ip
ORDER BY problem_percentage DESC;



SELECT 
    olt_ip,
    plan_category,
    status,
    COUNT(*) AS total
FROM customers
GROUP BY olt_ip, plan_category, status
ORDER BY olt_ip;




SELECT 
    olt_ip,
    status,
    COUNT(*) AS total
FROM customers
WHERE plan_category = 'high_value'
GROUP BY olt_ip, status;




SELECT 
    olt_ip,
    COUNT(*) AS total_high_value,
    
    SUM(CASE WHEN status != 'active' THEN 1 ELSE 0 END) AS risky_customers,
    
    ROUND(
        SUM(CASE WHEN status != 'active' THEN 1 ELSE 0 END) * 100.0 
        / COUNT(*), 
    2) AS risk_percentage

FROM customers
WHERE plan_category = 'high_value'
GROUP BY olt_ip
ORDER BY risk_percentage DESC;