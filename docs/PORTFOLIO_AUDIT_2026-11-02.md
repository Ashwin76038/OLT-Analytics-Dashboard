# Portfolio verification

Status: existing analytics preserved; automated regression workflow added.

The fresh public checkout passed all 15 Python tests on 29 October 2026.
Independent SQLite/pandas reconciliation retained 1,280 services, 1,193
normalized label groups, 1,210 active, 41 partial-active and 29 inactive
services. All 1,280 activation dates remain withheld. The dated aggregate
receipt is `audit_2026-10-29.json`.

The added GitHub workflow runs tests, the public audit, plan-period
reconciliation and DAX-query generation on pushes and pull requests. These
commands do not execute Power BI or MySQL. Native Desktop/MySQL receipts
remain historical evidence, not results of this audit. CI execution must be
checked after publication.

No calculation rewrite or dataset expansion was needed. Historical objects
were inventoried for sensitive filenames; this is not a complete binary or
secret scan. Earlier private-source artifacts may remain in history and
require a separate owner-reviewed remediation, without an automatic rewrite.

Readiness: 8/10 for a scoped service-status BI portfolio. Strong reconciliation
and native evidence; unresolved original extraction provenance, non-stable
keys and unavailable operational history limit broader claims.

Acceptance: tests and audits pass from the public clone, CI runs successfully,
and a relocated PBIP is configured and refreshed before sharing its binary.
