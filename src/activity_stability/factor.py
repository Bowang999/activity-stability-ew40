"""Causal estimator and one joint cross-sectional projection.

Arrays use time x security. EW40 is a decay span, not a 40-row truncation.
This reference implementation favors clarity over full-market speed.
"""
import numpy as np
import pandas as pd


def _panel(x):
    a = np.asarray(x, dtype=float)
    if a.ndim not in (1, 2):
        raise ValueError("Expected a vector or time x security matrix")
    return (a[:, None] if a.ndim == 1 else a), a.ndim == 1


def ew_std(values, span=40, min_periods=None):
    """Adjusted geometric-weight standard deviation; gaps reset history.

    The finite-weight denominator is 1 - sum(normalized_weight**2).
    Its usual unbiasedness interpretation requires sampling assumptions;
    serially dependent relative activity need not meet those assumptions.
    """
    if not isinstance(span, (int, np.integer)) or span < 2:
        raise ValueError("span must be an integer >= 2")
    minimum = span if min_periods is None else min_periods
    if not isinstance(minimum, (int, np.integer)) or minimum < 2:
        raise ValueError("min_periods must be an integer >= 2")
    x, vector = _panel(values)
    lam = (span - 1.) / (span + 1.)
    out = np.full(x.shape, np.nan)
    sw = np.zeros(x.shape[1]); sw2 = sw.copy(); mu = sw.copy(); m2 = sw.copy()
    count = np.zeros(x.shape[1], dtype=int)
    for t, row in enumerate(x):
        good = np.isfinite(row)
        sw[~good] = 0.; sw2[~good] = 0.; mu[~good] = 0.; m2[~good] = 0.; count[~good] = 0
        sw[good] = 1. + lam * sw[good]
        sw2[good] = 1. + lam * lam * sw2[good]
        delta = row[good] - mu[good]
        new_mu = mu[good] + delta / sw[good]
        m2[good] = lam * m2[good] + delta * (row[good] - new_mu)
        mu[good] = new_mu; count[good] += 1
        den = np.zeros_like(sw)
        den[good] = sw[good] - sw2[good] / sw[good]
        emit = good & (count >= minimum) & (den > 0)
        out[t, emit] = np.sqrt(np.maximum(0., m2[emit] / den[emit]))
    return out[:, 0] if vector else out


def activity_stability(amount, reference_window=20, span=40):
    """Return positive AS dispersion; the research score uses direction -1.

    Today's denominator uses only the preceding reference_window sessions.
    Observed zeros are preserved; nonfinite observations stay missing.
    """
    if not isinstance(reference_window, (int, np.integer)) or reference_window < 1:
        raise ValueError("reference_window must be a positive integer")
    x, vector = _panel(amount)
    if (x[np.isfinite(x)] < 0).any():
        raise ValueError("amount cannot be negative")
    frame = pd.DataFrame(np.where(np.isfinite(x), x, np.nan))
    denominator = frame.shift(1).rolling(reference_window, min_periods=reference_window).mean().to_numpy()
    ra = np.full(x.shape, np.nan)
    valid = np.isfinite(x) & np.isfinite(denominator) & (denominator > 0)
    np.divide(x, denominator, out=ra, where=valid)
    out = ew_std(ra, span)
    return out[:, 0] if vector else out


def turnover_cv(turnover, window=20, ew=False):
    """STD/mean of turnover; positive raw CV, negative research direction.

    Rectangular version uses ddof=1 and includes today. EW version uses
    the same adjusted weights for numerator and denominator; gaps reset.
    No additional EMA or clipping is applied.
    """
    if not isinstance(window, (int, np.integer)) or window < 2:
        raise ValueError("window must be an integer >= 2")
    x, vector = _panel(turnover)
    if (x[np.isfinite(x)] < 0).any():
        raise ValueError("turnover cannot be negative")
    frame = pd.DataFrame(np.where(np.isfinite(x), x, np.nan))
    if ew:
        sd = ew_std(x, window)
        mean = np.full_like(x, np.nan); sw = np.zeros(x.shape[1]); mu = sw.copy()
        lam = (window - 1.) / (window + 1.)
        for t, row in enumerate(x):
            good = np.isfinite(row); sw[~good] = 0.; mu[~good] = 0.
            sw[good] = 1. + lam * sw[good]
            mu[good] += (row[good] - mu[good]) / sw[good]
            mean[t, good] = mu[good]
    else:
        sd = frame.rolling(window, min_periods=window).std(ddof=1).to_numpy()
        mean = frame.rolling(window, min_periods=window).mean().to_numpy()
    out = np.full(x.shape, np.nan)
    np.divide(sd, mean, out=out, where=np.isfinite(sd) & (mean > 0))
    return out[:, 0] if vector else out


def process_cross_section(raw, float_cap, industry, eligible=None, controls=None,
                          direction=-1, min_industry=5, min_cross=100):
    """Average rank -> joint industry/log-cap/controls OLS -> population z.

    A SINGLE date's inputs; callers must supply historically available
    controls and a frozen common eligibility mask. Controls must be finite
    throughout that pool; silently changing the pool is not allowed here.
    Industry identifiers are nonnegative numeric codes, missing otherwise.
    """
    y = np.asarray(raw, float); cap = np.asarray(float_cap, float)
    groups = np.asarray(industry, float)
    if y.ndim != 1 or cap.shape != y.shape or groups.shape != y.shape:
        raise ValueError("raw, float_cap and industry must be equal-length vectors")
    mask = np.ones(len(y), bool) if eligible is None else np.asarray(eligible, bool).copy()
    if mask.shape != y.shape or direction not in (-1, 1):
        raise ValueError("Invalid eligibility shape or direction")
    mask &= np.isfinite(y) & np.isfinite(cap) & (cap > 0) & np.isfinite(groups) & (groups >= 0)
    for g in np.unique(groups[mask]):
        if np.sum(mask & (groups == g)) < min_industry:
            mask[groups == g] = False
    ids = np.flatnonzero(mask); out = np.full(y.shape, np.nan)
    if len(ids) < min_cross:
        return out
    extra = np.empty((len(y), 0)) if controls is None else np.asarray(controls, float)
    if extra.ndim == 1:
        extra = extra[:, None]
    if extra.ndim != 2 or extra.shape[0] != len(y) or not np.isfinite(extra[ids]).all():
        raise ValueError("Controls must be finite, security x descriptor, on the frozen pool")
    ranks = pd.Series(y[ids]).rank(method="average").to_numpy()
    dummy = np.column_stack([groups[ids] == g for g in np.unique(groups[ids])]).astype(float)
    continuous = np.column_stack([np.log(cap[ids]), extra[ids]])
    continuous -= continuous.mean(0)
    sd = continuous.std(0)
    continuous /= np.where(sd > 1e-12, sd, 1.)
    design = np.column_stack([dummy, continuous])
    residual = ranks - design @ np.linalg.lstsq(design, ranks, rcond=1e-10)[0]
    sigma = residual.std(ddof=0)
    if sigma > 1e-10:
        out[ids] = direction * (residual - residual.mean()) / sigma
    return out
