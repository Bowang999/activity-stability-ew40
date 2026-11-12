"""Regenerate the cost chart from released ledgers; no empirical backtest."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

ROOT = Path(__file__).resolve().parents[1]


def main():
    book = pd.read_csv(ROOT/'data/derived/books/six__AS.csv.gz')
    metrics = pd.read_csv(ROOT/'data/derived/portfolio_metrics.csv')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':'#19334b',
                         'axes.labelcolor':'#19334b','axes.titlecolor':'#19334b',
                         'axes.spines.top':False,'axes.spines.right':False})
    fig, axes = plt.subplots(2, 2, figsize=(16, 9), gridspec_kw={'height_ratios':[4.5,1.2]})
    fig.subplots_adjust(top=.82, bottom=.05, left=.07, right=.98, wspace=.2, hspace=.25)
    fig.suptitle('Activity Stability EW40 | Six Styles Controlled', fontsize=24, weight='bold', y=.97)
    fig.text(.5,.91,'Local style proxies | Daily rebalance, next-close execution | Already-viewed historical data',ha='center')
    for col, (period, lo, hi, start) in enumerate([
        ('research','2012-01-01','2024-12-31','2012-03-06'),
        ('later','2025-01-01','2026-10-20','2024-12-31')]):
        ax = axes[0,col]; rows = []
        for cost, color in [(0,'#236da1'),(10,'#188c7a'),(20,'#d48735')]:
            f=book[book.cost_bps.eq(cost)&book.date.between(lo,hi)].sort_values('date')
            nav=np.r_[1.,np.cumprod(1+f.net_return)]
            ax.plot(pd.to_datetime([start]+f.date.tolist()),nav,label=f'{cost} bp',color=color,lw=2.)
            z=metrics[metrics.model.eq('six__AS')&metrics.period.eq(period)&metrics.cost_bps.eq(cost)].iloc[0]
            rows.append([f'{cost} bp',f'{z.annual_return_pct:.2f}%',f'{z.sharpe:.2f}',f'{z.one_way_turnover_pct:.2f}%',f'{z.max_drawdown_pct:.2f}%'])
        ax.set(title='2012-2024' if period=='research' else '2025-2026.10.20',ylabel='Cumulative net value',xlabel='Year')
        ax.legend(frameon=False,ncol=3);ax.grid(alpha=.15)
        locator=mdates.AutoDateLocator(minticks=3,maxticks=5)
        ax.xaxis.set_major_locator(locator);ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(locator))
        tx=axes[1,col];tx.axis('off')
        table=tx.table(cellText=rows,colLabels=['Cost','CAGR','Sharpe','TO (1w)','MDD'],loc='center',cellLoc='center')
        table.auto_set_font_size(False);table.set_fontsize(11);table.scale(1,1.7)
        for (r,c),cell in table.get_celld().items():
            cell.set_edgecolor('#dae3eb');cell.set_facecolor('#edf3f7' if r==0 else 'white')
    out=ROOT/'results/local';out.mkdir(parents=True,exist_ok=True)
    p=out/'six_styles_costs.png';fig.savefig(p,dpi=160,facecolor='white');plt.close(fig)
    print(p)


if __name__=='__main__':main()
