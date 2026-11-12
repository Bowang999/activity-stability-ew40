"""Portable reference functions; empirical market data are not redistributed."""
from .factor import activity_stability, ew_std, turnover_cv, process_cross_section
from .statistics import hac_mean, adjust_p, performance

__all__ = ["activity_stability", "ew_std", "turnover_cv", "process_cross_section", "hac_mean", "adjust_p", "performance"]
