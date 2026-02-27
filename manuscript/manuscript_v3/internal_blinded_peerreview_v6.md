# Blinded Peer Review: Internal Consistency and Methods Audit

**Manuscript:** "Evaluating Large Language Models as Grant Reviewers: A Comparative Study of Prompt Engineering Strategies"

**Review Type:** FULL_METHODS + CONSISTENCY_AUDIT

**Date:** 2026-02-27

---

## 0) Material Inventory and Review Scope

**Study type:** Multi-condition, multi-vendor comparative evaluation (exploratory pilot)

**Article type:** Brief report / short communication

**Primary claims:**
1. Few-shot prompting produces the best alignment between LLM and human grant review scores.
2. Prompt engineering strategy significantly affects LLM scoring behavior (ANOVA on common application base).
3. LLMs show lower score dispersion than humans but fail to reproduce human rank ordering of applications.
4. Recommendation-level agreement is at or below chance across all conditions.

**Material provided:**
- Main manuscript with Abstract, Introduction, Method, Results, Discussion, Limitations, References
- Two tables in main text (Table 1: summary results; Table 2: vendor deviations)
- Supplementary materials with prompt templates (S1.1-S1.3), criterion-level tables (S1-S3), per-vendor criterion tables (S4-S6), recommendation distributions (S7), and API configuration (S8)
- Raw SQLite database with 12 human reviews and 81 LLM reviews

**Missing or absent sections:**
- No formal power analysis or sample size justification (acknowledged as exploratory)
- No formal ethics statement beyond IRB protocol number (non-human subjects)
- No CONSORT, STROBE, or similar reporting checklist cited
- No preregistration (acknowledged)
- No figure or visual display of data distributions (e.g., box plots, scatter plots)
- No raw data appendix showing individual LLM review scores, only aggregated summaries
- No description of how the one missing criterion-level value was handled in total score computation (though the manuscript states the total score was still produced)

---

## 1) Overall Recommendation

**Major Revision**

The manuscript is methodologically competent for an explicitly exploratory pilot study. The statistical framework (cell-mean aggregation, Glass's delta, bootstrap CIs, Holm correction) is appropriate for the design, and the authors exercise commendable restraint in interpretation. However, several moderate-to-major concerns limit the contribution: (a) the confound between few-shot calibration and application-specific anchoring is fundamental and undercuts the primary claim, (b) the kappa computation over non-independent pairs is methodologically problematic and likely inflates the number of informative data points, (c) the absence of any formal discussion of how the non-uniform temperature settings affect cross-vendor comparisons weakens the vendor-level analyses, and (d) several presentation choices obscure the degree to which the results are driven by just two or three applications. A revision that addresses the analytic confounds, adds appropriate caveats, and improves transparency about the data structure would make a worthwhile contribution to the emerging literature on LLM applications in research evaluation.

---

## 2) Summary Assessment

This manuscript reports an exploratory pilot comparing three prompt engineering strategies for LLM-generated grant reviews against human expert reviews, using three seed grant applications. The study design is sensible and the statistical approach -- aggregating LLM iterations into cell means before testing, using Glass's delta with the human SD as denominator, and applying bootstrap confidence intervals -- is appropriate for the nested, unbalanced data structure. The internal consistency audit against the raw database confirms that all reported numerical values are accurate: means, standard deviations, t-statistics, p-values, Glass's deltas, ANOVA results, recommendation distributions, and agreement metrics all reproduce from the source data within rounding tolerance. The main limitation is inherent to the design: with only three applications (two in the primary comparison for Experiments 2-3), application-specific effects are entirely confounded with any generalizable prompt engineering effects, and this is only partially acknowledged in the current text. The discussion appropriately hedges most claims, but the abstract and some results language could more clearly convey that the findings describe a case study rather than a generalizable experiment.

---

## 3) Fatal Flaws

No fatal flaws were identified. The study is explicitly framed as exploratory, sample sizes are transparently reported, and no confirmatory inferential claims are made. The numerical accuracy of reported statistics is excellent.

---

## 4) Major Concerns

### 4.1 Confound Between Few-Shot Calibration and Application-Specific Anchoring (Design)

The manuscript acknowledges (Section 4.1) that training examples from a single application (FC3/DANIEL, range 61-80) may anchor LLM scoring to that application's score range rather than teaching generalizable calibration. This is the study's most fundamental limitation, yet it receives only one paragraph in the limitations section. The improved alignment in Experiment 2 could be entirely explained by the training scores (mean ~71) pulling LLM outputs toward the mid-range of the scale, which happens to overlap with the human mean for the remaining two applications (83.1). The manuscript should more prominently frame this alternative explanation -- ideally in the Results section itself, not only in the Discussion -- and should explicitly state that the design cannot distinguish these two mechanisms. As written, the abstract states that "few-shot prompting produced scores closest to human reviewers" without immediate qualification, which a reader could reasonably interpret as evidence of calibration rather than anchoring.

### 4.2 Non-Independent Pairs in Kappa Computation (Statistical)

The manuscript computes Cohen's kappa over all human-LLM review pairs per application (n = 108 pairs for Experiment 1, n = 72 for Experiments 2-3). This creates severe non-independence: each human review is paired with 9 LLM reviews (3 vendors x 3 iterations), and each LLM review is paired with 4 human reviews. Cohen's kappa assumes independent rater pairs, and violating this assumption inflates the effective sample size and can bias the point estimate. The manuscript acknowledges this in Section 4.1 but dismisses it by noting that kappa values are near zero. While the qualitative conclusion (chance-level agreement) is likely robust, the specific kappa point estimates (0.061, 0.020, -0.037 for exact; 0.000, 0.100, -0.071 for broad) should not be interpreted at face precision. The appropriate approach would be to either (a) compute kappa on a reduced set of non-overlapping pairs, (b) use a multi-rater agreement statistic (e.g., Fleiss' kappa or Krippendorff's alpha), or (c) report only the raw agreement percentages with a clear caveat that no valid chance-corrected statistic can be computed from this pair structure.

### 4.3 Confounded Vendor Comparison Due to Temperature Settings (Design)

xAI Grok used temperature = 0.1, while OpenAI and Google used the default of 1.0. This 10-fold difference in sampling temperature directly affects output variability and potentially score distributions. The manuscript notes this in Section 2.4 and mentions it as a possible contributor to reduced variability. However, Table 2 and Section 3.3 present vendor comparisons without adjusting for or conditioning on this confound. The claim that "xAI Grok achieved the closest alignment with human scores (+0.21 points)" in Experiment 2 could be partly or wholly attributable to the temperature setting rather than model capability. This confound should be explicitly flagged alongside every vendor comparison, not just mentioned once in the methods.

---

## 5) Moderate Concerns

### 5.1 Human Score Non-Independence Not Modeled (Statistical)

Four reviewers each scored all three applications, creating a fully crossed design with within-reviewer correlation. The t-tests treat the 12 (or 8) human scores as independent observations. The manuscript acknowledges this (Section 2.5) but does not estimate the magnitude of the bias. With only 4 reviewers, the effective degrees of freedom could be substantially lower than the nominal values (e.g., df = 19 in Experiment 1 could be closer to df = 6-10 depending on the intraclass correlation). While p-values are already non-significant, this issue affects the stated confidence intervals for mean differences and Glass's delta. The authors should either (a) fit a mixed model with reviewer as a random effect (even acknowledging it may be unstable with n = 4), (b) compute the intraclass correlation among human reviewers and report the design effect, or (c) at minimum, provide a sensitivity analysis showing how results change if reviewer-level means (n = 4) are used instead of individual scores (n = 12).

### 5.2 ANOVA on FC1+FC2 Only: Limited Generalizability

The balanced ANOVA (F(2,15) = 8.18, p = 0.004, eta-squared = 0.522) is the only formally significant result in the manuscript and uses cell means from FC1 and FC2 only. With only two applications, this test is comparing prompt condition effects on a 2-application base. The significant result is technically correct (verified against raw data), but the large eta-squared (52.2% of variance explained) should be interpreted cautiously: with only 2 applications and 3 vendors, idiosyncratic application-vendor interactions could drive much of this effect. The manuscript should more explicitly note that this ANOVA tests whether prompt conditions shift LLM scores, not whether the shifts improve alignment with human judgment. The latter interpretation requires the comparison to human scores, which is not directly tested in the ANOVA.

### 5.3 "81 LLM Reviews Generated, 63 Entered Analyses" Framing

The manuscript states that 81 LLM reviews were generated and 63 entered the primary analyses. This is arithmetically correct (27 in Exp 1 + 18 in Exp 2 + 18 in Exp 3 = 63). However, the phrasing could mislead readers into thinking 18 reviews were excluded for quality or other post-hoc reasons. In fact, 27 reviews per experiment were generated across all three experiments (81 total), and the 18 "excluded" reviews in Experiments 2-3 are the DANIEL/FC3 reviews removed by design (to prevent data contamination). This should be stated more clearly -- e.g., "63 entered primary analyses after excluding the training application by design" -- to avoid any implication of selective reporting.

### 5.4 Absence of Distributional Visualizations

The manuscript presents no figures -- no box plots, scatter plots, or forest plots. For a study where the central claim concerns distributional properties (range restriction, score compression, rank ordering), visual displays would substantially aid interpretation and allow readers to assess the data structure directly. At minimum, a figure showing human vs. LLM score distributions by experiment (and ideally by application within experiment) should be provided.

---

## 6) Minor Concerns

### 6.1 Rounding Convention for Human Mean

The human mean for FC1+FC2 is 665/8 = 83.125, reported as 83.13 throughout. This is technically correct rounding to two decimal places, but "83.12" would be equally defensible depending on the rounding convention used (round-half-to-even vs. round-half-up). The manuscript should apply a consistent convention and note it if non-standard.

### 6.2 Table S6 Note on Missing Value

Table S6 notes "GPT-5 Nano Team Strength (n = 5 due to one missing criterion-level value)" but does not explain how this missing value affects the cell mean used in Table S3. The database confirms that the OpenAI-KELLY cell mean for Team Strength in Experiment 3 is based on 2 of 3 iterations (mean = 9.00). This should be explicitly stated in the supplementary note for Table S3 as well.

### 6.3 Inconsistent Precision in Reporting

Some values are reported to one decimal (e.g., "11.9-point spread"), others to two decimals (e.g., "83.63 +/- 5.24"), and kappa values to three decimals (e.g., "0.061"). While none of these are incorrect, adopting a uniform precision convention within each statistic type would improve readability.

### 6.4 "Fund with Revisions" Percentage Range

Section 3.4 states LLMs "consistently favored 'Fund with Revisions' (52-78%)." These percentages are derived from the analysis subsets (Exp 1: 14/27 = 51.9%; Exp 2: 14/18 = 77.8%; Exp 3: 13/18 = 72.2%). The range "52-78%" omits the fact that Experiment 3 falls at 72.2%, which is within range but the inclusive upper bound comes from Experiment 2, not Experiment 3. This is not incorrect but could be more precisely stated as "52-78% across conditions."

### 6.5 Reference to "Instruction Compliance Bias"

Section 4 cites Perez et al. (2022, ref. 12) in support of "instruction compliance bias." This reference describes model-written evaluations for discovering LLM behaviors, not instruction compliance bias per se. The term "instruction compliance bias" does not appear in that paper. The authors should either find a more directly relevant citation or explicitly mark this as their own interpretive framing.

### 6.6 Software Version Reporting

The manuscript reports "scipy 1.11, scikit-learn 1.6, and pandas 2.1." These should be reported to the patch version level (e.g., scipy 1.11.x) to ensure reproducibility, as minor versions can affect numerical results in edge cases.

---

## 7) Internal Consistency Audit

All numerical values reported in the manuscript and supplementary materials were verified against the raw SQLite database. The audit covered:

**Verified CORRECT:**

| Claim | Manuscript Value | Database Value | Status |
|-------|-----------------|----------------|--------|
| Total human reviews | 12 | 12 | MATCH |
| Total LLM reviews | 81 | 81 | MATCH |
| LLM reviews in analyses | 63 | 27+18+18=63 | MATCH |
| Human mean (all 12) | 79.08 +/- 13.32 | 79.08 +/- 13.32 | MATCH |
| Human mean (FC1+FC2) | 83.13 +/- 13.73 | 83.125 +/- 13.73 | MATCH (rounding) |
| Exp 1 LLM mean | 83.63 +/- 5.24 | 83.63 +/- 5.24 | MATCH |
| Exp 1 difference | +4.55 | +4.55 | MATCH |
| Exp 1 p-value | 0.347 | 0.347 | MATCH |
| Exp 1 Glass's delta | 0.34 | 0.34 | MATCH |
| Exp 2 LLM mean | 80.56 +/- 4.81 | 80.56 +/- 4.81 | MATCH |
| Exp 2 difference | -2.57 | -2.57 | MATCH |
| Exp 2 p-value | 0.671 | 0.671 | MATCH |
| Exp 2 Glass's delta | -0.19 | -0.19 | MATCH |
| Exp 3 LLM mean | 72.44 +/- 4.98 | 72.44 +/- 4.98 | MATCH |
| Exp 3 difference | -10.68 | -10.68 | MATCH |
| Exp 3 p-value | 0.097 | 0.096 | MATCH (rounding) |
| Exp 3 Glass's delta | -0.78 | -0.78 | MATCH |
| ANOVA F(2,15) | 8.18 | 8.18 | MATCH |
| ANOVA p | 0.004 | 0.004 | MATCH |
| ANOVA eta-squared | 0.522 | 0.522 | MATCH |
| 11.9-point spread | 84.4 to 72.4 = 11.9 | 84.39 to 72.44 = 11.95 | MATCH (rounding) |
| Exp 1 LLM app range | 82.1-84.6 (2.4 pts) | 82.11-84.56 (2.44 pts) | MATCH (rounding) |
| Human app range | 71.0-89.2 (18.2 pts) | 71.0-89.25 (18.25 pts) | MATCH (rounding) |
| Training example range | 61-80 | 61-80 | MATCH |
| Gemini Exp 1 | 88.44 (+9.36) | 88.44 (+9.36) | MATCH |
| GPT-5 Exp 1 | 77.33 (-1.75) | 77.33 (-1.75) | MATCH |
| Grok Exp 1 | 85.11 (+6.03) | 85.11 (+6.03) | MATCH |
| Gemini Exp 2 | 82.33 (-0.79) | 82.33 (-0.79) | MATCH |
| GPT-5 Exp 2 | 76.00 (-7.12) | 76.00 (-7.12) | MATCH |
| Grok Exp 2 | 83.33 (+0.21) | 83.33 (+0.21) | MATCH |
| Gemini Exp 3 | 78.00 (-5.12) | 78.00 (-5.12) | MATCH |
| GPT-5 Exp 3 | 69.83 (-13.29) | 69.83 (-13.29) | MATCH |
| Grok Exp 3 | 69.50 (-13.62) | 69.50 (-13.62) | MATCH |
| Within-applicant SD reduction Exp 1 | 49% | 49% (11.37 to 5.78) | MATCH |
| Within-applicant SD reduction Exps 2-3 | 59% | 59% (12.56 to 5.18) | MATCH |
| Exact agreement Exp 1 | 33.3% | 36/108 = 33.3% | MATCH |
| Exact agreement Exp 2 | 30.6% | 22/72 = 30.6% | MATCH |
| Exact agreement Exp 3 | 22.2% | 16/72 = 22.2% | MATCH |
| Broad agreement Exp 1 | 58.3% | 63/108 = 58.3% | MATCH |
| Broad agreement Exp 2 | 75.0% | 54/72 = 75.0% | MATCH |
| Broad agreement Exp 3 | 58.3% | 42/72 = 58.3% | MATCH |
| Kappa exact Exp 1 | 0.061 | 0.061 | MATCH |
| Kappa exact Exp 2 | 0.020 | 0.020 | MATCH |
| Kappa exact Exp 3 | -0.037 | -0.037 | MATCH |
| Kappa broad Exp 1 | 0.000 | 0.000 | MATCH |
| Kappa broad Exp 2 | 0.100 | 0.100 | MATCH |
| Kappa broad Exp 3 | -0.071 | -0.071 | MATCH |
| Exp 1 LLM 0 DNF | 0 | 0 | MATCH |
| Exp 3 LLM 0 Fund | 0 | 0 | MATCH |
| Exp 3 LLM 27.8% DNF | 27.8% | 5/18 = 27.8% | MATCH |
| Missing criterion: Team Strength | 1 review | KELLY/OpenAI/iter1/strict | MATCH |
| 4 human reviewers x 3 apps | Fully crossed | Confirmed (AM, SW, HW, Y) | MATCH |
| Human reviewer IDs in training data | AM, SW, HW, Y | AM, SW, HW, Y | MATCH |
| LLM rank matches human in Exp 2 only | Exp 2 only | KELLY > CHRISTINA > DANIEL in both | MATCH |

**Supplementary Tables S1-S3 (criterion-level):** All means, SDs, differences, t-statistics, uncorrected p-values, and Glass's deltas verified to match within rounding tolerance. Holm-Bonferroni corrections verified for all three experiments.

**Supplementary Tables S4-S6 (per-vendor criterion):** All per-vendor criterion means and SDs verified to match within rounding tolerance. The n=5 annotation for GPT-5 Nano Team Strength in Table S6 is confirmed correct.

**Supplementary Table S7 (recommendations):** All frequencies and percentages verified exactly against database.

**Overall consistency verdict:** The manuscript demonstrates excellent numerical accuracy. No discrepancies between reported values and the raw database were identified. All rounding is within acceptable tolerance (< 0.01 on any reported value).

---

## 8) Statistical Review (Simple-First)

### 8.1 Simple Adequacy

**Appropriate choices:**
- Cell-mean aggregation to address pseudoreplication from repeated LLM iterations is sound and conservative.
- Glass's delta with human SD as denominator is the correct effect size choice given the ~2.5x SD difference between groups.
- Bias-corrected bootstrap CIs (10,000 resamples) are appropriate for small, potentially non-normal samples.
- Holm-Bonferroni correction for criterion-level multiple comparisons is adequate and correctly implemented.
- Welch's t-test (or equivalent) for unequal variances is appropriate given the SD asymmetry.

**Concerns:**
- The t-tests assume independence of observations within each group. On the LLM side, cell-mean aggregation addresses this. On the human side, the 4 reviewers create a crossed structure that is not modeled (see Section 5.1).
- The ANOVA uses cell means from only 2 applications. With n = 6 per group (3 vendors x 2 applications) and only 2 applications, application is confounded with any within-application effects. An ANOVA with application as a factor would be more informative but is underpowered.
- No effect size CI is reported for the ANOVA eta-squared. Given the small sample, the sampling distribution of eta-squared is wide, and the point estimate of 0.522 could be compatible with population values ranging from small to very large.

### 8.2 Advanced Considerations

- The manuscript appropriately avoids mixed-effects models, which would be unstable with n = 3 applications and n = 4 reviewers. However, acknowledging the ideal analysis (crossed random effects for reviewer and application) and explaining why it was not feasible would strengthen the methods section.
- The bootstrap CI for the Experiment 3 mean difference excludes zero ([-20.11, -1.03]) while the parametric p-value does not reach significance (p = 0.097). The manuscript provides a reasonable explanation for this discrepancy (different distributional assumptions). This is a genuine methodological point and is handled transparently.
- Cohen's kappa computed over non-independent pairs (see Major Concern 4.2) does not have known statistical properties. The standard error and confidence interval for kappa are undefined under this pair structure, so the point estimates should be treated as rough descriptive summaries only.

---

## 9) Supplementary Materials Assessment

**Strengths:**
- Complete prompt templates for all three conditions are provided, enabling replication.
- The progressive annotation showing additions relative to previous conditions (S1.2, S1.3) is clear and helpful.
- API configuration details (Table S8) include model IDs, API versions, and temperature settings.
- Criterion-level tables (S1-S3) include both uncorrected and Holm-corrected p-values, which is best practice.

**Concerns:**
- The per-vendor criterion tables (S4-S6) report raw LLM scores (not cell means), which is inconsistent with the main analysis approach. The note "Values represent raw LLM scores (mean +/- SD across iterations and applications) prior to cell-mean aggregation" should be more prominent, and the implications for comparison with the cell-mean-based main tables should be discussed.
- Table S7 recommendation distributions do not include a per-application breakdown. Given that recommendation patterns may vary substantially by application (e.g., DANIEL likely receives more "Do Not Fund" than KELLY), an application-level breakdown would be informative.
- No supplementary table provides the individual LLM review scores that would allow readers to fully reconstruct the analyses. While the data availability statement references a GitHub repository, the review cannot verify that repository contents match the database.
- The prompt templates show that the training examples in Experiments 2-3 include specific reviewer initials (AM, SW, HW, Y) and a pseudonym (DANIEL). If these are real reviewer identifiers, this raises a minor de-identification concern for the publicly available prompts.

---

## 10) Claims That Overreach the Evidence

### 10.1 Abstract: "few-shot prompting produced scores closest to human reviewers"

This statement is factually correct for the observed data but omits the anchoring confound. A reader unfamiliar with the limitations section could interpret this as evidence of successful calibration. Suggested revision: "few-shot prompting produced scores closest to human reviewers, though this may reflect anchoring to the training application's score range rather than generalizable calibration."

**Status:** Partially addressed in the abstract's subsequent sentence but the initial claim is still prominent.

### 10.2 "49-59% lower score dispersion" framed as a finding about LLM consistency

The manuscript correctly notes that this may reflect range restriction rather than consistency, but the framing in the abstract ("LLMs demonstrated 49-59% lower score dispersion") presents the reduction as a finding before the qualification. Suggested revision: reframe to lead with the range restriction interpretation.

### 10.3 "instruction compliance bias" (Section 4)

The term "instruction compliance bias" is attributed to Perez et al. (2022) but this specific concept does not appear in that reference. The mechanistic claim that "LLMs may prioritize explicit instructions over the calibrating influence of training examples" is plausible but speculative, and the manuscript appropriately hedges it with "one speculative explanation." However, the citation should be corrected or the term should be presented as the authors' own framing.

### 10.4 "LLMs matched the human rank ordering of applications only in Experiment 2"

This claim is verified against the database (KELLY > CHRISTINA > DANIEL in both human and Exp 2 LLM rankings). However, with only 3 applications, there are only 6 possible rank orderings, and matching by chance has probability 1/6 = 16.7%. Matching in 1 of 3 experiments (33%) is not distinguishable from chance. The manuscript does not over-interpret this, but the phrase "only in Experiment 2" may imply that this match is meaningful rather than potentially random.

---

## 11) Priority Revisions Before Reconsideration

Listed in order of priority:

1. **Add explicit anchoring-vs-calibration framing in Results (Major).** The alternative explanation that few-shot alignment reflects anchoring to FC3's score range should be mentioned at the point where Experiment 2 results are first reported, not deferred entirely to the Discussion. One sentence in Section 3.1 would suffice.

2. **Address the non-independent kappa issue (Major).** Either replace the current kappa computation with one that accounts for the pair structure (e.g., report agreement per application and average, use Krippendorff's alpha, or use only non-overlapping pairs), or downgrade the kappa values to informal descriptive summaries with an explicit caveat in the Results section (not only in the limitations).

3. **Flag the temperature confound at every vendor comparison (Major).** Add a parenthetical note to Table 2 and Section 3.3 indicating that vendor differences are confounded with temperature settings. Consider re-running xAI Grok at temperature = 1.0 for a sensitivity analysis, or at minimum discuss the expected direction and magnitude of the bias.

4. **Estimate the human non-independence effect (Moderate).** Compute the intraclass correlation among the 4 human reviewers and report the design effect. Alternatively, present a sensitivity analysis using reviewer-level means (n = 4 per experiment) instead of individual scores.

5. **Add distributional visualizations (Moderate).** Include at least one figure showing score distributions by reviewer type, experiment, and application. A panel of box plots or strip plots would allow readers to assess range restriction, outliers, and overlap directly.

6. **Clarify the "81 generated, 63 analyzed" framing (Moderate).** Revise to make clear that the 18 excluded reviews were removed by design (training application exclusion), not due to quality or post-hoc filtering.

7. **Add a CI for ANOVA eta-squared (Minor).** Report a confidence interval for the eta-squared estimate to convey the uncertainty around this effect size.

8. **Correct or reframe the "instruction compliance bias" citation (Minor).** Either find a citation that directly supports this term or present it as the authors' interpretive label.

9. **Standardize reporting precision (Minor).** Adopt a consistent number of decimal places for each statistic type (e.g., 2 for means and SDs, 3 for p-values and kappas, 2 for effect sizes).

10. **Provide individual-level data in supplementary materials (Minor).** Include a table or data file with all 81 LLM review scores (applicant, vendor, experiment, iteration, total score, recommendation) to enable independent verification without requiring database access.

---

*End of review.*
