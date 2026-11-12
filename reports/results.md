# Results and figure guide

Primary periods: research=2012–2024; later=2025–2026-10-20. All already viewed. Tables preserve the archived definitions; no new parameters or direction were selected for this publication.

## Six-style IC / RankIC: original BY552

| period | horizon | metric | mean | p_two_sided | q_BY_combined552 |
| --- | --- | --- | --- | --- | --- |
| research | 1 | ic | 0.0111 | 6.299e-14 | 7.754e-13 |
| research | 1 | rank_ic | 0.02261 | 7.292e-58 | 5.137e-56 |
| research | 5 | ic | 0.01869 | 1.605e-11 | 1.802e-10 |
| research | 5 | rank_ic | 0.0332 | 2.998e-32 | 9.347e-31 |
| research | 21 | ic | 0.01967 | 1.37e-06 | 1.229e-05 |
| research | 21 | rank_ic | 0.03487 | 2.1e-17 | 3.049e-16 |
| later | 1 | ic | 0.006013 | 0.001865 | 0.01405 |
| later | 1 | rank_ic | 0.02436 | 5.997e-17 | 8.419e-16 |
| later | 5 | ic | 0.0109 | 0.002319 | 0.01723 |
| later | 5 | rank_ic | 0.03161 | 2.121e-09 | 2.135e-08 |
| later | 21 | ic | 0.01042 | 0.04631 | 0.3245 |
| later | 21 | rank_ic | 0.03662 | 1.087e-10 | 1.165e-09 |

## Six-style Fama–MacBeth: original BY552

Coefficient bp are cumulative future-return bp per 1SD of the raw oriented rank signal, not annualized portfolio returns. The raw95%CI is not multiplicity-adjusted.

| period | horizon | coefficient_bp | p_two_sided | q_BY_combined552 |
| --- | --- | --- | --- | --- |
| research | 1 | 2.662 | 1.048e-12 | 1.231e-11 |
| research | 5 | 9.916 | 3.391e-10 | 3.534e-09 |
| research | 21 | 20.87 | 2.812e-05 | 0.0002252 |
| later | 1 | 1.928 | 0.003287 | 0.02418 |
| later | 5 | 7.6 | 0.008742 | 0.06299 |
| later | 21 | 14.24 | 0.1063 | 0.7355 |

## Statistics families

The first two tables use original552. Incremental-family tables and figures use new372; combined924 is sensitivity only. Earlier and later studies can report the SAME baseline mean and p with DIFFERENT q because the family changes. The complete families are released, allowing the adjustment to be recomputed.

## Charts

### 01 Formula

![01_Formula](figures/01_Formula.png)

### 02 Cumulative NAV

![02_Cumulative_NAV](figures/02_Cumulative_NAV.png)

### 03 IC RankIC

![03_IC_RankIC](figures/03_IC_RankIC.png)

### 04 Decile NAV

![04_Decile_NAV](figures/04_Decile_NAV.png)

### 05 Style Controls

![05_Style_Controls](figures/05_Style_Controls.png)

### 06 Controlled IC RankIC

![06_Controlled_IC_RankIC](figures/06_Controlled_IC_RankIC.png)

### 07 Significance p q

![07_Significance_p_q](figures/07_Significance_p_q.png)

### 08 Fama MacBeth

![08_Fama_MacBeth](figures/08_Fama_MacBeth.png)

### 09 Parameter Neighborhood

![09_Parameter_Neighborhood](figures/09_Parameter_Neighborhood.png)

### 10 Execution Delay

![10_Execution_Delay](figures/10_Execution_Delay.png)

### 11 Universe Filters

![11_Universe_Filters](figures/11_Universe_Filters.png)

### 12 Six Styles All Costs

![12_Six_Styles_All_Costs](figures/12_Six_Styles_All_Costs.png)

### 13 Fixed Definitions

![13_Fixed_Definitions](figures/13_Fixed_Definitions.png)

### 14 Signal Overlap

![14_Signal_Overlap](figures/14_Signal_Overlap.png)

### 15 1D Incremental IC

![15_1D_Incremental_IC](figures/15_1D_Incremental_IC.png)

### 16 Portfolio NAV 10bp

![16_Portfolio_NAV_10bp](figures/16_Portfolio_NAV_10bp.png)

### 17 Portfolio Metrics 10bp

![17_Portfolio_Metrics_10bp](figures/17_Portfolio_Metrics_10bp.png)

### 18 Joint FMB

![18_Joint_FMB](figures/18_Joint_FMB.png)

## Plateau interpretation

Neighborhood heatmaps show gross CAGR, not10bp results. The primary formal rule uses80%retention,63-day circular blocks,4999 draws, simultaneous bounds across eight neighbors and an extra across-eight-maps correction. All main RankIC maps pass; later gross-CAGR maps have only4/8(base) and2/8(six) neighbors passing. Neither a smooth heatmap nor passing local tests rules out historical search overfitting. Delay/universe-filter books have their own matched starts/pools.

## Archived PDF

[Pre-CV report snapshot](ew40_research_snapshot.pdf): retained for the original research chain, not a replacement for the later [CV incremental report](incremental.zh-CN.md).
