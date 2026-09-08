# 📊 OLT Analytics Dashboard

Power BI dashboard analyzing telecom/ISP operations — customer status, plan revenue, OLT load, and churn risk — modeled on my family's fiber ISP business (~1,400 subscribers, 24 OLTs, 4 plan tiers).

---

## 🧩 Business Context

Customers on this network don't churn instantly — they go inactive first. Two operational patterns drive that:
- **Overloaded OLTs** → degraded speed → dissatisfaction → inactivity
- **Revenue leaks silently** — inactive/partial-active accounts sit unflagged for weeks before churn becomes visible in raw signups/cancellations

This dashboard exists to catch those early signals before they show up as lost revenue.

---

## 📊 Key Metrics (simulated dataset, structured to match real ops)

| Metric | Value |
|---|---|
| Total Customers | 1,280 |
| Active | 94.53% (1,210) |
| Partial Active | 3.20% (41) |
| Inactive | 2.27% (29) |
| Total OLTs | 24 |
| Avg Connections / OLT | 53 |
| Highest Load OLT | OLT-08 — 243 connections (4.6× avg) |
| Lowest Load OLT | OLT-17 — 12 connections |
| Total Revenue | ₹3.3M |
| Revenue at Risk | ₹0.86M (26% of total) |

---

## 📈 Key Findings

**1. OLT Load Imbalance**
OLT-08 carries 243 connections vs. a 53-connection average (4.6× overload). This is a congestion risk that directly precedes service complaints and inactivity spikes on that node.

**2. Revenue Concentration**
High-value plan customers make up 18% of the customer base but generate 61% of total revenue. Losing even a small fraction of this segment has an outsized financial impact compared to losing an equivalent number of low-tier customers.

**3. Early Churn Signal**
41 customers (3.2%) are in "partial active" status — the leading indicator before full churn. This is the group retention efforts should target first, before they convert to inactive.

**4. Revenue at Risk**
₹0.86M (26% of total revenue) sits with inactive/partial-active accounts. A relatively small share of at-risk customers accounts for a disproportionate revenue exposure.

**5. Risk Is Localized, Not Distributed**
The top 2 OLTs (OLT-08, OLT-14) account for 58% of all inactive customers — meaning this is an operational/infrastructure problem concentrated in specific areas, not a company-wide churn issue. That makes it fixable with targeted OLT maintenance rather than a broad retention campaign.

---

## 🧠 Technical Implementation

**Data Model**
`Customers` → `OLT` (many-to-one) · `Customers` → `Plan` (many-to-one) · status tracked per customer record

**DAX Measures**

```dax
Revenue_at_Risk =
CALCULATE(
    SUM('OLT'[Total Revenue]),
    'OLT'[status] IN {"inactive", "partial_active"}
)

Risk_Percentage =
DIVIDE([Risk_Customers], [Total_Connections], 0)

Avg_Connections_per_OLT =
DIVIDE([Total_Connections], [Total_OLTs])
```

**SQL (data prep)**

```sql
SELECT 
    olt_ip,
    COUNT(customer) AS total_connections,
    SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS active,
    SUM(CASE WHEN status = 'inactive' THEN 1 ELSE 0 END) AS inactive,
    SUM(CASE WHEN status = 'partial_active' THEN 1 ELSE 0 END) AS partial_active
FROM olt_data
GROUP BY olt_ip
ORDER BY total_connections DESC;
```

---

## 📊 Dashboard Pages

| Page | Preview |
|---|---|
| Overview | [View](Screenshots/overview.png) |
| Plan Analysis | [View](Screenshots/plan-analysis.png) |
| OLT Analysis | [View](Screenshots/olt-analysis.png) |
| Risk Analysis | [View](Screenshots/risk-analysis.png) |

---

## 📁 Dataset Note

Real ISP data is not shared for privacy reasons. A synthetic dataset (~1,000 rows) is included, structured to match the real schema and enable full demonstration of the dashboard logic.

---

## ⚙️ How to Use

1. Download the `.pbix` file
2. Open in Power BI Desktop
3. Explore the four dashboard pages

---

## 📬 Contact

- LinkedIn: [linkedin.com/in/aswin760](https://www.linkedin.com/in/aswin760/)
- Email: aswinaswin6552@gmail.com
