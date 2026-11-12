# Methodology and reproducibility boundary

## Estimator

Raw AS uses traded **amount**, not turnover. RA(t)=Amount(t)/mean(Amount(t−20)..Amount(t−1)). A full finite prior20 and positive denominator are required. An observed zero today gives RA0; missing data are not zero-filled. EW40 uses lambda39/41 and the full continuous valid RA segment with minimum40 values, finite-weight variance correction1−sum(p²), and no further EMA. Missing RA resets EW history. The economic research direction is −1. AS measures dispersion around the estimated weighted mean, not a constant1; it is not itself divided by that weighted mean.

## Universe, cross-section and controls

The empirical main study used the frozen common pool of ten estimator configurations and common valid style inputs; CV20/CVEW40 intersections retained100% of that pool. Common dates and all three inputs were reconciled. The portable implementation does not reconstruct this proprietary/source-dependent pool.

Average raw ranks are computed on t-known common eligible stocks. One joint unweighted OLS includes industry dummies, log float cap, and selected finite controls. Residuals get population-standard-deviation scaling, then the frozen direction. Never neutralize an already neutralized residual again to mimic the joint specification; never rerank residuals or smooth after projection. Add controls to the SAME joint design. For the CV study, raw reference ranks are extra controls. Total-cap size and log float-cap base controls are different descriptors, not accidental duplicates.

Six local CNE5 proxies: size, nonlinear size, beta, momentum, residual volatility and liquidity. They are not official Barra data, do not cover all classic CNE5 styles, and do not exclude nonlinear/omitted-style effects. Fundamental B/P, earnings yield, growth and leverage controls and new short-term reversal controls are not part of the completed main six-style run. Financial inputs added later must respect publication timestamps and revisions.

## Portfolio accounting

At t close form score, target positive and negative linear legs normalized to +1/−1 of NAV, respectively. Fill at t+1 close; the next price interval t+1..t+2 is the first holding return. Rebalance daily. Frozen nontradable inventory remains; unsuccessful target budgets are not redistributed. Positions continue across2025. Charges0/10/20bp are separate ledgers on actually executed bilateral traded notional, not a fee subtracted once from CAGR. Daily one-way TO=bilateral TO/2. NAV starts1 for each displayed interval, without resetting underlying positions.

CAGR=exp(mean(log(1+daily return))*252)−1; Sharpe=sqrt252*mean/sampleSD, rf0; MDD includes initial NAV1. 200%target gross exposure does not imply actual exposure is exactly200% every day. Deciles are separate independently simulated long-only diagnostics and cannot be substituted for the main signal-weighted long-short book. Stock borrowing, financing, impact, participation constraints and full order/price-limit simulation are not certified.

## Predictive labels and FMB

IC=Pearson; RankIC=Spearman(final processed score, simple forward return). For h=1/5/21, return uses observed closes t+1→t+1+h and may not cross each period endpoint. Overlapping daily labels are not independent samples; h is not a separate rebalance schedule.

Characteristic FMB: on each t, jointly regress these future returns on industry, log float cap, optional styles and negatively oriented raw ranks z-standardized on the t-known FULL common pool before filtering future endpoints. Report the time mean of daily characteristic coefficients. These are future cumulative-return bp per1SD raw-rank predictor, not strategy returns, IV2SLS or causal effects. It uses the same underlying observations as IC and is not an independent validation sample.

## Inference families

HAC63 uses Bartlett weights and a two-sided asymptotic normal p, with21/126 sensitivity. Nonfinite observations are removed before forming consecutive HAC lags, matching the archived convention. Raw95%CI are not multiple-test-adjusted. The nulls are zero mean IC/RankIC, zero mean FMB coefficient, or zero mean paired difference as appropriate. BY adjusted p is called q; it is not a posterior probability or Storey q.

Original552=540IC tests (45sensitivity cases×2periods×3horizons×2metrics)+12FMB. New372=216IC means+84FMB means+48paired blend-minus-CV IC differences+24paired daily-book-return differences. Combined924 is exploratory sensitivity. Use the entire family to recompute adjustment, not just visible selected rows. No family covers the entire unknown historical library search. Bootstrap1999 and plateau4999 draws use date blocks; nonzero resampling p estimates and existing sensitivity files are preserved.

## CV extension

Daily turnover=Volume/CirculatedShare in consistent units, with observed zeros retained and unavailable observations missing. No clipping at100%. CV20=current-inclusive20day sampleSTD(ddof1)/mean; CVEW40=finite-weight-corrected EW40STD/same-weighted-mean, minimum40 continuous, gaps reset. Both negative, no additional EMA. These are fixed definitions agreed for this comparison, not a claim to exactly reproduce every published turnover-CV variant.

AS|CV and CV|AS use one joint projection from raw ranks. Fixed50/50 mixes standardized separately processed scores and then normalizes long/short legs; weights were not fitted. Residual standalone PNL does not equal additive alpha in a combined portfolio. Annualized CAGR differences are descriptive; paired mean-daily-return tests assess net improvement.

## Selection history and remaining work

The original direction was frozen from earlier training-period base1D RankIC. EW40 was selected for display from ten estimator configurations, following a developmentIC/turnover rule, with a documented fallback because no candidate achieved jointIC-up/TO-down in both development windows. All historical periods, including2025+, had already been viewed. This was an exploratory refinement, not a fresh preregistered anomaly discovery. Nine local parameter neighbors are insufficient to account for broader selection history.

Future work: expanded fundamental and short-reversal controls; direct portfolio-return spanning and held-position style exposures; independent future fixed-rule observations; improved PIT, delisting, borrow, price-limit and capacity audits. These have not been completed by merely publishing the repository.

## What can be reproduced here

Portable estimator/CV/projection functions, synthetic numerical checks, independent recomputation of released aggregate-ledger metrics, HAC IC/FMB statistics, BY families, and the six-style cost chart. Files under data/derived are derived research series, not provider stock-level market data. The original full-market backtest and all nine-neighbor resampling runs cannot be recreated without provider inputs and the historical research engine. Existing plateau/bootstrap results are snapshots, not rerun by the release audit.
