"""Load public CSVs into a task-owned MySQL schema and reconcile headline KPIs.

Requires a MySQL 8 client and user-provided connection arguments. Never reads
private source files or alters an existing schema; schema names must be new.
"""
import argparse, json, subprocess, tempfile
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
def validate(client, connection, schema):
    if not schema.replace('_','').isalnum() or not schema.startswith('portfolio_audit_'):
        raise ValueError('Use a fresh portfolio_audit_ schema')
    model=ROOT/'data/powerbi_star_schema'
    tables={p.stem:pd.read_csv(p) for p in model.glob('*.csv')}
    queries={
      'services':'SELECT COUNT(*) FROM fact_customer_service',
      'customers':'SELECT COUNT(DISTINCT customer_key) FROM fact_customer_service',
      'active':'SELECT COUNT(*) FROM fact_customer_service f JOIN dim_service_state s USING(service_state_key) WHERE s.service_status="active"',
      'withheld':'SELECT SUM(activation_date_withheld_flag) FROM fact_customer_service',
      'legacy_future':'SELECT SUM(legacy_prepared_future_activation_flag) FROM fact_customer_service',
      'unknown_period':'SELECT SUM(dq_unknown_plan_period_flag) FROM fact_customer_service',
      'monthly_exposure':'SELECT SUM(f.monthly_fee) FROM fact_customer_service f JOIN dim_plan p USING(plan_key) JOIN dim_service_state s USING(service_state_key) WHERE p.plan_period="MONTHLY" AND s.service_status IN ("active","partial_active")',
    }
    f=tables['fact_customer_service'];j=f.merge(tables['dim_plan'],on='plan_key',validate='many_to_one').merge(tables['dim_service_state'],on='service_state_key',validate='many_to_one')
    expected={'services':len(f),'customers':f.customer_key.nunique(),'active':int(j.service_status.eq('active').sum()),'withheld':int(f.activation_date_withheld_flag.sum()),'legacy_future':int(f.legacy_prepared_future_activation_flag.sum()),'unknown_period':int(f.dq_unknown_plan_period_flag.sum()),'monthly_exposure':float(j.loc[j.plan_period.eq('MONTHLY') & j.service_status.isin(['active','partial_active']),'monthly_fee'].sum())}
    sql=f'CREATE DATABASE `{schema}`; USE `{schema}`;\n'
    for name,df in tables.items():
        cols=','.join(f'`{c}` '+('DOUBLE' if pd.api.types.is_numeric_dtype(df[c]) else 'TEXT') for c in df)
        sql+=f'CREATE TABLE `{name}` ({cols});\n'
        def cell(v):
            if pd.isna(v):return 'NULL'
            if isinstance(v,(int,float)):return str(v)
            return "'"+str(v).replace('\\','\\\\').replace("'","''")+"'"
        for start in range(0,len(df),250):
            sql+=f'INSERT INTO `{name}` VALUES '+','.join('('+','.join(cell(v) for v in row)+')' for row in df.iloc[start:start+250].itertuples(index=False,name=None))+';\n'
    sql+='SELECT VERSION();\n'+''.join(f'SELECT "{k}", ({q});\n' for k,q in queries.items())
    run=subprocess.run([client,*connection,'--batch','--skip-column-names'],input=sql,text=True,capture_output=True)
    if run.returncode:raise RuntimeError(run.stderr)
    lines=run.stdout.strip().splitlines();actual={k:float(v) for k,v in (l.split('\t') for l in lines[1:])}
    for k,v in expected.items():
        if abs(actual[k]-v)>1e-9:raise ValueError(f'MySQL/Python mismatch for {k}')
    receipt={'engine':'MySQL','version':lines[0],'checks':len(queries),'status':'passed','actual':actual,'limit':'native MySQL checks of these public aggregates; no original private MySQL workflow or Power BI validation implied'}
    (ROOT/'docs/mysql_validation.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    (ROOT/'sql/mysql_kpi_queries.sql').write_text('-- MySQL 8: run against the loaded public model tables.\n'+''.join(f'-- {k}\n{q};\n' for k,q in queries.items()),encoding='utf-8')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--client',required=True);p.add_argument('--schema',required=True);p.add_argument('connection',nargs=argparse.REMAINDER);a=p.parse_args();validate(a.client,a.connection[1:] if a.connection[:1]==['--'] else a.connection,a.schema)
