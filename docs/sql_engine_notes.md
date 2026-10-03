# SQL engine and reproduction

The author used **MySQL**. Native MySQL 8.0.46 was used on 1 October 2026 to load public CSVs into an isolated, new audit schema and reconcile seven aggregates with pandas. See `mysql_validation.json` and `sql/mysql_kpi_queries.sql`. This verifies the supplied audit queries, not an undisclosed original MySQL workflow.

Run against your own authorized MySQL 8 instance:

```bash
python scripts/validate_mysql.py --client mysql --schema portfolio_audit_olt_new -- --host=127.0.0.1 --port=3306 --user=YOUR_USER
```

Use an existing secure client configuration for credentials. The schema must not already exist; the script does not drop or overwrite one. `analyze_public.py` and `audit_public.py` additionally use in-memory SQLite for portable independent checks. Desktop validation is separately recorded in `powerbi_validation.md`.

The obsolete SQL Server reference DDL has been removed; MySQL loading and executable KPI queries are the supported SQL route.
