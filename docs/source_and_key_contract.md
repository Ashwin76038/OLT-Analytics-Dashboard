# Source, grain, privacy and future-snapshot contract

## What the committed extract proves

The public model contains one row per **service in one model snapshot configured for 12 September 2026**. It has 1,280 service rows, 1,193 build-scoped grouped customer keys and 12 OLT groups. These are not independently verified people, cancellations or physical network measurements. `scripts/audit_public.py` reproduces the aggregate evidence without reading the private source.

The published sample **is present in this repository**: six CSVs under `data/powerbi_star_schema/` (the 1,280-row service fact and five dimensions), plus a 12-row OLT anomaly output. The audit and tests read those committed files. The project author supplied the original customer workbook privately on 1 October 2026; it is intentionally not distributed. See [source reconciliation](source_workbook_review.md).

The author identifies the workbook as a confidential government-platform export and confirms that plan amounts relate to the listed plan periods. Portal, bill and tariff documents remain confidential; they will not be requested or published. Currency, actual export date, status-code meanings and an independent identity registry are undisclosed. Use author-attested field meanings and clearly stated assumptions for a scoped descriptive project. The optional builder consumes a prepared private `customers.csv`; the original-to-prepared transformation remains undocumented, so a public clone cannot reproduce a complete original-to-dashboard pipeline.

## Activation-date decision

The author confirms that Activation Date means internet plan/service activation. Explicit day-first parsing of the original workbook yields dates from 1999-02-15 through 2026-08-29 and zero dates after the configured 2026-09-12 cutoff. In the earlier prepared build, 810/1,280 values were later than that cutoff, reaching 2028-11-30; 1,275 of 1,280 earlier prepared dates differed from source under corroborated row-order comparison. The transformation responsible remains unresolved. The cutoff is model configuration, not a verified source snapshot date.

All 1,280 public activation and tenure values are now withheld. The historical future flag preserves the 810 earlier prepared discrepancies without retaining their dates. Current missing-date flags mean public withholding, not missing original dates. Source dates were not silently substituted; aggregate historical and current receipts document the change. No public cohort or tenure claim is supported.

## Keys and privacy

The current ETL normalizes prepared `customer_clean` and gives each distinct normalized label a sequential `customer_key`. On the supplied original workbook, trim + lowercase + internal-whitespace collapse reproduces all 1,193 groups and their current sequential keys in the filtered row order. This corroborates the frozen grouping but does not verify customer identity. It can merge people with the same label, and the numbering can change when source order changes. Never append independently generated snapshots by joining these keys.

For future snapshots, require a source-owner-approved stable service identifier and stable customer identifier with documented uniqueness, lifecycle and collision rules. In a private controlled environment, derive public pseudonyms with an HMAC using a secret key held outside Git, version the key and mapping process, and test that the same source identity maps consistently across snapshots. **Do not HMAC a name and call it a verified identity:** name collisions and changes remain. Do not publish the source identifiers, secret, lookup map, contact details or raw screenshots. If no stable source IDs are available, keep snapshots separate and do not report customer transitions or churn.

## Definitions that must remain separate

- **Service records:** count of fact rows. **Customer keys:** distinct build-scoped groups.
- **Inactive-only customer key:** no active/partial service and at least one inactive service in this snapshot. It is not a cancellation event.
- **Listed fee exposure:** supplied amounts on active/partial rows, reported with their listed plan periods. Period meanings are author-attested; currency is undisclosed and collections/recognized revenue are unavailable. See [period review](plan_period_review.md). No MRR is established.
- **Service-state index:** mean of analyst-defined status weights 1, 0.5 and 0. It is not throughput, downtime or network utilization.
- **High-risk status:** a service-state review label, not a churn probability.

## Evidence needed before stronger claims

The source comparison is complete at aggregate level. Label the analysis reference date and status mappings as assumptions where source details remain confidential. Describe plan amounts within supplied periods, with currency undisclosed. Future longitudinal work needs stable approved IDs; observed churn or physical-network claims would additionally need authentic outcomes/telemetry. Those sources are outside the current scoped project and will not be requested from confidential portals.
