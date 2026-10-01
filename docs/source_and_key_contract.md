# Source, grain, privacy and future-snapshot contract

## What the committed extract proves

The public model contains one row per **service in one model snapshot configured for 12 September 2026**. It has 1,280 service rows, 1,193 build-scoped grouped customer keys and 12 OLT groups. These are not independently verified people, cancellations or physical network measurements. `scripts/audit_public.py` reproduces the aggregate evidence without reading the private source.

The published sample **is present in this repository**: six CSVs under `data/powerbi_star_schema/` (the 1,280-row service fact and five dimensions), plus a 12-row OLT anomaly output. The audit and tests read those committed files. The project author supplied the original customer workbook privately on 1 October 2026; it is intentionally not distributed. See [source reconciliation](source_workbook_review.md).

The workbook is author-supplied source evidence. Its collection process, permissions, currency, billing period and identity registry remain **independently unverified**. The optional `scripts/build_powerbi_star_schema.py` expects an ignored prepared `customers.csv`; the original-workbook-to-prepared-CSV transformation is not documented. A reviewer can reproduce the public aggregate audit and tests, but cannot independently regenerate the six CSVs from the original workbook. Do not describe this as a fully reproducible raw-to-dashboard pipeline.

## Activation-date decision

The author confirms that Activation Date means internet plan/service activation. Explicit day-first parsing of the original workbook yields dates from 1999-02-15 through 2026-08-29 and zero dates after the configured 2026-09-12 cutoff. In contrast, 810/1,280 public values are later than that cutoff, reaching 2028-11-30; 1,275 of 1,280 public dates differ from source under corroborated row-order comparison. The transformation responsible remains unresolved. The cutoff is model configuration, not a verified source snapshot date.

The current model retains public dates in `reported_activation_date_key`, sets `dq_future_activation_flag=1`, and leaves validated dates/tenure null for future rows. Keep that quarantine until a privacy-reviewed source-date restoration and approved rebuild. Do not silently replace dates, infer renewal/expiry meanings, or use the remaining public dates for source-backed cohort claims. All public activation values need reconciliation, including the 465 nonfuture values that differ from source.

## Keys and privacy

The current ETL normalizes prepared `customer_clean` and gives each distinct normalized label a sequential `customer_key`. On the supplied original workbook, trim + lowercase + internal-whitespace collapse reproduces all 1,193 groups and their current sequential keys in the filtered row order. This corroborates the frozen grouping but does not verify customer identity. It can merge people with the same label, and the numbering can change when source order changes. Never append independently generated snapshots by joining these keys.

For future snapshots, require a source-owner-approved stable service identifier and stable customer identifier with documented uniqueness, lifecycle and collision rules. In a private controlled environment, derive public pseudonyms with an HMAC using a secret key held outside Git, version the key and mapping process, and test that the same source identity maps consistently across snapshots. **Do not HMAC a name and call it a verified identity:** name collisions and changes remain. Do not publish the source identifiers, secret, lookup map, contact details or raw screenshots. If no stable source IDs are available, keep snapshots separate and do not report customer transitions or churn.

## Definitions that must remain separate

- **Service records:** count of fact rows. **Customer keys:** distinct build-scoped groups.
- **Inactive-only customer key:** no active/partial service and at least one inactive service in this snapshot. It is not a cancellation event.
- **Listed fee exposure:** sum of supplied fees on active/partial service rows. Currency, period, collections and recognized revenue are unverified; do not call it MRR.
- **Service-state index:** mean of analyst-defined status weights 1, 0.5 and 0. It is not throughput, downtime or network utilization.
- **High-risk status:** a service-state review label, not a churn probability.

## Evidence needed before stronger claims

Confirm the actual source snapshot date, source-status definitions, stable approved IDs and billing-period/currency contract. Reconcile public activation dates with the supplied original workbook. Obtain dated cancellation events for churn and interval network telemetry for utilization if those claims are intended. Record source vintage, permissions and privacy review without committing confidential extracts.
