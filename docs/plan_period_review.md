# Listed plan amounts and periods

The author identifies the original customer export as confidential government-platform data and cannot disclose portal, bill or tariff documents. The author confirms that plan amounts should be read with their listed plan periods. Use the provided fields for descriptive analysis, with currency undisclosed and collection/revenue recognition outside scope.

The selected source and public model have matching period counts: 1,188 MONTHLY, six ANNUALLY, seven HALF YEARLY, three QUARTERLY, 14 across the equivalent text labels 13MONTHLY/13 MONTHLY, three 199DAYS, one 97DAYS and 58 missing/unknown. The original-to-public fee comparison matched all 1,280 service rows. This supports period-stratified reporting of the supplied amounts, not a verified billing ledger.

Run `python scripts/analyze_plan_periods.py` to reproduce per-period service counts, listed amounts and active/partial-service listed exposure. An optional `--output docs/plan_period_receipt.json` saves the aggregate receipt. Python and SQLite independently reconcile those totals. The script normalizes text aliases only, never assumes missing periods are monthly and never divides annual/day amounts into claimed revenue.

The stored column name `monthly_fee` is a legacy name for the source FMC value. For nonmonthly source periods, display **listed plan amount** and the period together. Do not combine amounts from different periods into a monthly-revenue headline. The overall listed-fee sum remains an unnormalized exposure proxy.

Source raw rows/contact details and confidential documentation remain private. Native Power BI measures and captions must adopt the same period-aware labels during the approved report phase; they have not been changed here.
