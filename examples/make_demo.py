"""Synthetic demonstration only: no empirical return claim or trading engine."""
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
import numpy as np
import pandas as pd
from activity_stability import activity_stability, process_cross_section

rng=np.random.default_rng(20261112)
amount=np.exp(rng.normal(12,.35,(150,120)))
cap=np.exp(rng.normal(22,1,120));industry=np.repeat(np.arange(6),20)
raw=activity_stability(amount)
score=process_cross_section(raw[-1],cap,industry)
out=ROOT/'results/local';out.mkdir(parents=True,exist_ok=True)
pd.DataFrame({'synthetic_security':np.arange(120),'raw_AS':raw[-1],'negative_processed_score':score}).to_csv(out/'synthetic_factor.csv',index=False)
print('Synthetic estimator demo saved. These values are not empirical backtest results.')
