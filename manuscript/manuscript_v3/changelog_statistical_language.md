# Statistical Language Simplification — Change Log

Use this file to update the Word document. Each section below shows the location, what changed, and the new text to insert.

---

## 1. Section 2.5 — Statistical Analysis, Paragraph 1

**Location in Word doc:** First paragraph under "2.5 Statistical Analysis"

**What changed:** Replaced "pseudoreplication" with a plain-language explanation; replaced "cell means" with "averaged scores"; restructured the Glass's Δ explanation to lead with the rationale; minor sentence restructuring throughout.

**New text:**

> Given the small sample size (n = 3 applications) and the nested structure of the data, all statistical analyses should be interpreted as exploratory rather than confirmatory. Because each LLM produced three non-independent repeated outputs per application, these iterations were averaged within each vendor-application combination to yield a single representative score, resulting in 9 independent LLM observations in Experiment 1 (3 vendors × 3 applications) and 6 in each of Experiments 2 and 3 (3 vendors × 2 applications). Within-experiment t-tests compared these averaged LLM scores against individual human scores. Effect sizes were calculated using Glass's Δ, which uses the human group's standard deviation as the baseline; this measure was chosen because LLM scores showed roughly 2.5 times less variability than human scores. We report 95% confidence intervals for mean differences; confidence intervals for Glass's Δ were computed via bias-corrected bootstrap (10,000 resamples).

---

## 2. Section 2.5 — Statistical Analysis, Paragraph 2

**Location in Word doc:** Second paragraph under "2.5 Statistical Analysis"

**What changed:** Replaced "within-reviewer correlation that is not modeled" → "correlation among scores from the same reviewer that the t-tests do not account for"; replaced "Cell means" → "averaged scores" in ANOVA sentence; replaced "designated as exploratory" → "exploratory"; added brief gloss for Holm-Bonferroni ("to control for multiple comparisons across the six scoring criteria"); added parenthetical "a chance-corrected measure of agreement" after Cohen's κ.

**New text:**

> Human scores are treated as independent observations in the t-tests, though the four reviewers each scored all applications, introducing correlation among scores from the same reviewer that the t-tests do not account for; this may reduce effective degrees of freedom below nominal values. To compare LLM scores across prompt conditions, a one-way ANOVA was restricted to the two applications common to all experiments (FC1 and FC2) to ensure balanced group sizes. Criterion-level analyses are exploratory; to control for multiple comparisons across the six scoring criteria within each experiment, Holm-Bonferroni correction was applied, and both uncorrected and corrected p-values are reported. Recommendation agreement was assessed using Cohen's κ, a chance-corrected measure of agreement, at both the exact category level (Fund/Fund with Revisions/Do Not Fund) and the broad level (positive vs. negative funding direction), computed over all human-LLM review pairs within each application. Analyses were conducted in Python 3.13 using the following python packages: scipy, scikit-learn, and pandas.

---

## 3. Section 3.1 — Overall Score Alignment

**Location in Word doc:** Paragraph under "3.1 Overall Score Alignment," before Table 1

**What changed:** Replaced "cell means (aggregated across 3 iterations) to address pseudoreplication" with simpler reference; broke the single dense paragraph into separate paragraphs (one per experiment + one for ANOVA); simplified the bootstrap vs. t-test discrepancy explanation; replaced "cell means" with "averaged LLM scores" in the ANOVA sentence.

**New text:**

> Table 1 summarizes results across all three experiments. All LLM statistics use averaged scores (aggregated across 3 iterations per vendor-application combination) as described in Section 2.5.
>
> In the zero-shot condition (Experiment 1), LLMs scored applications 4.55 points higher than humans (83.63 ± 5.24 vs. 79.08 ± 13.32; p = 0.347, Glass's Δ = 0.34, 95% CI [-0.28, 1.18]), indicating moderate optimism bias.
>
> Few-shot prompting (Experiment 2) achieved the best alignment, with LLMs scoring 2.57 points below humans (80.56 ± 4.81 vs. 83.13 ± 13.73; p = 0.671, Glass's Δ = -0.19, 95% CI [-1.44, 0.59]), a non-significant difference representing approximately 3% of the total scale.
>
> Adding strict instructions (Experiment 3) produced substantial under-scoring, with LLMs scoring 10.68 points below humans (72.44 ± 4.98 vs. 83.13 ± 13.73; p = 0.097, Glass's Δ = -0.78, 95% CI [-2.61, -0.08]). This trend did not reach statistical significance; notably, the bootstrap confidence interval for the mean difference ([-20.11, -1.03]) excludes zero while the parametric p-value does not, a discrepancy that reflects the different assumptions of each method, which can diverge with small samples.
>
> One-way ANOVA restricted to the common application base (FC1 and FC2 only, n = 6 per experiment) confirmed significant differences in averaged LLM scores across prompt conditions (F(2,15) = 8.18, p = 0.004, η² = 0.522).

---

## 4. Table 1 Note

**Location in Word doc:** Note below Table 1

**What changed:** Replaced "aggregated by averaging 3 iterations within each vendor-application cell" → "averaged across 3 iterations within each vendor-application combination"; replaced "reference denominator" → "baseline."

**New text:**

> Note: LLM scores were averaged across 3 iterations within each vendor-application combination before statistical testing. Glass's Δ uses the human SD as the baseline. 95% CIs computed via bias-corrected bootstrap (10,000 resamples). Agreement percentages and Cohen's κ are computed over all human-LLM review pairs per application (n = 108 pairs for Exp 1; n = 72 for Exps 2–3). Bold indicates best alignment.

---

## 5. Section 3.4 — Recommendation Agreement, Paragraph 1

**Location in Word doc:** First paragraph under "3.4 Recommendation Agreement and Consistency"

**What changed:** Replaced "human-LLM pairs are non-independent (each human review is crossed with multiple LLM reviews), which may bias point estimates" → "each human review is paired with multiple LLM reviews, creating non-independent pairs that may affect the estimates"; replaced "base-rate overlap rather than systematic concordance" → "chance overlap in how often each group chose the same category rather than true systematic agreement."

**New text:**

> Pair-level exact recommendation agreement ranged from 22.2% to 33.3% across experiments, but Cohen's κ values were near zero (exact κ: 0.061, 0.020, -0.037; broad κ: 0.000, 0.100, -0.071 for Experiments 1–3), indicating agreement at or below chance levels. These κ estimates should be interpreted cautiously because each human review is paired with multiple LLM reviews, creating non-independent pairs that may affect the estimates. LLMs consistently favored "Fund with Revisions" (52–78%) compared to humans (25%). In the zero-shot condition, LLMs generated zero "Do Not Fund" recommendations; strict instructions increased this to 27.8% but at the cost of zero "Fund" recommendations. Broad pair-level agreement was highest in Experiment 2 (75.0%) compared to 58.3% in Experiments 1 and 3, though κ values indicate this largely reflects chance overlap in how often each group chose the same category rather than true systematic agreement.

---

## 6. Section 3.4 — LLM Score Variability, Paragraph 2

**Location in Word doc:** Second paragraph under "3.4 Recommendation Agreement and Consistency"

**What changed:** Replaced "score dispersion" → "score variability"; replaced "range restriction" → "a compressed scoring range."

**New text:**

> LLMs demonstrated substantially lower score variability across all conditions, with average within-applicant standard deviations of 5.18–5.78 points compared to 11.37–12.56 for humans, representing a 49% reduction in Experiment 1 and 59% in Experiments 2–3. However, this lower variability likely reflects a compressed scoring range rather than superior consistency. LLMs did not consistently differentiate between applications: in Experiment 1, LLMs ranked all three applications within a narrow 2.4-point range (82.1–84.6) while humans distinguished a wider 18.2-point spread (71.0–89.2). LLMs matched the human rank ordering of applications only in Experiment 2.

---

## 7. Section 4 — Discussion, Paragraph 1

**Location in Word doc:** First paragraph under "4 Discussion"

**What changed:** Replaced "after accounting for pseudoreplication" → "after accounting for repeated iterations."

**Find and replace this phrase:**

- OLD: "after accounting for pseudoreplication"
- NEW: "after accounting for repeated iterations"

---

## 8. Section 4 — Discussion, Paragraph 2 (Strict Instructions)

**Location in Word doc:** Second paragraph of Discussion, starting "The counterproductive effect..."

**What changed:** Replaced "after correcting for pseudoreplication" → "after accounting for repeated iterations"; replaced "a pattern described as instruction compliance bias" → "a tendency sometimes described as instruction compliance bias"; removed "mechanistic" and "behavioral."

**New text:**

> The counterproductive effect of strict instructions (Experiment 3) is noteworthy. Adding directives to "be critical" shifted LLM scores from near-alignment to substantial under-scoring (10.68 points below human mean), though this difference did not reach statistical significance after accounting for repeated iterations (p = 0.097). One speculative explanation is that LLMs may prioritize explicit instructions over the calibrating influence of training examples, a tendency sometimes described as instruction compliance bias (12); however, this interpretation cannot be confirmed from our data alone. If replicated, this pattern would suggest that providing examples of desired scoring behavior may be more effective than directive language for calibrating LLM outputs.

---

## 9. Section 4 — Discussion, Paragraph 3 (Score vs. Recommendation Gap)

**Location in Word doc:** Third paragraph of Discussion, starting with the sentence about dissociation/gap

**What changed:** Replaced "The persistent dissociation between score alignment and recommendation agreement" → "The gap between how well scores aligned and how poorly recommendations agreed"; replaced "attributable to base-rate overlap rather than systematic concordance" → "largely due to chance overlap rather than true concordance"; replaced "Score-to-recommendation mapping" → "The mapping from scores to funding recommendations."

**New text:**

> The gap between how well scores aligned and how poorly recommendations agreed warrants attention. Even in the best-aligned condition, LLMs overwhelmingly favored "Fund with Revisions" (77.8% in Experiment 2 vs. 25% for humans), achieved only 30.6% pair-level exact agreement, and produced near-zero chance-corrected agreement (Cohen's κ: -0.04 to 0.10 across experiments), indicating that the observed agreement was largely due to chance overlap rather than true concordance. LLMs may default to intermediate options when uncertain, consistent with documented ambiguity aversion in AI systems (13). The mapping from scores to funding recommendations likely involves implicit thresholds that LLMs cannot infer from rubrics alone.

---

## 10. Section 4.1 — Limitations, Paragraph 2 (Few-Shot Training)

**Location in Word doc:** Second paragraph of Limitations, starting "The few-shot training examples..."

**What changed:** Replaced "This design confounds general scoring calibration with application-specific anchoring; the improved alignment...rather than learning generalizable scoring behavior" → "This makes it difficult to determine whether the LLM learned general scoring behavior or simply anchored to that particular application's score range; the improved alignment...could reflect either mechanism"; replaced "disentangle" → "separate."

**New text:**

> The few-shot training examples in Experiments 2 and 3 were derived from reviews of a single application (FC3), with human scores ranging from 61 to 80 points. This makes it difficult to determine whether the LLM learned general scoring behavior or simply anchored to that particular application's score range; the improved alignment in Experiment 2 could reflect either mechanism. Future studies should use training examples drawn from multiple applications to separate these effects.

---

## 11. Section 4.1 — Limitations, Paragraph 3 (Nested Data)

**Location in Word doc:** Third paragraph of Limitations, starting "Additionally..."

**What changed:** Replaced "pseudoreplication was addressed on the LLM side through cell-mean aggregation" → "repeated LLM iterations were addressed through averaging"; replaced "within-reviewer correlation that the t-tests do not model" → "correlation among scores from the same reviewer that the t-tests do not account for"; replaced "bias kappa point estimates" → "affect the κ estimates"; replaced "qualitative conclusion" → "overall conclusion."

**New text:**

> Additionally, while repeated LLM iterations were addressed through averaging, human scores remain nested within four reviewers who each scored all applications, introducing correlation among scores from the same reviewer that the t-tests do not account for. Cohen's κ was computed over all human-LLM review pairs per application, creating non-independent pairs that may affect the κ estimates; however, given that all κ values were near zero, this is unlikely to change the overall conclusion of chance-level agreement.

---

## 12. Section 4.1 — Limitations, Paragraph 4 (Dispersion)

**Location in Word doc:** Fourth paragraph of Limitations, starting "The observed 49–59%..."

**What changed:** Replaced "score dispersion" → "score variability"; replaced "range restriction and reduced sensitivity to application quality" → "a narrower scoring range and reduced sensitivity to differences in application quality."

**New text:**

> The observed 49–59% reduction in LLM score variability should be interpreted cautiously. LLMs compressed scores into a narrow range and failed to rank applications in the same order as humans in two of three experiments, suggesting that this lower variability reflects a narrower scoring range and reduced sensitivity to differences in application quality rather than superior consistency.

---

## 13. Section 4.2 — Implications, Sentence 2

**Location in Word doc:** Second sentence of "4.2 Implications and Future Directions"

**What changed:** Replaced "the persistent dissociation between score calibration and recommendation agreement" → "the gap between score calibration and recommendation agreement."

**Find and replace this phrase:**

- OLD: "the persistent dissociation between score calibration and recommendation agreement"
- NEW: "the gap between score calibration and recommendation agreement"
