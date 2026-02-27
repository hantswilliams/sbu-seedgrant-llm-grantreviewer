# Blinded Peer Review: Internal Consistency and Methods Audit

**Manuscript:** "Evaluating Large Language Models as Grant Reviewers: A Comparative Study of Prompt Engineering Strategies"

**Review Type:** FULL_METHODS + CONSISTENCY_AUDIT

**Date:** 2026-02-27

---

## 0) Material Inventory and Review Scope

### Materials Provided
- **Main manuscript:** Brief report format (~4,500 words), including Abstract, Introduction, Method, Results (with Tables 1-2), Discussion (with Limitations and Implications subsections), References (n=13), and standard declarations.
- **Supplementary materials:** Full prompt templates for all three reported experimental conditions (S1.1-S1.3), criterion-level statistical tables (S2: Tables S1-S3), per-vendor criterion means (S3: Tables S4-S6), recommendation distributions (S4: Table S7), and API configuration details (S5: Table S8).
- **Raw database:** SQLite database (`results.db`) containing 120 rows (12 human reviews + 108 LLM reviews across 4 experimental conditions).

### Materials Missing or Not Provided
- **Analysis code:** Referenced as publicly available on GitHub but not reviewed as part of this audit. Reproducibility of bootstrap CIs and Holm corrections depends on this code.
- **De-identified application texts:** Not provided for review; it is not possible to assess whether application characteristics might explain results.
- **Preregistration:** None (acknowledged by the authors).
- **Fourth experimental condition:** The database contains 27 LLM reviews from a `with_training_data_v1` experiment (single-example few-shot) that is neither reported nor mentioned anywhere in the manuscript or supplementary materials. This is addressed under Major Concerns.

### Scope of This Review
This review focuses on internal consistency (verifying all reported numbers against the raw database), methodological adequacy, statistical appropriateness, and whether the interpretive claims are supported by the evidence. All numerical values in the manuscript and supplementary tables were independently recomputed from the SQLite database.

---

## 1) Overall Recommendation

**Major Revision**

The manuscript addresses a timely question with a well-structured experimental design, and the core numerical results are largely verified against the raw data. However, several issues require substantive revision before the work meets publication standards: (a) the existence of an unreported fourth experimental condition constitutes selective reporting that must be disclosed and justified; (b) the stated total of "63 LLM reviews" is misleading because 81 reviews were generated across the three reported experiments (and 108 across all four conditions in the database); (c) the discrepancy between the parametric p-value and the bootstrap confidence interval in Experiment 3 needs explicit reconciliation; and (d) several interpretive claims exceed what these sample sizes can support. None of these issues are individually fatal, but collectively they undermine confidence in the transparency and rigor of the reporting.

---

## 2) Summary Assessment

This exploratory pilot study compares LLM-generated grant review scores to human expert reviews across three prompt engineering conditions (zero-shot, few-shot, few-shot with strict instructions) using three commercial LLMs and three de-identified seed grant applications. The experimental design is thoughtful, with appropriate controls for data contamination via training-test separation of applications, and the authors commendably address pseudoreplication through cell-mean aggregation. The core statistical findings -- that few-shot prompting produced the closest alignment while strict instructions induced substantial under-scoring -- are verified by the raw data. However, the study's interpretive value is severely constrained by the sample of only three applications from a single institution, and the manuscript does not disclose a fourth experimental condition present in the database. The statistical reporting is generally accurate, with one notable inconsistency between a parametric p-value and its corresponding bootstrap confidence interval that requires explanation. The authors' self-awareness of limitations is commendable but does not fully compensate for the transparency gap created by the unreported condition.

---

## 3) Fatal Flaws

None identified. The issues described below are serious but correctable through revision.

---

## 4) Major Concerns

### 4.1 Unreported Fourth Experimental Condition (Selective Reporting)

The raw database contains a `with_training_data_v1` condition (27 LLM reviews, 3 vendors x 3 applications x 3 iterations) that is not mentioned anywhere in the manuscript or supplementary materials. Examination of the prompt file reveals this is a single-example few-shot condition (providing only one human reviewer's scores for DANIEL as calibration, specifically HW's review scoring 77 with a "Do Not Fund" recommendation), distinct from the multi-example few-shot condition (Experiment 2, `multi_examples_v1`) that provides all four human reviewers' scores.

This omitted condition produced a mean deviation from the human mean of +1.82 points on the common FC1+FC2 base (Glass's delta = 0.13, p = 0.768), which is arguably better aligned than the reported multi-example condition (-2.57 points, Glass's delta = -0.19, p = 0.671) on some metrics. The omission is not disclosed or justified, and there is no mention that a fourth condition was run. This constitutes undisclosed selective reporting.

**Required action:** The authors must either (a) report this condition as a fourth experiment with full statistical results, or (b) provide a transparent statement explaining when and why this condition was excluded, with the data available in the repository. If the condition was a pilot or preliminary run, this should be stated explicitly.

### 4.2 Misleading Total LLM Review Count

The manuscript states: "Three independent iterations per vendor-application-experiment combination yielded 63 total LLM reviews" (Section 2.4). This is misleading. The database confirms that LLMs reviewed all three applications in all experiments, including DANIEL in Experiments 2 and 3 (where DANIEL was excluded from comparisons but was still reviewed). The actual counts are:

- Reported experiments: 27 (Exp 1) + 27 (Exp 2) + 27 (Exp 3) = **81 LLM reviews generated**
- Including unreported experiment: 27 x 4 = **108 LLM reviews generated**
- Comparison analyses: 27 (Exp 1) + 18 (Exp 2) + 18 (Exp 3) = **63 LLM reviews analyzed**

The figure "63" conflates reviews generated with reviews analyzed. The phrasing "yielded 63 total LLM reviews" implies that only 63 were produced, which is factually incorrect. The DANIEL reviews in Experiments 2-3 exist in the database and could, in principle, provide additional information (e.g., whether LLMs can replicate the training application's known scores -- a test of calibration fidelity).

**Required action:** Report the actual number of LLM reviews generated (81 for three experiments, or 108 total) and clarify that 63 were included in the primary analyses. Consider reporting LLM scores on the training application (DANIEL) in Experiments 2-3 as a calibration check.

### 4.3 Bootstrap CI and Parametric p-Value Discrepancy (Experiment 3)

The manuscript reports for Experiment 3: "the confidence interval for the mean difference ([-20.11, -1.03]) excludes zero" alongside p = 0.097. These are logically inconsistent at the alpha = 0.05 level: if the 95% CI excludes zero, the corresponding two-sided test should reject at alpha = 0.05. The manuscript notes this tension but attributes it to "the wide uncertainty inherent in these small samples," which is not a statistical explanation.

Independent recomputation using bias-corrected bootstrap (10,000 resamples, different random seed) yielded a CI of approximately [-19.96, -0.78], also excluding zero, while the parametric t-test gives p = 0.096. The discrepancy arises because the bootstrap CI and the t-test make different distributional assumptions, and with small, non-normal samples, they can disagree. This is a legitimate statistical phenomenon, but the manuscript must explain it explicitly rather than glossing over it.

**Required action:** Acknowledge the discrepancy directly and explain that it arises from the difference between parametric (t-test, assumes normality) and non-parametric (bootstrap) inference. State which method the authors consider primary. If both are retained, note that the bootstrap CI suggests significance while the t-test does not, and interpret accordingly with appropriate caution.

---

## 5) Moderate Concerns

### 5.1 Non-Independence of Human Scores in t-Tests

The manuscript acknowledges (Section 2.5) that "Human scores are treated as independent observations in the t-tests, though the four reviewers each scored all applications, introducing within-reviewer correlation that is not modeled." This is a genuine concern. With only four reviewers each scoring three (or two) applications, the effective degrees of freedom may be substantially lower than nominal, which could inflate Type I error rates. The authors correctly note this limitation, but the manuscript does not quantify the potential impact.

For Experiment 1 (12 human scores = 4 reviewers x 3 applications), the ICC among reviewers would determine how much the effective sample size is reduced. Given the wide human score range (SD = 13.32), the within-reviewer correlation could be non-trivial. This concern is partially mitigated by the fact that all reported p-values are well above alpha = 0.05 (smallest: 0.097), so inflation of effective degrees of freedom is unlikely to change any statistical conclusions in this case. However, the principle should be stated more clearly for methodological rigor.

### 5.2 Confounded Temperature Settings Across Vendors

The manuscript notes that xAI Grok used temperature = 0.1 while OpenAI and Google used default temperature = 1.0. This is a substantial confound: temperature directly controls output variability, and the manuscript's core claim about LLM "consistency" is undermined by the fact that one-third of the LLM reviews were generated under conditions designed to minimize variability. The dispersion analysis (49-59% lower SD than humans) is likely inflated by Grok's artificially constrained output.

The authors mention this in the limitations but do not analyze it. A supplementary analysis showing within-vendor dispersion for each vendor separately would clarify the extent to which the "consistency" finding is driven by Grok's temperature setting versus an intrinsic property of LLMs.

**Suggested action:** Report vendor-specific within-applicant standard deviations in a supplementary analysis to disentangle temperature effects from general LLM behavior.

### 5.3 Cohen's Kappa Computed Over Non-Independent Pairs

The manuscript reports Cohen's kappa over all human-LLM review pairs per application (e.g., 108 pairs in Experiment 1 = 12 human x 9 LLM). Each human review appears in multiple pairs (crossed with all 9 LLM reviews for that application), and each LLM review appears in multiple pairs (crossed with all 4 human reviews). This non-independence violates the assumptions of Cohen's kappa, which requires independent observation pairs.

The authors acknowledge this ("human-LLM pairs are non-independent") and argue it is unlikely to change qualitative conclusions given near-zero kappa values. This is a reasonable argument, but the point estimates themselves are unreliable and should not be compared across experiments or interpreted precisely. The presentation of kappa to three decimal places (e.g., 0.061, 0.020, -0.037) implies a precision that is not warranted.

### 5.4 Applicant-Level Human Score-Recommendation Discordance

The raw database reveals that reviewer Y assigned CHRISTINA a total score of 64/100 and recommended "Fund." This is the lowest score associated with a positive recommendation in the dataset and is discordant with the pattern of other reviewers (e.g., reviewer AM scored CHRISTINA at 65 and recommended "Do Not Fund"). This observation is not discussed in the manuscript but is relevant to the reliability of the human reference standard. If human reviewers themselves show score-recommendation inconsistency, the kappa-based comparison of LLM recommendations to human recommendations may be comparing two noisy processes.

### 5.5 Interpretation of "Best Alignment" in Experiment 2

The manuscript highlights Experiment 2 as the "best-aligned" condition based on the smallest mean difference (-2.57 points). However, the authors appropriately note that this "cannot be definitively attributed to generalizable few-shot learning" because the training examples came from a single application. The concern goes further: the unreported single-example condition (`with_training_data_v1`) produced a deviation of only +1.82 points on the same common base, which is numerically closer to zero than -2.57. If the single-example condition actually outperforms the multi-example condition, the theoretical rationale for why more examples improve calibration is weakened, not strengthened.

---

## 6) Minor Concerns

### 6.1 Table S6 Note Claims n=6 Per Vendor, but GPT-5 Nano Team Strength Has n=5

Table S6 states "n = 6 per vendor (2 applications x 3 iterations)." However, the missing Team Strength value (OpenAI, KELLY, strict_scoring_v1, iteration 1) means the GPT-5 Nano Team Strength statistic is computed from n=5 observations (mean = 8.20, SD = 0.84). The implied Team Strength for the missing review is 0 (total score 62 = sum of other five criteria = 62), which would be an extreme outlier if included. The manuscript notes the missing value but does not flag the inconsistency in the supplementary table note.

### 6.2 Rounding of "52-78%" for Fund with Revisions

The manuscript states LLMs "consistently favored 'Fund with Revisions' (52-78%)." The actual values are 51.9% (Exp 1), 77.8% (Exp 2), and 72.2% (Exp 3). Rounding 51.9% to 52% is acceptable, but the range "52-78%" implies Experiment 3 is at one extreme, when in fact it falls at 72.2%. The sentence could more accurately read "52-78%" only if Experiments 2-3 are considered (52% is from Exp 1 and 78% is from Exp 2). This is not incorrect but could be clearer.

### 6.3 Application Pseudonym Mapping

The manuscript refers to FC1, FC2, and FC3 but does not provide a mapping to the database pseudonyms (KELLY, CHRISTINA, DANIEL). While the mapping can be inferred from context (FC3 = DANIEL, used as training), for reproducibility purposes, the correspondence should be stated explicitly in the supplementary materials or data availability section.

### 6.4 Reference to "Approximately 2.5-Fold Variance Difference"

Section 2.5 refers to "the approximately 2.5-fold variance difference between groups" to justify using Glass's delta. The actual variance ratio (human variance / LLM variance) for Experiment 1 is (13.32/5.24)^2 = 6.46-fold, which is a 6.5-fold variance difference, not 2.5-fold. If the authors mean the SD ratio (13.32/5.24 = 2.54), this should say "2.5-fold standard deviation difference." Variance and standard deviation ratios are not interchangeable.

### 6.5 Software Version Specificity

The manuscript cites "scipy 1.11, scikit-learn 1.6, and pandas 2.1." Given that bootstrap CIs are seed-dependent and the exact implementation varies across scipy versions, providing the exact minor version (e.g., scipy 1.11.4) and the random seed would support reproducibility.

---

## 7) Internal Consistency Audit

All values were independently recomputed from the SQLite database at `data/results.db`. The database contains 120 rows: 12 human reviews (4 reviewers x 3 applications) and 108 LLM reviews (4 experiments x 3 vendors x 3 applications x 3 iterations).

### Table 1 (Main Results)

| Claim | Manuscript Value | Recomputed Value | Status |
|---|---|---|---|
| Exp 1 Human n | 12 | 12 | VERIFIED |
| Exp 1 LLM n (raw/aggregated) | 27/9 | 27/9 | VERIFIED |
| Exp 1 Human mean +/- SD | 79.08 +/- 13.32 | 79.08 +/- 13.32 | VERIFIED |
| Exp 1 LLM mean +/- SD (agg) | 83.63 +/- 5.24 | 83.63 +/- 5.24 | VERIFIED |
| Exp 1 Mean diff | +4.55 | +4.55 | VERIFIED |
| Exp 1 p-value | 0.347 | 0.347 | VERIFIED |
| Exp 1 Glass's delta | 0.34 | 0.34 | VERIFIED |
| Exp 2 Human n | 8 | 8 | VERIFIED |
| Exp 2 LLM n (raw/aggregated) | 18/6 | 18/6 | VERIFIED (as comparison group; 27 total generated) |
| Exp 2 Human mean +/- SD | 83.13 +/- 13.73 | 83.12 +/- 13.73 | VERIFIED (83.125 rounds to 83.13) |
| Exp 2 LLM mean +/- SD (agg) | 80.56 +/- 4.81 | 80.56 +/- 4.81 | VERIFIED |
| Exp 2 Mean diff | -2.57 | -2.57 | VERIFIED |
| Exp 2 p-value | 0.671 | 0.671 | VERIFIED |
| Exp 2 Glass's delta | -0.19 | -0.19 | VERIFIED |
| Exp 3 Human mean +/- SD | 83.13 +/- 13.73 | 83.12 +/- 13.73 | VERIFIED |
| Exp 3 LLM mean +/- SD (agg) | 72.44 +/- 4.98 | 72.44 +/- 4.98 | VERIFIED |
| Exp 3 Mean diff | -10.68 | -10.68 | VERIFIED |
| Exp 3 p-value | 0.097 | 0.096 | MINOR DISCREPANCY (rounding: 0.09646 rounds to 0.096 or 0.097 depending on precision) |
| Exp 3 Glass's delta | -0.78 | -0.78 | VERIFIED |

### Table 1 Agreement Metrics

| Claim | Manuscript Value | Recomputed Value | Status |
|---|---|---|---|
| Exp 1 Exact agreement | 33.3% (n=108 pairs) | 33.3% (36/108) | VERIFIED |
| Exp 1 Broad agreement | 58.3% | 58.3% (63/108) | VERIFIED |
| Exp 1 kappa exact | 0.061 | 0.061 | VERIFIED |
| Exp 1 kappa broad | 0.000 | 0.000 | VERIFIED |
| Exp 2 Exact agreement | 30.6% (n=72 pairs) | 30.6% (22/72) | VERIFIED |
| Exp 2 Broad agreement | 75.0% | 75.0% (54/72) | VERIFIED |
| Exp 2 kappa exact | 0.020 | 0.020 | VERIFIED |
| Exp 2 kappa broad | 0.100 | 0.100 | VERIFIED |
| Exp 3 Exact agreement | 22.2% | 22.2% (16/72) | VERIFIED |
| Exp 3 Broad agreement | 58.3% | 58.3% (42/72) | VERIFIED |
| Exp 3 kappa exact | -0.037 | -0.037 | VERIFIED |
| Exp 3 kappa broad | -0.071 | -0.071 | VERIFIED |

### Table 2 (Vendor Means and Deviations)

| Claim | Manuscript Value | Recomputed Value | Status |
|---|---|---|---|
| Gemini Exp 1 | 88.44 (+9.36) | 88.44 (+9.36) | VERIFIED |
| GPT-5 Nano Exp 1 | 77.33 (-1.75) | 77.33 (-1.75) | VERIFIED |
| Grok 4 Exp 1 | 85.11 (+6.03) | 85.11 (+6.03) | VERIFIED |
| Gemini Exp 2 | 82.33 (-0.79) | 82.33 (-0.79) | VERIFIED |
| GPT-5 Nano Exp 2 | 76.00 (-7.12) | 76.00 (-7.12) | VERIFIED |
| Grok 4 Exp 2 | 83.33 (+0.21) | 83.33 (+0.21) | VERIFIED |
| Gemini Exp 3 | 78.00 (-5.12) | 78.00 (-5.12) | VERIFIED |
| GPT-5 Nano Exp 3 | 69.83 (-13.29) | 69.83 (-13.29) | VERIFIED |
| Grok 4 Exp 3 | 69.50 (-13.62) | 69.50 (-13.62) | VERIFIED |

### ANOVA and Spread Claims

| Claim | Manuscript Value | Recomputed Value | Status |
|---|---|---|---|
| ANOVA F(2,15) | 8.18 | 8.18 | VERIFIED |
| ANOVA p-value | 0.004 | 0.004 | VERIFIED |
| ANOVA eta-squared | 0.522 | 0.522 | VERIFIED |
| 11.9-point spread | 11.9 (84.4 - 72.4) | 11.9 (84.39 - 72.44) | VERIFIED |

### Dispersion Claims

| Claim | Manuscript Value | Recomputed Value | Status |
|---|---|---|---|
| Exp 1 Human within-app SD | 11.37 | 11.37 | VERIFIED |
| Exp 1 LLM within-app SD | 5.78 | 5.78 | VERIFIED |
| Exp 1 reduction | 49% | 49% | VERIFIED |
| Exp 2 reduction | 59% | 59% | VERIFIED |
| LLM range Exp 1 | 2.4 points (82.1-84.6) | 2.4 points (82.11-84.56) | VERIFIED |
| Human range Exp 1 | 18.2 points (71.0-89.2) | 18.2 points (71.0-89.25) | VERIFIED |

### Rank Ordering Claims

| Claim | Manuscript Value | Recomputed Value | Status |
|---|---|---|---|
| Human rank | KELLY > CHRISTINA > DANIEL | 89.25 > 77.0 > 71.0 | VERIFIED |
| Exp 1 LLM rank mismatch | Yes (does not match human) | CHRISTINA (84.56) > KELLY (84.22) > DANIEL (82.11) | VERIFIED |
| Exp 2 LLM rank match | Yes (matches human) | KELLY (82.00) > CHRISTINA (79.11) | VERIFIED |
| Exp 3 LLM rank mismatch | Yes (does not match human) | CHRISTINA (73.33) > KELLY (71.56) | VERIFIED |

### Training Example Range

| Claim | Manuscript Value | Recomputed Value | Status |
|---|---|---|---|
| DANIEL human score range | 61-80 | 61, 66, 77, 80 | VERIFIED |

### Recommendation Distributions (Table S7)

| Claim | Manuscript Value | Recomputed Value | Status |
|---|---|---|---|
| Exp 1 Human: Fund | 4 (33.3%) | 4 (33.3%) | VERIFIED |
| Exp 1 Human: FwR | 3 (25.0%) | 3 (25.0%) | VERIFIED |
| Exp 1 Human: DNF | 5 (41.7%) | 5 (41.7%) | VERIFIED |
| Exp 1 LLM: Fund | 13 (48.1%) | 13 (48.1%) | VERIFIED |
| Exp 1 LLM: FwR | 14 (51.9%) | 14 (51.9%) | VERIFIED |
| Exp 1 LLM: DNF | 0 (0.0%) | 0 (0.0%) | VERIFIED |
| Exp 2 Human: Fund | 4 (50.0%) | 4 (50.0%) | VERIFIED |
| Exp 2 Human: FwR | 2 (25.0%) | 2 (25.0%) | VERIFIED |
| Exp 2 Human: DNF | 2 (25.0%) | 2 (25.0%) | VERIFIED |
| Exp 2 LLM: Fund | 3 (16.7%) | 3 (16.7%) | VERIFIED |
| Exp 2 LLM: FwR | 14 (77.8%) | 14 (77.8%) | VERIFIED |
| Exp 2 LLM: DNF | 1 (5.6%) | 1 (5.6%) | VERIFIED |
| Exp 3 LLM: Fund | 0 (0.0%) | 0 (0.0%) | VERIFIED |
| Exp 3 LLM: FwR | 13 (72.2%) | 13 (72.2%) | VERIFIED |
| Exp 3 LLM: DNF | 5 (27.8%) | 5 (27.8%) | VERIFIED |

### Criterion-Level Tables (S1-S3)

All criterion-level means, standard deviations, t-statistics, uncorrected p-values, and Glass's delta values in Tables S1-S3 were independently recomputed and **verified as correct**. The Holm-Bonferroni corrections were also verified (e.g., Innovation & Impact in Exp 3: 0.031 x 6 = 0.186).

### Per-Vendor Criterion Means (S4-S6)

All per-vendor criterion-level means and standard deviations in Tables S4-S6 were independently recomputed and **verified as correct**. One exception: Table S6 states "n = 6 per vendor" but the GPT-5 Nano Team Strength mean (8.20 +/- 0.84) is actually computed from n=5 due to the missing value (see Minor Concern 6.1).

### Consistency Audit Summary

**Overall assessment:** The reported numbers are remarkably consistent with the raw database. Out of approximately 100+ verified numerical values, only one minor rounding discrepancy was found (Exp 3 p-value: 0.097 vs. recomputed 0.096), and one supplementary table note incorrectly states n=6 when n=5 for one cell. The primary consistency concern is not with the numbers themselves but with the omission of the fourth experimental condition and the misleading total review count.

---

## 8) Statistical Review (Simple-First)

### 8.1 Simple Adequacy

**Study design:** The multi-condition, multi-vendor design is appropriate for the exploratory aims stated. The use of cell-mean aggregation to address pseudoreplication from repeated LLM iterations is a sound methodological choice.

**Primary statistical tests:** Independent-samples t-tests with Glass's delta effect sizes are reasonable for the stated comparisons. The choice of Glass's delta (using human SD as denominator) is well-justified given the unequal variances. One-way ANOVA for the cross-experiment comparison is appropriate given balanced group sizes on the common application base.

**Sample size adequacy:** The manuscript appropriately flags that all analyses are exploratory and underpowered. With effective sample sizes of 9 and 6 LLM observations (after aggregation) compared against 12 and 8 human observations, the study can detect only very large effects. This is honestly reported.

### 8.2 Advanced Considerations

**Bootstrap confidence intervals:** The use of bias-corrected bootstrap (10,000 resamples) for CIs is appropriate for small-sample, potentially non-normal data. However, the discrepancy between the bootstrap CI and parametric p-value in Experiment 3 (CI excludes zero while p > 0.05) requires explicit discussion. This arises because the bootstrap and t-test make different assumptions about the sampling distribution of the mean difference. With n=6 vs. n=8, non-normality (human scores range from 64 to 99 with possible bimodality), and unequal variances, the two methods can legitimately disagree. The authors should state which method they consider primary.

**Cohen's kappa with non-independent pairs:** As noted in Moderate Concern 5.3, the kappa estimates are computed over non-independent pairs. Standard errors for kappa assume independent observations, so the reported point estimates may be biased and their precision is unknowable. Given that all estimates are near zero, the qualitative conclusion (chance-level agreement) is likely robust, but the specific values should not be over-interpreted.

**ANOVA assumptions:** The one-way ANOVA on cell means (n=6 per group, 3 groups) assumes normality and homoscedasticity. With such small groups, normality cannot be verified. The Levene's test for homogeneity of variances was not reported. The ANOVA result (F(2,15) = 8.18, p = 0.004) is verified, but a non-parametric alternative (Kruskal-Wallis) would provide a useful robustness check.

**Multiple comparisons across experiments:** The manuscript does not apply correction for performing three separate experiment-level t-tests (one per experiment). While each experiment addresses a different research question, the simultaneous testing increases the family-wise error rate. This is partially mitigated by the fact that none of the individual tests reach significance at alpha = 0.05, but the principle should be acknowledged.

**Variance ratio terminology:** Section 2.5 refers to "the approximately 2.5-fold variance difference." The SD ratio is approximately 2.5 (13.32/5.24 = 2.54), but the variance ratio is approximately 6.5. The manuscript should use "standard deviation" rather than "variance" here.

---

## 9) Supplementary Materials Assessment

### Prompt Templates (S1.1-S1.3)

The prompt templates are well-documented and clearly annotated, making the experimental conditions reproducible. The annotation style (explaining what differs between conditions) is particularly helpful. One minor gap: the JSON output format in S1.1 shows `"Fund" | "Fund with Revisions" | "Do Not Fund"` using pipe notation that is not valid JSON; it would be more precise to show this as separate example values, though this is unlikely to have affected LLM behavior.

### Statistical Tables (S2-S3)

Tables S1-S3 (criterion-level comparisons) and S4-S6 (per-vendor means) are verified against the database. The tables are clearly labeled and include appropriate notes. The Holm-Bonferroni correction is correctly applied.

**Gap:** No table reports the criterion-level analysis for the missing Team Strength value. The note about n=6 per vendor in Table S6 is inaccurate for the GPT-5 Nano Team Strength cell (n=5).

### Recommendation Distributions (S4)

Table S7 is verified. The note explaining that Experiments 2-3 share the same human comparison group is appropriate.

### API Configuration (S5)

Table S8 provides sufficient detail for reproducibility. The note about the temperature discrepancy between vendors is appropriately flagged.

### Missing from Supplementary Materials

1. **Prompt template for `with_training_data_v1`:** This condition exists in the database and has a corresponding prompt file on disk but is not included in the supplementary materials.
2. **Correlation structure of human reviews:** An ICC or variance-components analysis of the human reviews (4 reviewers x 3 applications) would help readers assess the reliability of the reference standard.
3. **Individual LLM scores for the training application (DANIEL) in Experiments 2-3:** These exist in the database and would serve as a calibration fidelity check.

---

## 10) Claims That Overreach the Evidence

### 10.1 "Few-shot prompting produced scores closest to human reviewers"

While numerically accurate (-2.57 vs. +4.55 and -10.68), this characterization implies that the multi-example few-shot approach is categorically superior. The unreported single-example condition produced a +1.82 deviation on the same base, which is numerically smaller in absolute terms. Without reporting all conditions, the claim that multi-example few-shot is "best" is incomplete.

### 10.2 "LLMs demonstrated 49-59% lower score dispersion than humans"

This is presented as a finding about LLM behavior, but one-third of LLMs used temperature = 0.1 (Grok), which mechanistically reduces output variability. The claim conflates an engineered property (low temperature) with an observed behavioral difference. Without vendor-level dispersion analysis, the claim cannot be attributed to LLMs generally.

### 10.3 "Prompt engineering substantially affects LLM scoring behavior"

This claim is supported by the significant ANOVA (p = 0.004) but is confounded with the fact that only two applications contribute to the comparison. The 11.9-point spread could, in principle, reflect application-specific interactions with prompt conditions rather than a general prompt engineering effect. The manuscript's own limitations section acknowledges this, but the abstract and discussion state the claim more strongly than the evidence supports.

### 10.4 "One speculative explanation is that LLMs may prioritize explicit instructions over the calibrating influence of training examples"

This mechanistic interpretation, labeled as "speculative," is appropriately hedged in the discussion but implies a level of understanding about LLM internal processing that the behavioral data cannot support. The authors do qualify this with "this mechanistic interpretation cannot be confirmed from our behavioral data alone," which is commendable, but the framing still invites readers to accept the mechanism as plausible.

---

## 11) Priority Revisions Before Reconsideration

Listed in order of priority:

1. **Disclose the fourth experimental condition** (`with_training_data_v1`). Either report it as an additional experiment or provide a transparent explanation for its exclusion. This is the most significant revision needed and directly affects the manuscript's credibility regarding selective reporting.

2. **Correct the total LLM review count.** Replace "yielded 63 total LLM reviews" with accurate language distinguishing reviews generated from reviews analyzed. Report that 81 reviews were generated across three experiments (or 108 across four conditions), with 63 included in the primary analyses.

3. **Reconcile the bootstrap CI and parametric p-value discrepancy** in Experiment 3. Provide an explicit statistical explanation and state which inference method is considered primary.

4. **Correct the variance/standard deviation terminology** in Section 2.5. "2.5-fold variance difference" should read "2.5-fold standard deviation difference."

5. **Correct the Table S6 note** regarding n=6 per vendor for Team Strength (GPT-5 Nano has n=5 due to the missing value).

6. **Add a vendor-level dispersion analysis** (or at minimum vendor-specific within-applicant SDs) to disentangle the temperature confound from the general LLM dispersion finding.

7. **Provide the FC1/FC2/FC3 to KELLY/CHRISTINA/DANIEL mapping** in the supplementary materials or data availability section.

8. **Report the LLM scores on DANIEL in Experiments 2-3** as a calibration fidelity check (how closely did LLMs match the training application's known score range?).

9. **Temper the abstract language** regarding "best alignment" and "consistency" claims to reflect the full set of conditions run and the temperature confound.

10. **Consider reporting a robustness check** using Kruskal-Wallis for the ANOVA and/or reporting Levene's test for homogeneity of variances.

---

*End of review.*
