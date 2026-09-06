## Table 2. Summary of experimental results across three prompt engineering conditions

| Metric | Exp 1: Zero-shot | Exp 2: Few-shot | Exp 3: Few-shot + strict |
|---|---|---|---|
| Human reviews (n) | 12 | 8 | 8 |
| LLM reviews (n raw/aggregated) | 27/9 | 18/6 | 18/6 |
| Human mean ± SD | 79.08 ± 13.32 | 83.12 ± 13.73 | 83.12 ± 13.73 |
| LLM mean ± SD (aggregated) | 83.63 ± 5.24 | 80.56 ± 4.81 | 72.44 ± 4.98 |
| Mean difference [95% CI] | +4.55 [-3.37, +12.22] | -2.57 [-11.79, +7.18] | -10.68 [-20.00, -0.87] |
| p-value (aggregated) | 0.347 | 0.671 | 0.096 |
| Glass's Δ [95% CI] | 0.34 [-0.28, 1.16] | -0.19 [-1.43, 0.58] | -0.78 [-2.56, -0.06] |
| Broad agreement | 58.3% | 75.0% | 58.3% |
| Cohen's κ (broad) | 0.000 | 0.000 | -0.250 |
| Exact agreement | 33.3% | 25.0% | 16.7% |
| Cohen's κ (exact) | 0.053 | 0.000 | -0.111 |
| Mixed model: LLM effect [95% CI], p | +4.55 [-9.23, +18.32], p = 0.518 | -2.57 [-17.04, +11.90], p = 0.728 | -10.68 [-25.38, +4.02], p = 0.154 |
| Sensitivity κ, raw pairs (exact / broad) | 0.061 / 0.000 (n = 108) | 0.020 / 0.100 (n = 72) | -0.037 / -0.071 (n = 72) |

## Table 3. LLM vendor mean scores and deviation from human mean

| Vendor | Exp 1: Zero-shot | Exp 2: Few-shot | Exp 3: Few-shot + strict |
|---|---|---|---|
| Gemini 2.5 Flash | 88.44 (+9.36) | 82.33 (-0.79) | 78.00 (-5.12) |
| GPT-5 Nano | 77.33 (-1.75) | 76.00 (-7.12) | 69.83 (-13.29) |
| Grok 4 Fast | 85.11 (+6.03) | 83.33 (+0.21) | 69.50 (-13.62) |

## Criterion-level deviations (LLM raw mean − human mean), t-test on cell means, Holm-corrected


**Exp 1: Zero-shot**

| Criterion | Human mean | LLM mean | Difference | p (uncorrected) | p (Holm) |
|---|---|---|---|---|---|
| Innovation & Impact | 25.42 | 26.11 | +0.69 | 0.488 | 1.000 |
| Methodology & Feasibility | 21.67 | 24.48 | +2.81 | 0.264 | 1.000 |
| Team Strength | 8.58 | 8.48 | -0.10 | 0.854 | 1.000 |
| External Funding Potential | 7.67 | 8.78 | +1.11 | 0.064 | 0.382 |
| Budget Clarity | 8.33 | 8.37 | +0.04 | 0.956 | 1.000 |
| Presentation Quality | 7.42 | 7.41 | -0.01 | 0.987 | 1.000 |

**Exp 2: Few-shot**

| Criterion | Human mean | LLM mean | Difference | p (uncorrected) | p (Holm) |
|---|---|---|---|---|---|
| Innovation & Impact | 26.00 | 25.06 | -0.94 | 0.412 | 1.000 |
| Methodology & Feasibility | 23.12 | 23.17 | +0.04 | 0.990 | 1.000 |
| Team Strength | 8.75 | 8.39 | -0.36 | 0.625 | 1.000 |
| External Funding Potential | 8.38 | 8.44 | +0.07 | 0.909 | 1.000 |
| Budget Clarity | 8.88 | 7.89 | -0.99 | 0.202 | 1.000 |
| Presentation Quality | 8.00 | 7.61 | -0.39 | 0.568 | 1.000 |

**Exp 3: Few-shot + strict**

| Criterion | Human mean | LLM mean | Difference | p (uncorrected) | p (Holm) |
|---|---|---|---|---|---|
| Innovation & Impact | 26.00 | 23.39 | -2.61 | 0.031 | 0.186 |
| Methodology & Feasibility | 23.12 | 19.28 | -3.85 | 0.274 | 0.739 |
| Team Strength | 8.75 | 7.65 | -1.10 | 0.209 | 0.739 |
| External Funding Potential | 8.38 | 7.78 | -0.60 | 0.373 | 0.739 |
| Budget Clarity | 8.88 | 7.72 | -1.15 | 0.136 | 0.680 |
| Presentation Quality | 8.00 | 7.06 | -0.94 | 0.185 | 0.739 |

## Recommendation distributions

| Experiment | Group | Fund | Fund with Revisions | Do Not Fund |
|---|---|---|---|---|
| Exp 1: Zero-shot | human | 33.3% | 25.0% | 41.7% |
| Exp 1: Zero-shot | llm | 48.1% | 51.9% | 0.0% |
| Exp 2: Few-shot | human | 50.0% | 25.0% | 25.0% |
| Exp 2: Few-shot | llm | 16.7% | 77.8% | 5.6% |
| Exp 3: Few-shot + strict | human | 50.0% | 25.0% | 25.0% |
| Exp 3: Few-shot + strict | llm | 0.0% | 72.2% | 27.8% |

## Application-level means (Figure 2) and within-application dispersion

| Experiment | Human means | LLM means | Human within-app SD | LLM within-app SD | Reduction |
|---|---|---|---|---|---|
| Exp 1: Zero-shot | {'FC1': 77.0, 'FC2': 89.25, 'FC3': 71.0} | {'FC1': 84.56, 'FC2': 84.22, 'FC3': 82.11} | 11.37 | 5.78 | 49% |
| Exp 2: Few-shot | {'FC1': 77.0, 'FC2': 89.25} | {'FC1': 79.11, 'FC2': 82.0} | 12.56 | 5.18 | 59% |
| Exp 3: Few-shot + strict | {'FC1': 77.0, 'FC2': 89.25} | {'FC1': 73.33, 'FC2': 71.56} | 12.56 | 5.19 | 59% |

## Exploratory one-way ANOVA across prompt conditions (FC1 and FC2 only)

F(2,15) = 8.18, p = 0.004, η² = 0.522; group sizes [6, 6, 6]

