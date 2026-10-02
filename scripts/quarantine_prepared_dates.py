"""Remove unreliable prepared dates without publishing private source dates.

Preserve historical future-date flags as explicit lineage. This operates only
on public tables; it never reads, infers or substitutes original activation dates.
"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

def quarantine(root=ROOT):
    model = root / 'data/powerbi_star_schema'
    fact = pd.read_csv(model / 'fact_customer_service.csv')
    if 'activation_date_withheld_flag' in fact:
        return
    before = root / 'docs/before_date_quarantine_audit.json'
    before.write_text((root / 'docs/public_audit.json').read_text(encoding='utf-8'), encoding='utf-8')
    fact['legacy_prepared_future_activation_flag'] = fact.dq_future_activation_flag
    for column in ['activation_date_key','reported_activation_date_key','valid_tenure_days','valid_tenure_months']:
        fact[column] = pd.Series(pd.NA, index=fact.index, dtype='Int64')
    fact['activation_date_withheld_flag'] = 1
    fact['dq_future_activation_flag'] = 0
    fact['dq_missing_activation_flag'] = 1
    # Withholding is a privacy/fitness decision, not a defect in original dates.
    remaining = ['dq_invalid_fee_flag','dq_connection_count_flag','dq_unknown_plan_period_flag']
    fact['data_quality_flag'] = fact[remaining].any(axis=1).map({True:'review',False:'valid'})
    fact.to_csv(model / 'fact_customer_service.csv',index=False,lineterminator='\n')
    dates = pd.read_csv(model / 'dim_date.csv')
    dates[dates.date_key.isin(fact.snapshot_date_key)].to_csv(model / 'dim_date.csv',index=False,lineterminator='\n')
    (root / 'docs/date_publication_policy.md').write_text('''# Public activation-date policy

The original workbook has zero activation dates after the analyst reference date. The earlier public preparation changed 1,275 dates and introduced 810 future dates; its transformation cause is unresolved. The before receipt preserves these findings.

After author approval, all 1,280 unreliable public activation dates and derived tenures were removed, rather than replaced with confidential row-level dates. The original workbook was not changed. `activation_date_withheld_flag=1` distinguishes deliberate withholding from an original-source missing date. `legacy_prepared_future_activation_flag` retains the 810 historical flags. Current `dq_missing_activation_flag` means unavailable in the public model, not missing in the original workbook. Other review flags remain independent.

The date dimension now contains only the analyst reference date, 12 September 2026. It is not a verified export date. No public tenure/cohort claims are made. Customer, plan, fee, service-status and OLT keys/counts are unchanged. The privacy review permits aggregates and existing sanitized attributes; it does not publish private exact dates, contacts or OLT addresses. Existing sequential keys remain frozen-build labels. Public Git history can retain prior prepared dates.
''',encoding='utf-8')

if __name__ == '__main__':
    quarantine()
