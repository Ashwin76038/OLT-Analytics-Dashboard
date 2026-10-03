# Portfolio readiness review

**Assessment: 4/5 for a scoped descriptive service-status BI project.** This is an evidence-based portfolio assessment, not employer certification. The rating does not apply to churn prediction or network engineering.

## Changed-file groups

- Public fact/date CSVs and quarantine script: withhold all unreliable precise dates and tenure, preserve 810 historical flags and unchanged service/status/fee totals.
- Source comparison, audit and tests: distinguish original-source evidence, historical defects and current withholding; reproduce the public checks.
- `dashboard/OLT_Service_Project/`: three-page editable report, sanitized input copies, five relationships and 19 explicit measures.
- DAX expected-case generator, query and native screenshots: 114/114 Desktop checks, all pages rendered, OLT slicer/reset tested.
- MySQL validator, queries and receipt: seven native MySQL checks against independent Python totals.
- README, dictionary, methodology, source/key/date policies and refresh guide: publish scope, limitations and reproducible instructions.

## Three strongest findings

1. 1,280 service rows represent 1,193 grouped labels: customer and service denominators differ.
2. 70 service records need status review (41 partial, 29 inactive); 94.53% are active. This guides verification rather than asserting churn.
3. Original-source reconciliation overturned the prepared-date story: 1,275 disagreements, with 810 earlier future flags versus zero source dates beyond the assumed reference. Withholding prevents unsupported tenure claims.

## Interview story

“I built a service-status dashboard from a sanitized ISP extract. I separated service and customer grains, compared listed amounts within billing periods, and traced a major date-quality discrepancy back to prepared data. I withheld unreliable public dates, documented stable-key requirements, and reconciled Power BI measures across filter contexts with Python and native MySQL. The result supports status and data-quality review; I do not claim real churn, revenue or utilization.”

## Before / after and limitations

See `public_quality_review.md` for numeric before/after evidence and `powerbi_validation.md` for executed checks. The former candidate report is now refreshed, saved and visually reviewed in Desktop. Missing confidential export/status/currency definitions remain documented assumptions; exact dates stay private. Original extraction and transformation are not fully reproducible publicly. Future snapshots require approved stable IDs and controlled pseudonymization. No measured business impact is claimed.

## Public reproduction check

On 3 October 2026, five reproduction commands passed from a Git archive containing only tracked files, including all 15 unit tests. No ignored private workbook or Desktop cache was available. See `clean_clone_validation.json`; installed Python dependencies were reused.
