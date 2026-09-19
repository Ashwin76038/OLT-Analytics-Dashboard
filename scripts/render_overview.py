"""Render a static portfolio figure directly from public tables."""
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[1]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold'})
fig,(a,b)=plt.subplots(1,2,figsize=(14,6),gridspec_kw={'width_ratios':[1,1.4]})
f=pd.read_csv(ROOT/'data/powerbi_star_schema/fact_customer_service.csv')
s=pd.read_csv(ROOT/'data/powerbi_star_schema/dim_service_state.csv')
d=f.merge(s,on='service_state_key',validate='many_to_one')
counts=d.service_status.value_counts().reindex(['active','partial_active','inactive'])
bars=a.barh(['Active','Partial-active','Inactive'],counts.values,color=['#2463a0','#b57926','#64748b'])
a.invert_yaxis();a.set_xlim(0,1400);a.set_xlabel('Service records');a.set_title('Service status | 1,280 records',loc='left',pad=16)
a.bar_label(bars,labels=[f'{v:,} ({v/len(d):.1%})' for v in counts],padding=6,fontsize=10)
quality=pd.Series({'Future activation date':int(f.dq_future_activation_flag.sum()),'Usable activation date':int(f.activation_date_key.notna().sum())})
bars=b.barh(list(quality.index),quality.values,color=['#b57926','#2463a0']);b.invert_yaxis();b.set_xlim(0,1000);b.bar_label(bars,padding=6);b.set_xlabel('Service records');b.set_title('Activation-date coverage',loc='left',pad=16)
fig.suptitle('Telecom service snapshot',x=.06,ha='left',fontsize=23,fontweight='bold')
fig.text(.06,.885,'1,193 customer keys  |  12 OLTs  |  supplied snapshot: 12 September 2026',fontsize=12,color='#475569')
fig.text(.06,.065,'Source: public fact/dimension CSVs. Customer keys group source labels; they are not independently verified people.',fontsize=10,color='#475569')
fig.text(.06,.03,'Status is not historical churn. Python evidence figure; Power BI report refresh remains pending.',fontsize=10,color='#475569')
fig.subplots_adjust(left=.12,right=.96,bottom=.22,top=.76,wspace=.8)
(ROOT/'images').mkdir(exist_ok=True);fig.savefig(ROOT/'images/01-service-overview.png',dpi=150,facecolor='white')
