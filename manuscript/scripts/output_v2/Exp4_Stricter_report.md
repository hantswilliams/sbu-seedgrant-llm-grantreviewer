# Experiment 4: Stricter Prompt
**Description:** Stricter prompt with DANIEL training data (DANIEL excluded from analysis)
**Generated:** 2025-11-05 12:32:42

---

## Sample Sizes
- Human reviews: 8
- LLM reviews: 18
- *Note: All reviews of DANIEL excluded (used as training data)*

## Overall Performance

### Human Reviewers
- Mean ± SD: 83.12 ± 13.73
- Median (IQR): 85.50 (74.00 - 92.75)
- Range: 64.0 - 99.0

### LLM Reviewers
- Mean ± SD: 72.44 ± 5.34
- Median (IQR): 72.00 (69.25 - 76.00)
- Range: 62.0 - 83.0

### Statistical Comparison
- Difference (LLM - Human): -10.68 points
- t-statistic: 2.900
- p-value: 0.0079 (significant)
- Cohen's d: -1.026

![Overall Comparison](Exp4_Stricter_overall_comparison.png)

## Performance by Criteria

| Criterion | Human Mean (%) | LLM Mean (%) | Difference | p-value |
|-----------|----------------|--------------|------------|----------|
| Innovation & Impact | 86.7% | 78.0% | -2.61 | 0.0026* |
| Methodology & Feasibility | 77.1% | 64.3% | -3.85 | 0.0661 |
| Team Strength | 87.5% | 76.5% | -1.10 | 0.0738 |
| External Funding Potential | 83.8% | 77.8% | -0.60 | 0.1975 |
| Budget Clarity | 88.8% | 77.2% | -1.15 | 0.0897 |
| Presentation Quality | 80.0% | 70.6% | -0.94 | 0.0466* |

![Criteria Comparison](Exp4_Stricter_criteria_comparison.png)

## Model-Specific Performance

| Model | n | Mean ± SD | Difference from Human |
|-------|---|-----------|----------------------|
| Google | 6 | 78.00 ± 3.29 | -5.12 |
| OpenAI | 6 | 69.83 ± 5.00 | -13.29 |
| xAI | 6 | 69.50 ± 2.35 | -13.62 |

![Model Comparison](Exp4_Stricter_model_comparison.png)

## Recommendation Analysis

**Broad Agreement Rate (Positive vs Negative):** 50.0%
**Exact Agreement Rate:** 0.0%

*Note: Broad agreement groups 'Fund' and 'Fund with Revisions' as 'Positive' vs 'Do Not Fund' as 'Negative'*

### Human Recommendations
- Do Not Fund: 2 (25.0%)
- Fund: 4 (50.0%)
- Fund with Revisions: 2 (25.0%)

### LLM Recommendations
- Do Not Fund: 5 (27.8%)
- Fund with Revisions: 13 (72.2%)

![Recommendations](Exp4_Stricter_recommendations.png)

## Inter-Rater Consistency
- Human average SD: 12.56
- LLM average SD: 5.19
- Pearson correlation: r = -1.000 (p = 1.0000)
- Spearman correlation: ρ = -1.000 (p = nan)
