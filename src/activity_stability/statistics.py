"""Statistics used to audit released aggregate series, not a trading engine."""
from math import erfc, sqrt
import numpy as np


def hac_mean(values, lag=63):
    """Bartlett/Newey-West mean uncertainty; two-sided asymptotic normal p.

    Nonfinite observations are removed before computing consecutive lags,
    matching the archived convention. CI is unadjusted for multiplicity.
    """
    if not isinstance(lag, (int, np.integer)) or lag < 0:
        raise ValueError("lag must be a nonnegative integer")
    a = np.asarray(values, float); a = a[np.isfinite(a)]; n = len(a)
    if n < 2:
        raise ValueError("At least two finite observations required")
    mean = a.mean(); z = a - mean; variance = z @ z / n
    for h in range(1, min(lag, n-1)+1):
        variance += 2 * (1-h/(lag+1)) * (z[h:] @ z[:-h] / n)
    se = sqrt(max(variance, 0.) / n)
    t = mean / se if se > 0 else float("nan")
    return dict(n=n, mean=float(mean), se=se, t=t, p_two_sided=erfc(abs(t)/sqrt(2)),
                CI95_low=float(mean-1.96*se), CI95_high=float(mean+1.96*se), lag=lag)


def adjust_p(pvalues, method="BY"):
    """BH/BY adjusted p on EXACTLY the supplied complete test family."""
    p = np.asarray(pvalues, float)
    if p.ndim != 1 or not len(p) or not np.isfinite(p).all() or ((p < 0) | (p > 1)).any():
        raise ValueError("Expected a nonempty vector of finite p values in [0, 1]")
    method = method.upper()
    if method not in ("BH", "BY"):
        raise ValueError("method must be BH or BY")
    m = len(p); order = np.argsort(p)
    factor = np.sum(1./np.arange(1, m+1)) if method == "BY" else 1.
    scaled = p[order] * m * factor / np.arange(1, m+1)
    out = np.empty(m); out[order] = np.minimum(1., np.minimum.accumulate(scaled[::-1])[::-1])
    return out


def performance(returns, bilateral_turnover=None):
    """252-session compounded CAGR, rf=0 Sharpe, MDD including initial NAV1."""
    r = np.asarray(returns, float)
    if r.ndim != 1 or len(r) < 2 or not np.isfinite(r).all() or (r <= -1).any():
        raise ValueError("Expected at least two finite returns greater than -1")
    nav = np.r_[1., np.cumprod(1+r)]
    sd = r.std(ddof=1)
    out = dict(annual_return_pct=float(np.expm1(np.log1p(r).mean()*252)*100),
               sharpe=float(sqrt(252)*r.mean()/sd) if sd > 0 else float("nan"),
               max_drawdown_pct=float(-np.min(nav/np.maximum.accumulate(nav)-1)*100))
    if bilateral_turnover is not None:
        turn = np.asarray(bilateral_turnover, float)
        if turn.shape != r.shape or not np.isfinite(turn).all() or (turn < 0).any():
            raise ValueError("Turnover must be finite, nonnegative and aligned")
        out["one_way_turnover_pct"] = float(turn.mean()*50)
    return out
