# Public activation-date policy

The original workbook has zero activation dates after the analyst reference date. The earlier public preparation changed 1,275 dates and introduced 810 future dates; its transformation cause is unresolved. The before receipt preserves these findings.

After author approval, all 1,280 unreliable public activation dates and derived tenures were removed, rather than replaced with confidential row-level dates. The original workbook was not changed. `activation_date_withheld_flag=1` distinguishes deliberate withholding from an original-source missing date. `legacy_prepared_future_activation_flag` retains the 810 historical flags. Current `dq_missing_activation_flag` means unavailable in the public model, not missing in the original workbook. Other review flags remain independent.

The date dimension now contains only the analyst reference date, 12 September 2026. It is not a verified export date. No public tenure/cohort claims are made. Customer, plan, fee, service-status and OLT keys/counts are unchanged. The privacy review permits aggregates and existing sanitized attributes; it does not publish private exact dates, contacts or OLT addresses. Existing sequential keys remain frozen-build labels. Public Git history can retain prior prepared dates.
