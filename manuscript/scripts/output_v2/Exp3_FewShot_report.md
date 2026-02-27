# Experiment 3: Few Shot
**Description:** Multiple training examples using DANIEL data (DANIEL excluded from analysis)
**Generated:** 2025-11-05 12:32:41

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
- Mean ± SD: 80.56 ± 5.36
- Median (IQR): 81.50 (77.25 - 84.00)
- Range: 70.0 - 90.0

### Statistical Comparison
- Difference (LLM - Human): -2.57 points
- t-statistic: 0.697
- p-value: 0.4926 (not significant)
- Cohen's d: -0.247

![Overall Comparison](Exp3_FewShot_overall_comparison.png)

## Performance by Criteria

| Criterion | Human Mean (%) | LLM Mean (%) | Difference | p-value |
|-----------|----------------|--------------|------------|----------|
| Innovation & Impact | 86.7% | 83.5% | -0.94 | 0.2596 |
| Methodology & Feasibility | 77.1% | 77.2% | +0.04 | 0.9831 |
| Team Strength | 87.5% | 83.9% | -0.36 | 0.5155 |
| External Funding Potential | 83.8% | 84.4% | +0.07 | 0.8532 |
| Budget Clarity | 88.8% | 78.9% | -0.99 | 0.1440 |
| Presentation Quality | 80.0% | 76.1% | -0.39 | 0.4513 |

![Criteria Comparison](Exp3_FewShot_criteria_comparison.png)

## Model-Specific Performance

| Model | n | Mean ± SD | Difference from Human |
|-------|---|-----------|----------------------|
| xAI | 6 | 83.33 ± 1.21 | +0.21 |
| Google | 6 | 82.33 ± 6.83 | -0.79 |
| OpenAI | 6 | 76.00 ± 3.41 | -7.12 |

![Model Comparison](Exp3_FewShot_model_comparison.png)

## Recommendation Analysis

**Broad Agreement Rate (Positive vs Negative):** 50.0%
**Exact Agreement Rate:** 0.0%

*Note: Broad agreement groups 'Fund' and 'Fund with Revisions' as 'Positive' vs 'Do Not Fund' as 'Negative'*

### Human Recommendations
- Do Not Fund: 2 (25.0%)
- Fund: 4 (50.0%)
- Fund with Revisions: 2 (25.0%)

### LLM Recommendations
- Do Not Fund: 1 (5.6%)
- Fund: 3 (16.7%)
- Fund with Revisions: 14 (77.8%)

![Recommendations](Exp3_FewShot_recommendations.png)

## Inter-Rater Consistency
- Human average SD: 12.56
- LLM average SD: 5.18
- Pearson correlation: r = 1.000 (p = 1.0000)
- Spearman correlation: ρ = 1.000 (p = nan)
