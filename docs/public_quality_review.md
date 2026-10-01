# Public snapshot quality review

Run `python scripts/audit_public.py --output docs/public_audit.json` to reproduce the aggregate receipt. It reads only the six committed sanitized tables and independently reconciles headline counts with SQLite. The existing star-schema tests and new audit tests cover keys, foreign keys, future-date exclusions, review counts and important KPI denominators.

**Source reconciliation update, 1 October 2026:** the author supplied the original workbook and clarified Activation Date as service activation. The original selected rows contain zero dates after the configured cutoff, whereas 1,275 public dates differ from source. The table below describes the still-uncorrected public model; the 810 future values must not be attributed to the original workbook. See [source review](source_workbook_review.md).

| Finding | Current evidence | Decision risk | Action |
|---|---:|---|---|
| Future reported activation | 810/1,280 service rows (63.28%); 772 active, 22 partial-active, 16 inactive | Tenure/cohort results would be invalid if these dates were used | Retain source date for audit; exclude from validated activation/tenure until source meaning is confirmed |
| Other quality flags | 816/1,280 review rows (63.75%); 58 rows have unknown plan period, with overlap with future-date rows | Missing period prevents interpreting fee cadence | Resolve period definitions upstream; do not convert listed fees to MRR |
| Grain/identity | 1,280 service rows versus 1,193 grouped customer keys; 22 inactive-only keys | Service shares and customer shares need different denominators; keys are not verified people | Label every KPI by grain; require stable source IDs before multi-snapshot claims |
| Status mix | 1,210 active, 41 partial-active, 29 inactive | Status is not observed churn or network telemetry | Use status review language, not churn/performance outcomes |
| Fee exposure | 3,282,809 listed fee units on active/partial services; 54,712 on partial-active services | Currency and billing period are unverified | Keep units unverified and avoid revenue/loss claims |
| Public BI artifact | Sanitized star-schema CSVs, candidate DAX and a blueprint are committed; refreshed Desktop report is absent | Interviewer cannot verify a current interactive Power BI report | Build and validate a privacy-reviewed report only after explicit approval for Power BI changes |

### What the audit can and cannot validate

The receipt validates public data structure and aggregate calculations, not the provenance of the private extract or execution of candidate DAX in Power BI Desktop. The screenshot in `images/` is a Python-rendered public-data figure. It is not evidence of a refreshed Power BI report. Old binary/screenshots were quarantined; the public tree cannot prove old Git objects were removed.

### Before and after this review

| Item | Latest committed starting state | This review |
|---|---|---|
| Service and customer counts | 1,280 services and 1,193 grouped keys already documented | Unchanged; independent audit checks both grains |
| Future activation | 810 flagged and excluded by the existing ETL | Unchanged; new receipt and tests verify 810 excluded from validated tenure, leaving 470 rows |
| Quality and status KPIs | Existing Python summary and candidate DAX | New receipt checks 816 review rows, 22 inactive-only grouped keys and listed-fee exposure with explicit units/denominators |
| Automated tests | 5 passing baseline tests | 8 passing tests, including duplicate-key rejection and future-date regression |
| Power BI | Candidate DAX/model guidance, no validated Desktop report | Unchanged; Desktop relationships, measures, filters and visuals remain unverified |

The three strongest findings are the future-date quarantine, the service/customer grain difference, and the separation of status-based fee exposure from actual churn or revenue. This is a stronger **data-modeling and quality** portfolio case, but it does **not yet meet a defensible 4/5 BI-project rating**: the source date meaning and billing units are unresolved, and a current privacy-reviewed Desktop report has not been validated.

### Resume-safe project story

“I modeled a telecom service snapshot and built checks that distinguish 1,280 services from 1,193 grouped customer keys. After obtaining the original workbook, I reconciled the scoped rows on fees, plans and grouping and found 1,275 public activation dates differed from source. I retained the public-data quality flags and stopped tenure/cohort claims pending a documented, privacy-reviewed correction and Power BI refresh.”
