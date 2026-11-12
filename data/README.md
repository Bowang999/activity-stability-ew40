# Data interface

Only **derived aggregate research outputs** are included. No credentials, licensed stock-level market panels, float-share histories, eligibility masks, account data or stock-level positions are published. CSV gzip is readable with pandas.read_csv without a Parquet dependency.

- `derived/portfolio_metrics.csv`: all18 models×2periods×3costs=108 summaries.
- `derived/books/*.csv.gz`: daily aggregate net returns, bilateral turnover and exposures by model/cost. These are already-executed historical ledgers, not orders or positions.
- `derived/incremental_daily_ic.csv.gz`: date, cross-section count, IC, RankIC, horizon and model. Purge labels at the relevant period end before recomputation.
- `derived/incremental_daily_fmb.csv.gz`: daily characteristic coefficients, stage, regression, predictor, horizon and sample count.
- `derived/original_ic_family540_q552.csv` + `original_fmb12_q552.csv`: the complete original552 family split into two files.
- `derived/incremental_all_tests_p_q.csv`: complete new372 family, separateBY372 and combinedBY924 columns. `mean` units depend on test type; FMB here uses return fractions, while display tables usebp.
- `derived/plateau_*`, `robustness_*`, style exposure/overlap tables: archived sensitivity results. The publication audit verifies the main aggregates, not a full replay of these experiments.

Models: prefix`base__`=industry/logfloatcap; `six__`adds six local style proxies. `AS`=EW40, `CV20`=rectangular turnoverCV, `CVEW40`=same-memory turnoverCV, `_res_`=target conditioned on reference, `blend_`=fixed50/50score blend. Costs use actual bilateral executed amount. Turnover column is a fraction; one-way dailypercent=50×mean(turnover). Period`research`ends2024-12-31;`later`ends2026-10-20. Later is already viewed history.

For YOUR local estimator run, provide a finite/nonnegative amount array in time×security shape. Missing is NaN, observed zero remains0. `activity_stability(amount)` returns positive raw dispersion; use direction−1 AFTER joint cross-sectional projection. Supply t-known floatcap, nonnegative industry codes, common eligibility and finite selected descriptors to `process_cross_section` one date at a time. Provider calendars, delisting settlement, historical categories and tradeability must be supplied and audited separately. Never infer next-day availability or future survival from a final stock list.

Synthetic demo outputs go to ignored `results/local/`. Any private provider inputs belong in ignored `data/local/` and must not be committed.
