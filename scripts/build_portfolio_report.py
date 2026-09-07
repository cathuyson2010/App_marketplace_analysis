"""Regenerate the portfolio dashboard and analyst-ready category extracts."""
from pathlib import Path
import json
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
df = pd.read_csv(ROOT / 'data/googleplaystore_cleaned.csv')
assert len(df) == 8196 and df['app'].is_unique
assert df['category'].nunique() == 33
out = ROOT / 'reports'
out.mkdir(exist_ok=True)
summary = df.groupby('category').agg(
    app_count=('app', 'size'), rated_apps=('rating', 'count'),
    avg_rating=('rating', 'mean'), total_installs=('installs', 'sum'),
    mean_installs=('installs', 'mean'), median_installs=('installs', 'median'))
top3 = df.sort_values('installs', ascending=False).groupby('category').head(3)
summary['top3_share_pct'] = top3.groupby('category')['installs'].sum() / summary['total_installs'] * 100
summary = summary.sort_values('total_installs', ascending=False)
summary.to_csv(out / 'category_summary.csv')
game = df[df['category'].eq('GAME')]
paid = game.groupby('type').agg(app_count=('app','size'), avg_rating=('rating','mean'),
    total_installs=('installs','sum'), median_installs=('installs','median'))
paid.to_csv(out / 'game_free_paid.csv')
game.assign(primary_genre=game['genres'].str.split(';').str[0]).groupby('primary_genre').agg(
    app_count=('app','size'), avg_rating=('rating','mean'), median_installs=('installs','median')
).to_csv(out / 'game_genres.csv')
plt.rcParams.update({'font.family':'DejaVu Sans', 'font.size':10,
    'axes.spines.top':False, 'axes.spines.right':False, 'axes.titleweight':'bold'})
fig, axes = plt.subplots(2,2,figsize=(16,10))
fig.patch.set_facecolor('#f5f7fb')
fig.suptitle('APP MARKETPLACE | CATEGORY OPPORTUNITY', x=.07, ha='left', y=.985,
             fontsize=23, weight='bold', color='#102c46')
fig.text(.07,.94,'8,196 rated apps   /   33 categories   /   Python + MySQL reconciled',
         fontsize=13, color='#41566b')
top = summary.head(8).iloc[::-1]
axes[0,0].barh(top.index,top.total_installs/1e9,color='#277b92')
axes[0,0].set(title='01 / GAME leads observed installs', xlabel='Reported install lower bounds (billions)')
focus = summary.loc[['GAME','COMMUNICATION','TOOLS','EDUCATION','PERSONALIZATION']].iloc[::-1]
y = range(len(focus))
axes[0,1].barh([i-.17 for i in y],focus.mean_installs,height=.32,label='Mean',color='#277b92')
axes[0,1].barh([i+.17 for i in y],focus.median_installs,height=.32,label='Median',color='#da9853')
axes[0,1].set_yticks(list(y),focus.index)
axes[0,1].xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x/1e6:g}M'))
axes[0,1].set(title='02 / Typical adoption differs from the average',xlabel='Reported installs per app')
axes[0,1].legend(frameon=False)
axes[1,0].barh(focus.index,focus.top3_share_pct,color='#526c99')
axes[1,0].set(title='03 / Concentration varies by category',xlabel='Top 3 apps: share of category installs (%)',xlim=(0,100))
for i,val in enumerate(focus.top3_share_pct):
    axes[1,0].text(val+1,i,f'{val:.1f}%',va='center')
rates = summary.query('rated_apps >= 100').sort_values('avg_rating').tail(8)
axes[1,1].scatter(rates.avg_rating,rates.index,s=70,color='#277b92')
axes[1,1].set(title='04 / Ratings inform a research shortlist',xlabel='Mean rating (minimum 100 rated apps)',xlim=(0,5))
for i,val in enumerate(rates.avg_rating):
    axes[1,1].text(val+.05,i,f'{val:.2f}',va='center',fontsize=9)
for ax in axes.flat:
    ax.grid(axis='x',alpha=.15)
    ax.set_axisbelow(True)
    ax.set_facecolor('white')
fig.text(.07,.035,'Scope: cleaned rated-app snapshot. Installs are cumulative buckets; no revenue, growth or startup-success estimates.',
         fontsize=10,color='#41566b')
fig.subplots_adjust(left=.16,right=.97,top=.86,bottom=.12,wspace=.52,hspace=.40)
fig.savefig(ROOT/'assets/portfolio_dashboard.png',dpi=160,facecolor=fig.get_facecolor())
plt.close(fig)
print(summary.loc[['GAME','COMMUNICATION','EDUCATION','PERSONALIZATION']].round(3).to_json(orient='index'))
print('Generated dashboard and three CSV extracts.')
