"""Independent audit of all released main/incremental aggregate statistics."""
import sys, json, hashlib, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'src'))
import numpy as np
import pandas as pd
from activity_stability import performance, hac_mean, adjust_p

D = ROOT/'data/derived'
PERIODS = {'research': ('2010-01-01','2024-12-31'), 'later': ('2025-01-01','2026-10-20')}


def equal(a, b, label):
    try:
        probability = (isinstance(label, str) and 'BY' in label) or (isinstance(label, tuple) and label[-1] == 'p_two_sided')
        np.testing.assert_allclose(a, b, atol=1e-300 if probability else 3e-10, rtol=3e-7, equal_nan=True)
    except AssertionError as exc:
        raise AssertionError(label) from exc


def run():
    metrics = pd.read_csv(D/'portfolio_metrics.csv')
    checked = 0
    for model, rows in metrics.groupby('model'):
        book = pd.read_csv(D/'books'/f'{model}.csv.gz')
        for row in rows.itertuples():
            lo, hi = PERIODS[row.period]
            f = book[book.cost_bps.eq(row.cost_bps) & book.date.between(lo, hi)].sort_values('date')
            assert not f.date.duplicated().any()
            calc = performance(f.net_return, f.turnover)
            for key, value in calc.items():
                equal(value, getattr(row, key), (model, row.period, row.cost_bps, key))
            checked += 1
    assert checked == 108
    old_ic = pd.read_csv(D/'original_ic_family540_q552.csv')
    old_fmb = pd.read_csv(D/'original_fmb12_q552.csv')
    new = pd.read_csv(D/'incremental_all_tests_p_q.csv')
    old = pd.concat([old_ic, old_fmb], ignore_index=True)
    assert len(old) == 552 and len(new) == 372
    equal(adjust_p(old.p_two_sided), old.q_BY_combined552, 'BY552')
    equal(adjust_p(new.p_two_sided), new.q_BY_new372, 'BY372')
    equal(adjust_p(pd.concat([old.p_two_sided, new.p_two_sided]))[552:],
          new.q_BY_old552_plus_new372, 'BY924 new rows')
    ic = pd.read_csv(D/'incremental_daily_ic.csv.gz')
    calendar = np.sort(ic.date.unique())
    ic_count = 0
    for row in new[new.kind.eq('IC')].itertuples():
        lo, hi = PERIODS[row.period]
        f = ic[ic.model.eq(row.model) & ic.horizon.eq(row.horizon) & ic.date.between(lo, hi)]
        last = np.searchsorted(calendar, hi, side='right')-1
        f = f[np.searchsorted(calendar, f.date.to_numpy())+1+int(row.horizon) <= last]
        calc = hac_mean(f[row.metric], int(row.lag))
        assert calc['n'] == row.n
        for key in ['mean', 'se', 't', 'p_two_sided']:
            equal(calc[key], getattr(row, key), ('IC', row.model, row.period, row.horizon, row.metric, key))
        ic_count += 1
    assert ic_count == 216
    coeff = pd.read_csv(D/'incremental_daily_fmb.csv.gz')
    count = 0
    for row in new[new.kind.eq('FMB')].itertuples():
        stage, regression = row.model.split('__')
        lo, hi = PERIODS[row.period]
        f = coeff[coeff.stage.eq(stage) & coeff.regression.eq(regression) &
                  coeff.predictor.eq(row.predictor) & coeff.horizon.eq(row.horizon) & coeff.date.between(lo, hi)]
        last = np.searchsorted(calendar, hi, side='right')-1
        f = f[np.searchsorted(calendar, f.date.to_numpy())+1+int(row.horizon) <= last]
        calc = hac_mean(f.coefficient, int(row.lag))
        assert calc['n'] == row.n
        for key in ['mean', 'se', 't', 'p_two_sided']:
            equal(calc[key], getattr(row, key), ('FMB', row.model, row.period, row.horizon, row.predictor, key))
        count += 1
    assert count == 84
    original_coeff = pd.read_csv(D/'original_daily_fmb.csv.gz')
    original_count = 0
    for row in old_fmb.itertuples():
        lo, hi = PERIODS[row.period]
        f = original_coeff[original_coeff.model.eq(row.model) & original_coeff.horizon.eq(row.horizon) & original_coeff.date.between(lo, hi)]
        last = np.searchsorted(calendar, hi, side='right')-1
        f = f[np.searchsorted(calendar, f.date.to_numpy())+1+int(row.horizon) <= last]
        calc = hac_mean(f.coefficient, int(row.lag))
        assert calc['n'] == row.n
        for key in ['mean', 'se', 't', 'p_two_sided']:
            equal(calc[key], getattr(row, key), ('original FMB', row.model, row.period, row.horizon, key))
        original_count += 1
    assert original_count == 12
    manifest = json.loads((ROOT/'reports/audit/source_manifest.json').read_text('utf-8'))
    for item in manifest:
        p = ROOT/item['file']
        assert hashlib.sha256(p.read_bytes()).hexdigest() == item['sha256'], item['file']
    broken = []
    for p in ROOT.rglob('*.md'):
        for link in re.findall(r'\]\(([^)]+)\)', p.read_text('utf-8')):
            if '://' in link or link.startswith('#'):
                continue
            if not (p.parent/link.split('#')[0]).exists():
                broken.append((str(p.relative_to(ROOT)), link))
    assert not broken, broken
    for p in (ROOT/'notebooks').glob('*.ipynb'):
        nb = json.loads(p.read_text('utf-8'))
        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                compile(''.join(cell['source']), str(p), 'exec')
    result = dict(portfolio_summaries=checked, IC_HAC_statistics=ic_count,
                  FMB_HAC_statistics=count, original_FMB_HAC_statistics=original_count, BY552=True, BY372=True, combinedBY924=True,
                  manifest_files=len(manifest), markdown_links_valid=True,
                  notebook_cells_compile=True, full_market_backtest_replayed=False)
    print(json.dumps(result, indent=2))
    (ROOT/'reports/audit/release_checks.json').write_text(json.dumps(result, indent=2)+'\n', 'utf-8')


if __name__ == '__main__':
    run()
