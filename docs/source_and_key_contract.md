# Source, grain, privacy and future-snapshot contract

## What the committed extract proves

The public model contains one row per **service in one 12 September 2026 snapshot**. It has 1,280 service rows, 1,193 build-scoped grouped customer keys and 12 OLT groups. These are not independently verified people, cancellations or physical network measurements. `scripts/audit_public.py` reproduces the aggregate evidence without reading the private source.

The published sample **is present in this repository**: six CSVs under `data/powerbi_star_schema/` (the 1,280-row service fact and five dimensions), plus a 12-row OLT anomaly output. The audit and tests read those committed files. The separate original customer extract used to build the public tables is not present.

The source of the original operational-style extract, its collection process, permissions, currency, billing period and identity registry are **not verified from this repository**. The optional `scripts/build_powerbi_star_schema.py` expects an ignored private `customers.csv`; that source is not distributed. A reviewer can reproduce the public aggregate audit and tests, but cannot independently regenerate the six CSVs from the private extract. Do not describe this as a fully reproducible raw-to-dashboard pipeline.

## Activation-date decision

The supplied date field is called `activation date`, but 810/1,280 values are later than the 2026-09-12 snapshot, reaching 2028-11-30. Its actual source meaning cannot be resolved from the public files. The ETL retains the value only in `reported_activation_date_key`, sets `dq_future_activation_flag=1`, and leaves `activation_date_key` and tenure null. Do not reinterpret it as an expiry, renewal or corrected activation date without source-system confirmation. Until then, exclude these rows from tenure/cohort claims.

## Keys and privacy

The current ETL normalizes `customer_clean` and gives each distinct normalized label a sequential `customer_key`. That is acceptable for grouping within this frozen build only. It can merge people with the same label, and the numbering can change when the source order changes. Never append independently generated snapshots by joining these keys.

For future snapshots, require a source-owner-approved stable service identifier and stable customer identifier with documented uniqueness, lifecycle and collision rules. In a private controlled environment, derive public pseudonyms with an HMAC using a secret key held outside Git, version the key and mapping process, and test that the same source identity maps consistently across snapshots. **Do not HMAC a name and call it a verified identity:** name collisions and changes remain. Do not publish the source identifiers, secret, lookup map, contact details or raw screenshots. If no stable source IDs are available, keep snapshots separate and do not report customer transitions or churn.

## Definitions that must remain separate

- **Service records:** count of fact rows. **Customer keys:** distinct build-scoped groups.
- **Inactive-only customer key:** no active/partial service and at least one inactive service in this snapshot. It is not a cancellation event.
- **Listed fee exposure:** sum of supplied fees on active/partial service rows. Currency, period, collections and recognized revenue are unverified; do not call it MRR.
- **Service-state index:** mean of analyst-defined status weights 1, 0.5 and 0. It is not throughput, downtime or network utilization.
- **High-risk status:** a service-state review label, not a churn probability.

## Evidence needed before stronger claims

Obtain a source-owner definition of activation and snapshot dates; stable approved IDs; a billing-period/currency contract; dated cancellation events for churn; and interval network telemetry for utilization. Record source vintage, permissions and privacy review without committing confidential extracts. Only then consider longitudinal, revenue or network-performance claims.
