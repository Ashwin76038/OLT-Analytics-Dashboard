# Executed Power BI validation

On 1 October 2026, the three-page `dashboard/OLT_Service_Project/OLT_Service_Analytics.pbip` opened, refreshed from sanitized CSVs and was saved in Power BI Desktop.

- **114/114 native DAX checks passed**: 19 measures across All, OLT 1, monthly, annual, inactive, and OLT 1 + monthly contexts. Expected values are independently generated with pandas by `scripts/build_dax_validation.py`. `docs/validate_measures.dax` is the actual executed query, and `dax_validation_cases.json` records every expectation.
- The OLT slicer was changed to OLT_0001: 449 services, 428 customer keys, 426 active services, 94.88% active and 23 status-review services. Resetting it restored 1,280 / 1,193 / 1,210 / 94.53% / 70. Cards and both charts updated together.
- Service overview, OLT/plan-period review and data-quality pages were inspected after refresh. Native screenshots are in `dashboard/screenshots/`. No rendered-error placeholders appeared. The public tenure measure remains blank because all precise activation dates are withheld.
- Five single-direction, many-to-one relationships connect the service fact to customer, OLT, plan, state and reference-date dimensions. Source CSV keys/foreign keys are tested; DAX contexts exercised their filtering.
- Listed Exposure In Period is blank across mixed periods; monthly listed exposure reconciles to 2,956,272 undisclosed units. The report's abbreviated card rounds that to 3M. This is a listed amount for active/partial monthly services, not recognized revenue.

Native MySQL 8.0.46 also passed seven public KPI checks; `mysql_validation.json` records them. Python unit tests and SQLite audits are separate from Desktop execution.

This validates the listed measures, pages and representative interactions. It does not establish actual churn, revenue, physical network utilization, confidential portal definitions, every possible filter combination, or a verified export date. Exact source dates and original rows remain private.

## Clean-clone refresh

1. Install the Python requirements; run `python -m unittest discover -s tests -v` and `python scripts/audit_public.py`.
2. Run `python scripts/configure_powerbi.py` to set this checkout's local CSV folder. This changes only the local parameter definition.
3. Open the PBIP above in Desktop. Refresh data, applying pending changes if prompted. No portal connection or confidential workbook is needed.
4. Paste `docs/validate_measures.dax` into DAX query view and run it. Expect Checks=114, Passed=114, and empty Failures.
5. Review all three pages and repeat the OLT slicer/reset check before replacing screenshots. Save locally. Never commit `.pbi` caches or a private PBIX.

The committed CSVs reproduce this frozen snapshot. Repeating the private-source comparison additionally requires the privately supplied workbook; the public clone cannot reproduce confidential extraction.
