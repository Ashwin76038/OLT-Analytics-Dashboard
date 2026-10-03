"""Generate independent pandas expectations for native Power BI DAX checks."""
import json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]

def build():
    d=ROOT/'data/powerbi_star_schema'
    f=pd.read_csv(d/'fact_customer_service.csv').merge(pd.read_csv(d/'dim_plan.csv'),on='plan_key',validate='many_to_one').merge(pd.read_csv(d/'dim_service_state.csv'),on='service_state_key',validate='many_to_one')
    cases=[]
    contexts=[('All',{}),('OLT 1',{'olt_key':'OLT_0001'}),('Monthly',{'plan_period':'MONTHLY'}),('Annual',{'plan_period':'ANNUALLY'}),('Inactive',{'service_status':'inactive'}),('OLT 1 Monthly',{'olt_key':'OLT_0001','plan_period':'MONTHLY'})]
    for label,filters in contexts:
        selected=f.copy(); no_state=f.copy()
        predicates=[]
        for column,value in filters.items():
            selected=selected[selected[column].eq(value)]
            if column!='service_status':no_state=no_state[no_state[column].eq(value)]
            table={'olt_key':'dim_olt','plan_period':'dim_plan','service_status':'dim_service_state'}[column]
            predicates.append(f'TREATAS({{{json.dumps(value)}}},{table}[{column}])')
        keys=set(selected.customer_key)
        flags=no_state[no_state.customer_key.isin(keys)].groupby('customer_key').service_status.agg(lambda s:set(s))
        active=selected.service_status.eq('active');partial=selected.service_status.eq('partial_active');inactive=selected.service_status.eq('inactive')
        exposure=selected[selected.service_status.isin(['active','partial_active'])]
        monthly=exposure[exposure.plan_period.eq('MONTHLY')]
        values={
          'Service Records':len(selected),'Customer Keys':selected.customer_key.nunique(),'OLT Groups':selected.olt_key.nunique(),
          'Active Services':int(active.sum()),'Partial Services':int(partial.sum()),'Inactive Services':int(inactive.sum()),
          'Active Service Share':float(active.mean()),'Status Review Services':int((partial|inactive).sum()),'Status Review Share':float((partial|inactive).mean()),
          'Inactive Only Keys':sum(v=={'inactive'} for v in flags),
          'Monthly Listed Exposure':float(monthly.monthly_fee.sum()) if len(monthly) else None,
          'Listed Exposure In Period':float(exposure.monthly_fee.sum()) if selected.plan_period.nunique()==1 and len(exposure) else None,
          'Service State Index':float(selected.olt_performance_weight.mean()),'Date Withheld Records':int(selected.activation_date_withheld_flag.sum()),
          'Legacy Future Dates':int(selected.legacy_prepared_future_activation_flag.sum()),'Current Future Dates':int(selected.dq_future_activation_flag.sum()),
          'Unknown Period Records':int(selected.dq_unknown_plan_period_flag.sum()),'Quality Review Records':int(selected.data_quality_flag.eq('review').sum()),
          'Valid Tenure Records':None if selected.valid_tenure_days.notna().sum()==0 else int(selected.valid_tenure_days.notna().sum()),
        }
        for name,value in values.items():
            expression='['+name+']'
            if predicates:expression='CALCULATE('+expression+','+','.join(predicates)+')'
            cases.append({'check':label+' / '+name,'expression':expression,'expected':value})
    rows=[]
    for c in cases:
        e=c['expression'];v=c['expected']
        condition=f'ISBLANK({e})' if v is None else f'NOT ISBLANK({e}) && ABS({e}-({v}))<0.0000001'
        rows.append('ROW("Check",'+json.dumps(c['check'])+',"Passed",'+condition+')')
    query='DEFINE\n VAR Checks = UNION(\n'+',\n'.join(rows)+'\n)\nEVALUATE ROW("Checks",COUNTROWS(Checks),"Passed",COUNTROWS(FILTER(Checks,[Passed])),"Failures",CONCATENATEX(FILTER(Checks,NOT [Passed]),[Check],"; "))\n'
    (ROOT/'docs/validate_measures.dax').write_text(query,encoding='utf-8')
    (ROOT/'docs/dax_validation_cases.json').write_text(json.dumps(cases,indent=2)+'\n',encoding='utf-8')
    print(f'Generated {len(cases)} native DAX checks; not executed by this script.')
if __name__=='__main__':build()
