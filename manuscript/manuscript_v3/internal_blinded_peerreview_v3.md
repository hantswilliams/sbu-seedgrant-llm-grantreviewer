# Blinded Peer Review

**Manuscript:** "Evaluating Large Language Models as Grant Reviewers: A Comparative Study of Prompt Engineering Strategies"

**Article Type:** Brief Report / Exploratory Pilot Study

**Review Date:** 2026-02-26

---

### 0) Material Inventory and Review Scope

**Materials received:**
- Main manuscript (~4,500 words including references)
- Supplementary materials document (S1--S5) containing: full prompt templates for all three experimental conditions (S1.1--S1.3), criterion-level statistical tables for all experiments (S2, Tables S1--S3), per-vendor criterion-level means (S3, Tables S4--S6), recommendation distributions (S4, Table S7), and LLM API configuration details (S5, Table S8)
- Raw data in SQLite database (combined_reviews table with 120 rows: 12 human, 108 LLM across 4 experiments)

**Materials present:**
- Abstract: Present
- Introduction: Present
- Methods (Design, Participants, Materials, Procedures, Analysis): Present
- Results (Tables 1--2, narrative): Present
- Discussion (including Limitations, Implications): Present
- Conflict of Interest / Author Contributions / Funding / Data Availability: Present
- References: 13 citations
- Supplementary Material: Present and comprehensive

**Materials absent or incomplete:**
- No CONSORT, STROBE, or comparable reporting checklist is cited. Given the experimental nature of the study, a structured reporting framework (or at minimum a checklist for AI/ML evaluation studies, such as TRIPOD+AI or DECIDE-AI) would strengthen transparency.
- No preregistration (acknowledged by authors in Limitations).
- No power analysis or sample size justification beyond the pragmatic constraint of available applications.
- The database contains a fourth experimental condition ("with_training_data_v1," 27 LLM reviews) that is not reported in the manuscript. The selective exclusion of this condition is not disclosed or justified.
- No figures are included in the manuscript text. The study would benefit from at least one visualization (e.g., score distributions by condition, or a panel comparing human vs. LLM score dispersion).

---

### 1) Overall Recommendation

**Revise and Resubmit (Major Revisions Required)**

The study addresses a timely and relevant question, employs a reasonable methodological framework for an exploratory pilot, and demonstrates commendable transparency about its limitations. However, the manuscript contains a factual error in the reported training example score range (68--92 vs. actual 61--80), an ambiguous definition of the "15.2-point swing" metric, inconsistent units of analysis for agreement metrics within Table 1, and incomplete disclosure of all experimental conditions run. These issues, combined with several interpretive overclaims that exceed what the small sample can support, require substantive revision before the manuscript is suitable for publication.

---

### 2) Summary Assessment

This exploratory pilot study compares LLM-generated grant review scores to human expert reviews across three prompt engineering strategies using three commercial LLMs and three seed grant applications. The study design is appropriate for a pilot investigation, and the authors demonstrate laudable methodological awareness by addressing pseudoreplication through cell-mean aggregation, using Glass's delta with the human SD as reference, and providing extensive limitations. However, the effective sample sizes (n = 3 applications, 4 human reviewers) are extremely small, and the study cannot distinguish prompt engineering effects from application-specific or reviewer-specific effects. A factual error in the reported training example score range undermines confidence in data handling. The agreement metrics in Table 1 conflate application-level majority-vote agreement with pair-level Cohen's kappa, which is methodologically inconsistent and inadequately explained. Despite these concerns, the manuscript contributes a useful methodological template for future, larger-scale investigations and appropriately frames its findings as hypothesis-generating.

---

### 3) Fatal Flaws

No single issue rises to the level of a fatal, rejection-warranting flaw. The study is explicitly framed as an exploratory pilot, and the primary claims are appropriately hedged. However, the accumulation of the major concerns listed below approaches the threshold at which the manuscript's contribution-to-noise ratio must be carefully weighed.

---

### 4) Major Concerns

**4.1 Incorrect Training Example Score Range**

- **Issue:** Section 2.3 states that the four human reviews of FC3 used as training examples demonstrated "natural score variance (range: 68--92 points)." The actual scores in the database and in the supplementary materials (Table in S1.2) are 61, 66, 77, and 80, yielding a range of 61--80. The stated range of 68--92 does not correspond to any subset of the data.
- **Where it appears:** Section 2.3, paragraph on Experiment 2.
- **Why it matters:** This is a factual error about the study's core intervention. The training examples are the primary manipulation differentiating Experiments 2--3 from Experiment 1. Readers relying on the manuscript text would have an incorrect understanding of the calibration signal provided to the LLMs. The discrepancy between the actual range (61--80, centered below the midpoint of the scale) and the stated range (68--92, centered above the midpoint) could lead to different interpretations of why LLMs calibrated as they did.
- **What would strengthen it:** Correct the range to 61--80 throughout the manuscript. Verify all other numerical claims against the raw data to ensure no similar transcription errors exist.

**4.2 Ambiguous and Misleading "15.2-Point Swing" Metric**

- **Issue:** The Discussion (Section 4, paragraph 1) and abstract refer to a "15.2-point swing in mean LLM scores across experimental conditions." Verification against the data reveals that the actual range of LLM means across experiments is 11.2 points (83.63 minus 72.44) or 11.9 points when computed on a common comparison base (FC1 and FC2 only across all three experiments: 84.39 minus 72.44). The 15.2-point figure is instead the range of mean differences from the human reference group (+4.55 minus [-10.68] = 15.23). These are fundamentally different quantities: the former measures absolute LLM score change, while the latter conflates LLM score change with the changing composition of the human comparison group (12 human reviews including DANIEL in Experiment 1 vs. 8 excluding DANIEL in Experiments 2--3).
- **Where it appears:** Abstract (line 13), Section 4 Discussion (paragraph 1), Section 4 Discussion (paragraph 1 again, in the comparison with vendor spread).
- **Why it matters:** Describing the range of mean differences as a "swing in mean LLM scores" misattributes a composite statistic to LLM behavior alone. The quantity is inflated relative to the actual change in LLM scoring because the human comparison group also shifts between experiments (the human mean rises from 79.08 to 83.13 when DANIEL is excluded). This overstates the magnitude of the prompt engineering effect and could mislead readers about the practical significance of prompt design choices.
- **What would strengthen it:** Either (a) report the actual range of LLM means on a common comparison base (~11.9 points using FC1/FC2 only), or (b) clearly define the 15.2-point figure as the range of mean deviations from the respective human baselines, with an explicit note that this conflates LLM scoring changes with composition changes in the comparison group. Adjust the abstract and all downstream comparisons accordingly.

**4.3 Mixed Units of Analysis in Table 1 Agreement Metrics**

- **Issue:** Table 1 presents "Broad agreement" and "Exact agreement" as percentages alongside Cohen's kappa values. Verification reveals that the percentage agreement is computed at the application level using majority-vote classification (e.g., 1/3 applications = 33.3% for Experiment 1), while Cohen's kappa is computed over all human-LLM review pairs per application (n = 108 pairs for Experiment 1). These represent fundamentally different units of analysis, and the manuscript does not disclose this difference. The Methods section (2.5) states only that "Cohen's kappa... [was] computed over all human-LLM review pairs within each application," with no mention of an application-level majority-vote metric.
- **Where it appears:** Table 1 (rows: "Broad agreement," "Exact agreement," "Cohen's kappa [broad]," "Cohen's kappa [exact]").
- **Why it matters:** Readers will reasonably assume that the agreement percentages and kappa values were computed on the same unit of analysis. The application-level agreement percentages are based on n = 2 or 3 applications, yielding only 3 possible values (0%, 50%, or 100% for Experiments 2--3), which provides negligible statistical information. Presenting these alongside pair-level kappas without disclosure creates an internally inconsistent table.
- **What would strengthen it:** Either (a) compute all agreement metrics at the same unit of analysis (pair-level), or (b) clearly label and footnote the different units of analysis in Table 1 and the Methods section. If retaining the application-level metric, acknowledge that it is based on n = 2--3 observations and is therefore uninformative.

**4.4 Undisclosed Fourth Experimental Condition**

- **Issue:** The database contains 27 LLM reviews from an experiment labeled "with_training_data_v1" that is not reported in the manuscript. This experiment used all three applicants and all three vendors, with an overall mean score of 83.33. The manuscript states that "three prompt engineering strategies were tested" and reports "63 total LLM reviews," both of which are technically accurate for the reported experiments but omit the existence of this additional condition.
- **Where it appears:** Not in the manuscript; discovered through database audit.
- **Why it matters:** Selective reporting of experimental conditions, even in exploratory studies, introduces a risk of reporting bias. Readers and reviewers cannot assess whether the omitted condition was excluded for principled reasons (e.g., it was a pilot run, or it tested a different research question) or because its results were inconvenient. Transparent research requires disclosure of all data collected.
- **What would strengthen it:** Either (a) include the fourth condition in the manuscript with appropriate justification for its role in the study, or (b) acknowledge its existence in the Methods section and provide a clear rationale for its exclusion from the reported analyses (e.g., "A preliminary single-example few-shot condition was also tested but excluded from the primary analyses because [reason]").

---

### 5) Moderate Concerns

**5.1 Missing Criterion Score Affecting Total Score Computation**

- **Issue:** One LLM review (OpenAI GPT-5 Nano, iteration 1, applicant KELLY, Experiment 3) has a missing Team Strength score. The total score for this review is 62.0, which equals the sum of the five non-missing criteria, meaning the total was computed without any Team Strength contribution. The manuscript acknowledges the missing value ("one criterion-level value [Team Strength] was missing from a single review but the total score was still produced") but does not disclose that the total score is therefore understated by approximately 7--9 points (based on the mean of the other GPT-5 Nano Team Strength scores in Experiment 3, which is 8.2).
- **Where it appears:** Section 2.4, and implicitly in all Experiment 3 results.
- **Why it matters:** An understated total score of 62 (vs. an estimated ~70 if Team Strength were imputed) affects the GPT-5 Nano/KELLY cell mean in Experiment 3 (66.33 instead of an estimated ~69.07), which propagates to the overall Experiment 3 LLM mean, the ANOVA, and the mean difference from humans. The manuscript's framing suggests the missing value is inconsequential, but it systematically biases Experiment 3 results toward greater underscoring.
- **What would strengthen it:** Either (a) impute the missing Team Strength score using the within-condition, within-vendor mean and report the imputation, (b) exclude the review entirely, or (c) conduct a sensitivity analysis showing how results change with and without the affected review. Disclose the direction and approximate magnitude of the bias.

**5.2 Confounding of Training Example Source with Scoring Calibration**

- **Issue:** The authors appropriately note in Section 4.1 (Limitations) that using a single application (FC3/DANIEL) as the training example confounds general scoring calibration with application-specific anchoring. However, this limitation is more severe than acknowledged: DANIEL received the lowest human mean score (71.0) of the three applications, with 3 of 4 reviewers recommending "Do Not Fund." The training examples thus disproportionately demonstrated critical scoring and rejection behavior. The improved alignment in Experiment 2 and the substantial under-scoring in Experiment 3 could both reflect LLMs anchoring to the low-scoring training application rather than learning calibrated scoring behavior.
- **Where it appears:** Sections 2.3, 4.1.
- **Why it matters:** The direction of the prompt engineering effects (downward shift from Experiment 1 to 2 and further to 3) is consistent with LLMs anchoring to the critical training examples rather than with generalizable calibration. Without training examples from higher-scoring applications, the study cannot distinguish these explanations. The Discussion's framing of Experiment 2 as achieving "best alignment" may be artifactual if the calibration simply shifted scores toward the training anchor.
- **What would strengthen it:** Expand the discussion of this confound to explicitly state that the training application was the lowest-scoring of the three, note that the direction of all prompt engineering effects is consistent with anchoring to this low-scoring example, and temper claims about "best alignment" accordingly.

**5.3 Non-Independent Pairs in Kappa Computation**

- **Issue:** The Methods section (2.5) states that "Cohen's kappa was computed over all human-LLM review pairs within each application, creating non-independent pairs that may bias kappa point estimates." This acknowledgment is appropriate, but the degree of non-independence is substantial: for Experiment 1, each of the 12 human reviews is paired with each of the 27 LLM reviews that share the same application, yielding 108 pairs from only 39 independent reviews. Each human review appears in 9 pairs, and each LLM review appears in 4 pairs. This degree of pseudoreplication in the kappa computation likely inflates the apparent precision of the kappa estimates even though the point estimates themselves happen to be near zero.
- **Where it appears:** Sections 2.5, 3.4, Table 1.
- **Why it matters:** While the qualitative conclusion (near-zero agreement) is robust to this concern, the specific kappa point estimates (e.g., 0.061, 0.020, -0.037) carry false precision. Reporting three-decimal kappas computed from massively pseudoreplicated data may convey unjustified specificity.
- **What would strengthen it:** Either (a) compute kappa on aggregated data (e.g., modal recommendation per vendor-application cell vs. modal recommendation per application for humans), or (b) report kappa values as approximate ranges rather than point estimates, with an explicit caveat about the degree of pseudoreplication. Consider presenting a confusion matrix in the supplementary materials to allow readers to assess the pair-level data directly.

**5.4 Inconsistent Temperature Settings Across Vendors**

- **Issue:** xAI Grok was run with temperature = 0.1 while OpenAI and Google used their default temperature of 1.0. The manuscript acknowledges this difference in Section 2.4 and again in the Limitations, but it is not adequately addressed as a confound. A 10-fold difference in temperature is a major parameter difference that would be expected to reduce output variability for Grok relative to the other vendors, yet the study draws vendor-level comparisons without controlling for this.
- **Where it appears:** Section 2.4, Table S8, and implicitly in all vendor comparisons (Table 2, Section 3.3).
- **Why it matters:** The vendor comparisons in Table 2 and Section 3.3 are presented descriptively, but readers may still interpret them as reflecting meaningful differences in model capability. The temperature confound makes such interpretations unreliable. Grok's apparent consistency may reflect a deterministic-like parameter setting rather than any property of the model itself.
- **What would strengthen it:** Either (a) rerun Grok at temperature 1.0 (or all models at temperature 0.1) to obtain a controlled comparison, or (b) prominently flag the temperature difference in Table 2 and Section 3.3 (not just in 2.4 and the Limitations) and state explicitly that vendor comparisons are confounded by this parameter difference.

---

### 6) Minor Concerns

**6.1 Rounding of Human Mean in Table 1**

- **Issue:** The human mean for Experiments 2--3 is computed as 83.125 (the arithmetic mean of scores 90, 99, 91, 77, 65, 98, 81, 64). The manuscript reports this as 83.13 in Table 1 and throughout the text. Standard IEEE 754 rounding (round half to even) would round 83.125 to 83.12, while "round half up" would yield 83.13. The choice of rounding convention should be consistent and the difference is trivial, but it is noted for completeness.
- **Where it appears:** Table 1, throughout Section 3.
- **Why it matters:** Negligible impact on results. Noted for editorial completeness.
- **What would strengthen it:** Adopt consistent rounding and verify all reported decimal values.

**6.2 Article Type Classification**

- **Issue:** The manuscript is positioned as a "brief report" or "exploratory pilot study" but at approximately 4,500 words (excluding references and supplementary materials) it approaches the length of a standard original research article. Some journals distinguish these article types by word limit.
- **Where it appears:** Throughout.
- **Why it matters:** The article type should match the target journal's classification. If submitted as a brief report, the length may exceed format requirements.
- **What would strengthen it:** Verify that the manuscript meets the word count requirements of the target journal's article type.

**6.3 Software Version Imprecision**

- **Issue:** Section 2.5 lists "scipy 1.11, scikit-learn 1.6, and pandas 2.1" without patch version numbers. Given that minor releases can change default behaviors (e.g., scipy 1.11.0 vs. 1.11.4), full version numbers would improve reproducibility.
- **Where it appears:** Section 2.5.
- **Why it matters:** Minor impact on reproducibility.
- **What would strengthen it:** Report full version numbers (e.g., scipy 1.11.4, pandas 2.1.3).

**6.4 Pseudonym Inconsistency Between Manuscript and Supplementary**

- **Issue:** The manuscript uses pseudonyms FC1, FC2, FC3 for the three applications. The supplementary materials use pseudonyms DANIEL, KELLY, CHRISTINA, and the prompt template references "PART_A." The mapping between these naming systems (FC3 = DANIEL) can be inferred but is never explicitly stated.
- **Where it appears:** Section 2.2 (FC1, FC2, FC3) vs. Supplementary S1.2 (DANIEL, PART_A).
- **Why it matters:** Readers cross-referencing the manuscript and supplementary materials must infer the mapping. This creates unnecessary ambiguity.
- **What would strengthen it:** Provide an explicit mapping table or consistent pseudonym usage across the manuscript and supplementary materials.

**6.5 Reference 12 Mismatch**

- **Issue:** Reference 12 (Perez et al., 2022) is cited in support of "instruction compliance bias." This paper describes methods for discovering model behaviors through model-written evaluations and does not specifically introduce or validate the concept of "instruction compliance bias" as a named phenomenon. The citation may not adequately support the specific claim.
- **Where it appears:** Section 4, paragraph 2.
- **Why it matters:** The claim about instruction compliance bias is speculative (appropriately hedged as such), but the citation should support the concept invoked.
- **What would strengthen it:** Either find a more directly relevant citation or remove the citation and present the speculation as purely author-generated.

---

### 7) Internal Consistency Audit

The following numerical claims were systematically verified against the raw SQLite database. Items are marked as VERIFIED, DISCREPANCY, or NOTED.

| Claim | Location | Verification Result |
|---|---|---|
| 12 human reviews (4 reviewers x 3 applications) | Abstract, Section 2.2 | **VERIFIED.** Database contains exactly 12 human reviews. |
| 63 LLM reviews | Abstract, Section 2.4 | **VERIFIED** as reviews used in analysis (27 + 18 + 18). However, the phrasing "yielded 63 total LLM reviews" is misleading -- at minimum 81 LLM reviews were generated across the 3 reported experiments (27 per experiment), and 108 exist in the database across 4 experiments. |
| 27 LLM reviews in Exp 1 | Section 2.3, Table 1 | **VERIFIED.** 3 vendors x 3 applications x 3 iterations = 27. |
| 18 LLM reviews in Exp 2 and 3 | Section 2.3, Table 1 | **VERIFIED.** 3 vendors x 2 applications x 3 iterations = 18 (DANIEL excluded). |
| Human mean 79.08 +/- 13.32 (Exp 1) | Table 1 | **VERIFIED.** Computed: 79.08, SD = 13.32. |
| Human mean 83.13 +/- 13.73 (Exp 2--3) | Table 1 | **VERIFIED** (with rounding note). Computed: 83.125, SD = 13.73. Rounded to 83.13 in manuscript. |
| LLM aggregated mean 83.63 +/- 5.24 (Exp 1) | Table 1 | **VERIFIED.** Computed: 83.63, SD = 5.24. |
| LLM aggregated mean 80.56 +/- 4.81 (Exp 2) | Table 1 | **VERIFIED.** Computed: 80.56, SD = 4.81. |
| LLM aggregated mean 72.44 +/- 4.98 (Exp 3) | Table 1 | **VERIFIED.** Computed: 72.44, SD = 4.98. |
| Mean difference +4.55 (Exp 1) | Table 1, Section 3.1 | **VERIFIED.** 83.63 - 79.08 = 4.55. |
| Mean difference -2.57 (Exp 2) | Table 1, Section 3.1 | **VERIFIED.** 80.56 - 83.13 = -2.57. |
| Mean difference -10.68 (Exp 3) | Table 1, Section 3.1 | **VERIFIED.** 72.44 - 83.13 = -10.69 (rounds to -10.68 depending on whether 83.12 or 83.13 is used as the human mean). |
| p = 0.347 (Exp 1) | Table 1 | **VERIFIED.** Computed: 0.347. |
| p = 0.671 (Exp 2) | Table 1 | **VERIFIED.** Computed: 0.671. |
| p = 0.097 (Exp 3) | Table 1 | **VERIFIED** (within rounding). Computed: 0.096--0.097 depending on precision. |
| Glass's delta 0.34, -0.19, -0.78 | Table 1 | **VERIFIED.** Computed: 0.34, -0.19, -0.78. |
| ANOVA F(2,18) = 8.99, p = 0.002, eta-squared = 0.500 | Section 3.1 | **VERIFIED.** df = (2, 18) from 9 + 6 + 6 = 21 observations. F = 8.99, p = 0.002, eta-squared = 0.500. |
| Training example range 68--92 | Section 2.3 | **DISCREPANCY.** Actual range is 61--80 (scores: 61, 66, 77, 80). The supplementary materials correctly show 61--80. |
| 15.2-point swing | Abstract, Section 4 | **DISCREPANCY** (misleading). The 15.2-point figure is the range of mean differences from human (+4.55 to -10.68 = 15.23), not the range of raw LLM mean scores (11.2 points, or 11.9 on a common sample base). |
| Vendor means in Table 2 average to Table 1 LLM means | Tables 1--2 | **VERIFIED.** Exp 1: (88.44 + 77.33 + 85.11)/3 = 83.63. Exp 2: (82.33 + 76.00 + 83.33)/3 = 80.55 (rounds to 80.56). Exp 3: (78.00 + 69.83 + 69.50)/3 = 72.44. |
| LLM FwR: 52--78% | Abstract, Section 3.4 | **VERIFIED.** Exp 1: 51.9%, Exp 2: 77.8%, Exp 3: 72.2%. Range 51.9--77.8% reported as 52--78%. |
| Human FwR: 25% | Abstract, Section 3.4 | **VERIFIED.** Exp 1: 3/12 = 25%. Exp 2--3: 2/8 = 25%. |
| Cohen's kappa (exact): 0.061, 0.020, -0.037 | Table 1 | **VERIFIED.** Computed from all human-LLM pairs per application. |
| Cohen's kappa (broad): 0.000, 0.100, -0.071 | Table 1 | **VERIFIED.** |
| Broad agreement: 33.3%, 50.0%, 50.0% | Table 1 | **VERIFIED** as application-level majority-vote agreement (not pair-level), though this basis is not disclosed in the Methods. |
| Exact agreement: 0.0%, 0.0%, 0.0% | Table 1 | **VERIFIED** as application-level majority-vote agreement. |
| Dispersion reduction 49% (Exp 1) | Abstract, Section 3.4 | **VERIFIED.** Human avg within-applicant SD: 11.37; LLM: 5.78. Reduction: 49%. |
| Dispersion reduction 59% (Exp 2--3) | Abstract, Section 3.4 | **VERIFIED.** Exp 2: Human 12.56, LLM 5.18 = 59%. Exp 3: Human 12.56, LLM 5.19 = 59%. |
| LLM rank range 2.4 points (Exp 1) | Section 3.4 | **VERIFIED.** LLM application means: 84.56, 84.22, 82.11. Range = 2.44. |
| Human rank range 18.2 points (Exp 1) | Section 3.4 | **VERIFIED.** Human application means: 89.25, 77.00, 71.00. Range = 18.25. |
| Rank ordering matched only in Exp 2 | Section 3.4 | **VERIFIED.** Exp 1: Human [KELLY, CHRISTINA, DANIEL], LLM [CHRISTINA, KELLY, DANIEL] -- mismatch. Exp 2: Both [KELLY, CHRISTINA] -- match. Exp 3: Human [KELLY, CHRISTINA], LLM [CHRISTINA, KELLY] -- mismatch. |
| Recommendation distributions (Table S7) | Supplementary S4 | **VERIFIED.** All counts and percentages match the database. |
| Zero DNF in Exp 1 LLM | Section 3.4 | **VERIFIED.** |
| 27.8% DNF in Exp 3 LLM | Section 3.4 | **VERIFIED.** 5/18 = 27.8%. |
| Zero Fund in Exp 3 LLM | Section 3.4 | **VERIFIED.** |
| Criterion-level statistics (Tables S1--S3) | Supplementary S2 | **VERIFIED.** All human means, LLM means, differences, t-statistics, and p-values reproduced to within rounding tolerance. |
| One missing Team Strength value | Section 2.4 | **VERIFIED.** OpenAI GPT-5 Nano iteration 1, KELLY, Experiment 3. Total score = 62 (sum of 5 non-missing criteria; team strength not included). |

---

### 8) Statistical Review (Simple-First)

**8.1 Simple Adequacy**

- The choice of independent-samples t-tests comparing aggregated LLM cell means to individual human scores is defensible for an exploratory pilot, though it does not model the nested structure of the human data (4 reviewers scoring all applications). The authors acknowledge this in the Limitations.
- Glass's delta with the human SD as reference is appropriate given the large variance ratio between groups (~2.5-fold difference). This is correctly justified in Section 2.5.
- Cell-mean aggregation across the 3 LLM iterations per vendor-application combination appropriately addresses pseudoreplication. The resulting sample sizes (n = 9 or 6 for LLM, n = 12 or 8 for human) are reported transparently.
- Holm-Bonferroni correction for multiple criterion-level comparisons is applied and both uncorrected and corrected p-values are reported. This is good practice.

**8.2 Advanced Concerns**

- The one-way ANOVA comparing LLM cell means across the three experiments is potentially problematic: the three groups do not share the same composition (Experiment 1 includes all 3 applications; Experiments 2--3 include only 2). This means the ANOVA compares means derived from different application pools, confounding prompt effects with application composition effects. The F(2,18) = 8.99 with p = 0.002 and eta-squared = 0.500 is numerically verified, but the inferential validity is questionable because the groups are not exchangeable.
- The tension between the bootstrap confidence interval for Experiment 3 ([-20.11, -1.03], excluding zero) and the t-test p-value (0.097, not rejecting at alpha = 0.05) is acknowledged in the manuscript. This tension likely arises from the difference between bootstrap and parametric assumptions with small, non-normal samples. The manuscript handles this appropriately by noting the discrepancy.
- The paired structure of the human data (4 reviewers each scoring all applications) is not modeled. A mixed-effects approach would be more appropriate for a confirmatory study but is reasonable to omit in this exploratory context. The authors correctly identify this as a limitation and recommend mixed-effects models for future work.
- No corrections for multiple comparisons are applied across the three experiments at the overall score level (only within criterion-level analyses). Given the exploratory framing, this is acceptable but should be noted.
- The effective sample size for the ANOVA is 21 (9 + 6 + 6), yielding 18 residual degrees of freedom. This is verified and correctly reported.

**8.3 Effect Size Interpretation**

- Glass's delta values of 0.34, -0.19, and -0.78 are reported with bootstrap confidence intervals. The CIs are wide (e.g., [-2.61, -0.08] for Experiment 3), reflecting the high uncertainty inherent in the small sample. The authors appropriately refrain from strong claims about effect magnitude.
- The eta-squared of 0.500 for the ANOVA suggests a very large effect, but this should be interpreted cautiously given the small sample and the composition confound noted above.

---

### 9) Supplementary Materials Assessment

**Strengths:**
- The full prompt templates (S1.1--S1.3) provide complete transparency about the experimental manipulation. This is essential for reproducibility and is a significant strength of the manuscript.
- Per-vendor criterion-level means (S3) and recommendation distributions (S4) provide useful granular data.
- API configuration details (S5) enhance reproducibility.

**Concerns:**
- Supplementary Table S6 reports Team Strength for GPT-5 Nano (Experiment 3) as 8.20 +/- 0.84 based on n = 5 non-missing values, but the table header implies n = 6 per vendor. This should be footnoted.
- The supplementary annotation for S1.2 states "score range: 61--80," which is correct but contradicts the manuscript text stating "68--92." This discrepancy between manuscript and supplementary materials should have been caught during internal review.
- The criterion names in the prompt templates (e.g., "Strength of Research Team [Who]") differ slightly from those in the statistical tables (e.g., "Team Strength"). While trivial, consistent naming aids cross-referencing.
- The supplementary materials do not include raw score distributions, individual review scores for LLM reviews, or confusion matrices for the recommendation agreement analysis. Including at least a confusion matrix for each experiment would allow readers to evaluate the kappa computations directly.

---

### 10) Claims That Overreach the Evidence

**10.1** The abstract states that "few-shot prompting produced scores closest to human reviewers" with a -2.57 point difference. While numerically accurate, characterizing this as the prompt strategy "producing" the closest alignment implies a causal relationship that cannot be established with 3 applications. The result is equally consistent with application-specific anchoring to the low-scoring training example (which would shift LLM scores downward from the optimistic baseline toward the human mean by coincidence rather than by calibration).

**10.2** The Discussion states that "prompt condition differences exceeded vendor differences in the best-aligned experiment (Experiment 2: 7.3-point vendor spread vs. 15.2-point prompt swing)." As noted in Major Concern 4.2, the 15.2-point figure is inflated. Even if correctly computed, comparing a within-experiment vendor spread to a cross-experiment prompt effect is not a meaningful comparison because the vendor spread is measured within a fixed prompt condition while the prompt effect spans different conditions and comparison groups.

**10.3** The Discussion's claim about "instruction compliance bias" (Section 4, paragraph 2) is appropriately hedged as "speculative" but may still convey more theoretical specificity than warranted. Labeling the observed pattern with a named cognitive/computational bias implies a mechanism that cannot be inferred from three applications.

**10.4** The abstract's statement that "LLMs demonstrated 49--59% lower score dispersion than humans" is framed as a finding about LLM behavior, but the manuscript's own Results section (3.4) correctly notes this may reflect "range restriction rather than superior consistency." The abstract should mirror this qualification rather than presenting the dispersion reduction as a straightforward finding.

**10.5** The claim that "LLMs cannot yet reliably replicate human grant review judgments" (abstract, final sentence) is directionally supported by the near-zero kappa values and recommendation misalignment but cannot be generalized from a study of 3 applications, 4 reviewers, and 3 LLMs at a single institution. The qualifying phrase "These case-study findings from three applications at a single institution suggest" appropriately hedges the scope but is followed by a conclusion that drops this hedging.

---

### 11) Priority Revisions Before Reconsideration

Listed in order of priority:

1. **Correct the training example score range** from 68--92 to 61--80 throughout the manuscript (Section 2.3). Verify all other numerical claims against the raw data.

2. **Clarify or correct the "15.2-point swing" metric.** Either recompute using a consistent comparison base (the range of LLM means computed on FC1/FC2 only across all experiments, which yields ~11.9 points) or explicitly define the metric as the range of mean deviations from the respective human baselines with a note about composition confounding. Update the abstract and Discussion accordingly.

3. **Disclose the fourth experimental condition** ("with_training_data_v1") present in the database. Provide a brief rationale for its exclusion from the reported analyses.

4. **Reconcile the agreement metrics in Table 1.** Either use a consistent unit of analysis for all metrics or clearly label and footnote the different computation methods (application-level for percentage agreement, pair-level for kappa). Update the Methods section to describe both computation methods.

5. **Address the missing Team Strength score** more transparently. Disclose that the affected total score (62) does not include a Team Strength contribution, quantify the likely impact on Experiment 3 results, and either impute the missing value or conduct a sensitivity analysis.

6. **Strengthen the Discussion of training example anchoring confound.** Explicitly note that the training application received the lowest human scores and that all prompt engineering effects are directionally consistent with anchoring to this low-scoring example.

7. **Qualify the abstract's dispersion reduction claim** by adding the range restriction caveat present in the Results section.

8. **Report the ANOVA with an explicit caveat** that the three groups include different application compositions (3 vs. 2 vs. 2 applications), which partially confounds the prompt engineering effect with application selection.

9. **Provide explicit pseudonym mapping** between the manuscript (FC1, FC2, FC3) and supplementary materials (KELLY, CHRISTINA, DANIEL).

10. **Add confusion matrices** to the supplementary materials to allow independent evaluation of the recommendation agreement data.

---

*End of Review*
