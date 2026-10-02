# Methodology

Grain: one frozen service record, 1,280 rows; 1,193 normalized-label customer groups. Customer identity and actual snapshot date are not independently verified. The configured reference is 2026-09-12.

Source A/D/E map to active/partial_active/inactive as analyst assumptions. Active share uses all service rows in filter context. Status review is partial + inactive. Inactive-only keys have at least one inactive service and no active/partial service; status selection does not remove their other services when classifying the key. OLT and plan context still apply.

Listed exposure sums supplied amounts on active/partial services within a plan period. Mixed-period exposure is blank. Currency, payment, recognition and collections are unavailable. The legacy `monthly_fee` name does not establish monthly revenue. Status index averages weights 1, 0.5, 0; it is not network telemetry.

All precise public activation/tenure values are withheld after source comparison identified 1,275 discrepancies. The historical future flag preserves 810 earlier prepared discrepancies. Current future=0 means no published activation dates, not evidence that all source dates were validated against an actual export. Missing-date=1 means withheld in this public model. Quality-review rows=58 reflects remaining unknown periods, excluding intentional withholding. No tenure/cohort analysis is supported.

Five single-direction relationships connect the service fact to customer, OLT, plan, state and reference-date dimensions. Native measures are in the PBIP `_Measures.tmdl`; the old DAX filename is a reference copy. [Executed Desktop validation](powerbi_validation.md) covers 114 checks, representative interactions and current screenshots. The native MySQL audit and Python/SQLite checks are independently documented; no original private SQL workflow is claimed executed.
