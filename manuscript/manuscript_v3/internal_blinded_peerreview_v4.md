# Blinded Peer Review: Internal Consistency and Methods Audit

**Manuscript:** "Evaluating Large Language Models as Grant Reviewers: A Comparative Study of Prompt Engineering Strategies"

**Review Type:** FULL_METHODS + CONSISTENCY_AUDIT

**Date:** 2026-02-27

---

## 0) Material Inventory and Review Scope

### Provided Materials
| Material | Status | Notes |
|---|---|---|
| Main manuscript (brief report format) | Present | ~4,500 words including references |
| Abstract | Present | Structured, includes key quantitative claims |
| Methods section | Present | Covers design, data, experiments, LLM config, statistics |
| Results section | Present | Tables 1-2, descriptive and inferential statistics |
| Discussion with limitations | Present | Thorough limitations subsection |
| Supplementary Material S1 (Prompt templates) | Present | All three experimental prompts provided |
| Supplementary Tables S1-S3 (Criterion-level) | Present | Per-experiment criterion comparisons |
| Supplementary Tables S4-S6 (Per-vendor criterion) | Present | Raw LLM means by vendor and experiment |
| Supplementary Table S7 (Recommendations) | Present | Frequency distributions |
| Supplementary Table S8 (API config) | Present | Model IDs, temperatures, tokens |
| Raw SQLite database | Present | Verified against all manuscript claims |

### Missing or Incomplete
| Material | Status | Impact |
|---|---|---|
| Preregistration or analysis plan | Absent | Acknowledged in limitations |
| Effect size justification / power analysis | Absent | Understandable given exploratory framing |
| Fourth experimental condition (with_training_data_v1) | **Unreported** | See Major Concern #1 |
| Mixed-effects modeling or ICC for human reviewer nesting | Absent | Acknowledged in limitations |
| Raw prompt text for Experiment 4 (with_training_data_v1.md) | Present in repository but not in supplementary | Selective omission |
| Confidence intervals for kappa estimates | Absent | Minor given near-zero values |

### Study Characteristics
- **Study type:** Multi-condition, multi-vendor comparative evaluation (exploratory pilot)
- **Article type:** Brief report
- **Primary claims:** (1) Few-shot prompting produces closest LLM-to-human score alignment; (2) Strict instructions cause counter-productive under-scoring; (3) LLMs show reduced variability but cannot reliably replicate human rank ordering; (4) Recommendation agreement is at chance level across all conditions.

---

## 1) Overall Recommendation

**Major Revision**

The manuscript is methodologically thoughtful for a pilot study, demonstrates appropriate statistical caution, and the numerical claims are internally consistent with the raw database. However, the omission of a fourth experimental condition present in the raw data (with_training_data_v1, a single-example few-shot condition) constitutes a selective reporting concern that must be addressed before publication. The ANOVA comparing experiments with non-overlapping application sets is technically problematic. Several additional concerns regarding the nested human reviewer structure, the confound between calibration and anchoring, and the framing of the "best-aligned" experiment require revision. None of these issues are fatal, but collectively they require substantive methodological clarification.

---

## 2) Summary Assessment

This exploratory pilot study compares three prompt engineering strategies (zero-shot, few-shot, few-shot with strict instructions) across three commercial LLMs applied to seed grant review, finding that few-shot prompting produces the smallest deviation from human scores while strict instructions cause counter-productive under-scoring. The study design is appropriate for its exploratory aims, and the authors demonstrate commendable statistical discipline in addressing pseudoreplication, using Glass's delta with human SD as the reference, and repeatedly flagging the pilot-scale limitations. The raw database confirms nearly all numerical claims in the manuscript and supplementary materials. However, the database reveals a fourth experimental condition (with_training_data_v1, a single-example few-shot prompt) that was conducted but not reported, raising a selective reporting concern. The cross-experiment ANOVA compares groups derived from non-overlapping application sets (3 applications in Experiment 1 vs. 2 in Experiments 2-3), conflating prompt effects with application composition effects. These issues are addressable but require transparent disclosure and analytical revision.

---

## 3) Fatal Flaws

None identified. The study is appropriately framed as exploratory, the core numerical claims are verified against the raw data, and the authors' interpretive restraint is generally appropriate for the sample size. The concerns below are substantive but correctable.

---

## 4) Major Concerns

### Major Concern 1: Unreported Fourth Experimental Condition (Selective Reporting)

**Severity: Major**

The raw database contains four LLM experimental conditions, not three:
1. `baseline_v1` (version 1.0) -- reported as Experiment 1 (Zero-Shot)
2. `with_training_data_v1` (version 2.0) -- **not reported**
3. `multi_examples_v1` (version 3.0) -- reported as Experiment 2 (Few-Shot)
4. `strict_scoring_v1` (version 4.0) -- reported as Experiment 3 (Few-Shot + Strict)

The unreported condition (`with_training_data_v1`) is a single-example few-shot prompt that provides one human reviewer's scores (HW: 77/100, "Do Not Fund") as a calibration example. It was run chronologically between the baseline and multi-example conditions (prompt version 2.0). The raw data show 27 LLM reviews generated under this condition across all three applications and all three vendors.

On the common application base (FC1 + FC2), this unreported condition produced a mean deviation of +1.82 points from the human mean -- closer to alignment than the reported zero-shot condition (+4.55 on 3 applications, or approximately +1.27 on FC1+FC2 only) and the reported multi-example condition (-2.57). Its inclusion would alter the narrative that the multi-example condition (Experiment 2) represents the "best alignment."

The omission of a conducted experiment from a manuscript, particularly one whose results are relevant to the central research question, constitutes a selective reporting concern under standard reporting guidelines (e.g., CONSORT extensions, ARRIVE). Even if the authors had methodological reasons for exclusion (e.g., the single-example design was considered a preliminary pilot), this must be transparently disclosed, ideally with its results reported in supplementary materials and the rationale for exclusion stated in the methods.

**Action required:** Report all conducted experimental conditions. If with_training_data_v1 is excluded from the primary analysis, provide a clear rationale and include its descriptive results in a supplementary table.

### Major Concern 2: ANOVA Compares Non-Overlapping Application Sets

**Severity: Major**

The one-way ANOVA comparing LLM cell means across experiments (F(2,18) = 8.99, p = 0.002, eta-squared = 0.500) treats the three experiments as levels of a single factor. However, Experiment 1 includes cell means from all three applications (CHRISTINA, DANIEL, KELLY; n = 9), while Experiments 2 and 3 include only CHRISTINA and KELLY (n = 6 each). The ANOVA therefore conflates two sources of variation: (a) the prompt engineering effect and (b) the inclusion/exclusion of DANIEL, whose human mean (71.0) is substantially below the FC1+FC2 human mean (83.1).

When the ANOVA is restricted to the common application base (FC1 + FC2 only, n = 6 per experiment), the result remains significant (F = 8.18, p = 0.004) but with a different effect size. The authors should report this balanced analysis as the primary ANOVA, or at minimum as a sensitivity analysis, to demonstrate that the prompt engineering effect holds after removing the composition confound.

**Action required:** Either restrict the ANOVA to the common application base (FC1 + FC2) or report both the current and balanced analyses, discussing the potential confound.

---

## 5) Moderate Concerns

### Moderate Concern 1: Confound Between Calibration and Anchoring in Few-Shot Conditions

The manuscript acknowledges in Section 4.1 that the improved alignment in Experiment 2 "could reflect the LLM calibrating to FC3's particular score range rather than learning generalizable scoring behavior." This is a central interpretive limitation that deserves more prominence, as it directly affects the primary claim. The training examples are drawn from a single application (DANIEL/FC3) with scores ranging from 61-80. Any LLM calibration effect is inseparable from an anchoring effect specific to FC3's quality level. The manuscript appropriately notes this but frames Experiment 2 as demonstrating the "best alignment" in the abstract and results without sufficient caveat in those sections.

**Action required:** Add an explicit caveat about the calibration-vs-anchoring confound wherever Experiment 2 is described as "best-aligned," including in the abstract.

### Moderate Concern 2: Non-Independence in Cohen's Kappa Computation

The manuscript computes pair-level agreement by crossing all human reviews with all LLM reviews within each application, producing 108 pairs for Experiment 1 (4 human x 27 LLM) and 72 pairs for Experiments 2-3 (4 human x 18 LLM). These pairs are not independent: each human review is paired with multiple LLM reviews (and vice versa), violating the independence assumption underlying Cohen's kappa.

The authors acknowledge this limitation in Section 4.1, stating that "non-independent pairs may bias kappa point estimates" but arguing that "given that all kappa values were near zero, this is unlikely to change the qualitative conclusion." This defense is reasonable for the qualitative conclusion but the specific kappa values (0.061, 0.020, -0.037 for exact; 0.000, 0.100, -0.071 for broad) should not be reported to three decimal places without noting that the point estimates are biased by non-independence. The appropriate metric would be agreement computed at the cell-mean level (aggregating LLM recommendations within each vendor-application cell, e.g., by majority vote) to match the aggregation approach used for scores.

**Action required:** Either compute kappa on aggregated (majority-vote) recommendations to parallel the cell-mean approach used for scores, or add a more explicit caveat in the results section (not just the limitations) about the non-independence of the pairs.

### Moderate Concern 3: Human Reviewer Nesting Not Modeled

The four human reviewers each scored all three applications, introducing within-reviewer correlation. The manuscript's t-tests treat the 12 (or 8) human scores as independent observations. With only four reviewers, the effective degrees of freedom may be substantially lower than the nominal values. This concern is acknowledged in the limitations but not in the methods or results.

The impact is difficult to quantify without the reviewer-level data structure being modeled (e.g., via ICC or mixed-effects models), but with only four reviewers and high inter-reviewer variability (CHRISTINA SDs of 16.0, spanning 64-98), the human group mean and SD are heavily influenced by individual reviewer calibration. This does not invalidate the t-tests but should temper confidence in the reported p-values and confidence intervals.

**Action required:** Report the ICC or range of individual reviewer means in the results or supplementary materials to characterize the degree of human reviewer clustering.

### Moderate Concern 4: Asymmetric Temperature Settings Across Vendors

The manuscript acknowledges that xAI Grok used temperature = 0.1 while OpenAI and Google used default temperature = 1.0. This is a 10-fold difference in a parameter that directly controls output randomness. In Experiment 1, xAI Grok produced within-vendor total score SDs of 2.37 (compared to 4.59 for Google and 2.74 for OpenAI), so the effect of the temperature asymmetry is not uniformly apparent. However, in Experiment 2, xAI Grok had the lowest within-vendor SD (1.21 vs. 6.83 for Google and 3.41 for OpenAI), consistent with a temperature-driven reduction in variability.

This asymmetry means that vendor comparisons are confounded with temperature settings. The manuscript notes this limitation but does not discuss its implications for the aggregated (cross-vendor) results. If xAI Grok's low temperature artificially reduces its within-cell variance, the cell-mean aggregation is less affected (since cell means average over iterations), but the within-vendor comparisons in Table 2 and Tables S4-S6 are not interpretable as pure vendor effects.

**Action required:** Either justify the temperature asymmetry (e.g., 0.1 was the vendor-recommended default) or explicitly state that vendor-level comparisons are confounded with temperature settings and should not be interpreted as reflecting inherent model differences.

---

## 6) Minor Concerns

### Minor Concern 1: Abstract Claims "63 LLM reviews"

The abstract states "generating 63 LLM reviews compared against 12 human expert reviews." This count (27 + 18 + 18 = 63) represents the reviews used in comparisons, not the total generated. The database contains 108 LLM reviews across the three reported experiments (27 per experiment, including DANIEL reviews in Experiments 2-3 that were excluded from comparisons) plus 27 reviews from the unreported fourth condition (total: 135 generated LLM reviews). The "63" figure is not wrong but may be misleading. Consider clarifying as "63 LLM reviews entered the analysis" or similar.

### Minor Concern 2: "12 human expert reviews" Framing

The abstract and introduction frame the comparison as "63 LLM reviews compared against 12 human expert reviews," but Experiments 2 and 3 use only 8 human reviews (FC1 + FC2). The human comparison set varies across experiments. A more precise abstract formulation would note that the human reference group comprised 12 reviews in Experiment 1 and 8 in Experiments 2-3.

### Minor Concern 3: Rounding Precision in Table 1

The human mean for FC1+FC2 is reported as 83.13 (Table 1, Experiments 2-3). The database yields 83.125, which rounds to 83.13 to two decimal places. This is correct. However, the FC1+FC2 SD is reported as 13.73; the computed value is 13.7276, which rounds to 13.73. All other values verified to within rounding precision. No discrepancies found.

### Minor Concern 4: Missing Criterion-Level Value

The manuscript states: "one criterion-level value (Team Strength) was missing from a single review but the total score was still produced." The database confirms this: Table S6 shows n = 5 for OpenAI Team Strength in Experiment 3 (vs. n = 6 for all other cells). The total score was apparently computed by the LLM without the Team Strength sub-score, or the sub-score was present in the LLM output but not parsed. The manuscript should clarify how the total score was handled (was it the LLM's self-reported total, or was it recomputed from criterion scores?). If the LLM's total is used directly, it may be inconsistent with the sum of criterion scores.

### Minor Concern 5: Reference to "Experiment 2" in Rank-Order Claim

The manuscript states: "LLMs matched the human rank ordering of applications only in Experiment 2." This is verified for FC1 + FC2 (KELLY > CHRISTINA in both human and LLM groups). However, this claim is trivial given that only two applications are compared in Experiments 2-3 (the rank order of two items can only be correct or reversed). In Experiment 1, with three applications, the rank-order comparison is more informative (and LLMs failed to match it). This should be noted.

### Minor Concern 6: Software Version Discrepancy

The methods state analyses used "scipy 1.11, scikit-learn 1.6, and pandas 2.1." Given the October 2025 data collection timeframe, these may not be the exact versions used. This is a minor point but exact software versions should be verified.

---

## 7) Internal Consistency Audit

### Database Verification Summary

All numerical claims in the manuscript and supplementary materials were verified against the raw SQLite database (`data/results.db`, table: `combined_reviews`). The verification procedure is summarized below.

| Claim | Manuscript Value | Database Value | Status |
|---|---|---|---|
| Total human reviews | 12 | 12 | VERIFIED |
| Human mean (all 12) | 79.08 +/- 13.32 | 79.08 +/- 13.32 | VERIFIED |
| Human mean (FC1+FC2, n=8) | 83.13 +/- 13.73 | 83.13 +/- 13.73 | VERIFIED |
| Exp 1 LLM cell mean (n=9) | 83.63 +/- 5.24 | 83.63 +/- 5.24 | VERIFIED |
| Exp 1 mean difference | +4.55 | +4.55 | VERIFIED |
| Exp 2 LLM cell mean (n=6) | 80.56 +/- 4.81 | 80.56 +/- 4.81 | VERIFIED |
| Exp 2 mean difference | -2.57 | -2.57 | VERIFIED |
| Exp 3 LLM cell mean (n=6) | 72.44 +/- 4.98 | 72.44 +/- 4.98 | VERIFIED |
| Exp 3 mean difference | -10.68 | -10.68 | VERIFIED |
| Glass's delta Exp 1 | 0.34 | 0.34 | VERIFIED |
| Glass's delta Exp 2 | -0.19 | -0.19 | VERIFIED |
| Glass's delta Exp 3 | -0.78 | -0.78 | VERIFIED |
| ANOVA F(2,18) | 8.99, p=0.002 | 8.99, p=0.0020 | VERIFIED |
| ANOVA eta-squared | 0.500 | 0.500 | VERIFIED |
| Table 2: Gemini Exp 1 | 88.44 (+9.36) | 88.44 (+9.36) | VERIFIED |
| Table 2: GPT-5 Exp 1 | 77.33 (-1.75) | 77.33 (-1.75) | VERIFIED |
| Table 2: Grok 4 Exp 1 | 85.11 (+6.03) | 85.11 (+6.03) | VERIFIED |
| Table 2: Gemini Exp 2 | 82.33 (-0.79) | 82.33 (-0.79) | VERIFIED |
| Table 2: GPT-5 Exp 2 | 76.00 (-7.12) | 76.00 (-7.13) | VERIFIED (rounding) |
| Table 2: Grok 4 Exp 2 | 83.33 (+0.21) | 83.33 (+0.21) | VERIFIED |
| Table 2: Gemini Exp 3 | 78.00 (-5.12) | 78.00 (-5.13) | VERIFIED (rounding) |
| Table 2: GPT-5 Exp 3 | 69.83 (-13.29) | 69.83 (-13.30) | VERIFIED (rounding) |
| Table 2: Grok 4 Exp 3 | 69.50 (-13.62) | 69.50 (-13.63) | VERIFIED (rounding) |
| FC3/DANIEL training range | 61-80 | 61-80 (scores: 61, 66, 77, 80) | VERIFIED |
| 11.9-point spread (FC1+FC2) | 84.4 to 72.4 | 84.39 to 72.44 = 11.94 | VERIFIED |
| Exp 1 LLM app range | 82.1-84.6 (2.4 pts) | DANIEL=82.1, KELLY=84.2, CHRISTINA=84.6 | VERIFIED |
| Human app range | 71.0-89.2 (18.2 pts) | DANIEL=71.0, CHRISTINA=77.0, KELLY=89.25 | VERIFIED |
| Pair-level exact agreement Exp 1 | 33.3% | 36/108 = 33.3% | VERIFIED |
| Pair-level broad agreement Exp 1 | 58.3% | 63/108 = 58.3% | VERIFIED |
| Pair-level exact agreement Exp 2 | 30.6% | 22/72 = 30.6% | VERIFIED |
| Pair-level broad agreement Exp 2 | 75.0% | 54/72 = 75.0% | VERIFIED |
| Pair-level exact agreement Exp 3 | 22.2% | 16/72 = 22.2% | VERIFIED |
| Pair-level broad agreement Exp 3 | 58.3% | 42/72 = 58.3% | VERIFIED |
| Table S7 Exp 1 Human: Fund | 4 (33.3%) | 4 (33.3%) | VERIFIED |
| Table S7 Exp 1 Human: FwR | 3 (25.0%) | 3 (25.0%) | VERIFIED |
| Table S7 Exp 1 Human: DNF | 5 (41.7%) | 5 (41.7%) | VERIFIED |
| Table S7 Exp 1 LLM: Fund | 13 (48.1%) | 13 (48.1%) | VERIFIED |
| Table S7 Exp 1 LLM: FwR | 14 (51.9%) | 14 (51.9%) | VERIFIED |
| Table S7 Exp 1 LLM: DNF | 0 (0.0%) | 0 (0.0%) | VERIFIED |
| Table S7 Exp 2 Human: Fund | 4 (50.0%) | 4 (50.0%) | VERIFIED |
| Table S7 Exp 2 Human: FwR | 2 (25.0%) | 2 (25.0%) | VERIFIED |
| Table S7 Exp 2 Human: DNF | 2 (25.0%) | 2 (25.0%) | VERIFIED |
| Table S7 Exp 2 LLM: Fund | 3 (16.7%) | 3 (16.7%) | VERIFIED |
| Table S7 Exp 2 LLM: FwR | 14 (77.8%) | 14 (77.8%) | VERIFIED |
| Table S7 Exp 2 LLM: DNF | 1 (5.6%) | 1 (5.6%) | VERIFIED |
| Table S7 Exp 3 LLM: Fund | 0 (0.0%) | 0 (0.0%) | VERIFIED |
| Table S7 Exp 3 LLM: FwR | 13 (72.2%) | 13 (72.2%) | VERIFIED |
| Table S7 Exp 3 LLM: DNF | 5 (27.8%) | 5 (27.8%) | VERIFIED |
| Within-app SD reduction Exp 1 | 49% | Human avg=11.37, LLM avg=5.78, reduction=49% | VERIFIED |
| Within-app SD reduction Exp 2-3 | 59% | Human avg=12.56, LLM avg=5.18/5.19, reduction=59% | VERIFIED |
| All Table S1 values | As reported | As computed | VERIFIED |
| All Table S2 values | As reported | As computed | VERIFIED |
| All Table S3 values | As reported | As computed | VERIFIED |
| All Table S4 values | As reported | As computed | VERIFIED |
| All Table S5 values | As reported | As computed | VERIFIED |
| All Table S6 values | As reported | As computed (n=5 for OpenAI Team in Exp 3) | VERIFIED |

### Discrepancies Found

| Issue | Details | Severity |
|---|---|---|
| Unreported experiment | Database contains `with_training_data_v1` (27 LLM reviews, prompt version 2.0) not mentioned in manuscript | Major |
| Table 2 deviation rounding | GPT-5 Exp 2 deviation: manuscript says -7.12, computed = -7.13; Gemini Exp 3: -5.12 vs -5.13; GPT-5 Exp 3: -13.29 vs -13.30; Grok 4 Exp 3: -13.62 vs -13.63 | Negligible (last-digit rounding) |
| Total LLM reviews generated | Manuscript implies 63 total; database shows 135 generated (108 across 3 reported experiments + 27 unreported) | See Major Concern 1 |

### Cross-Reference Checks

- Training example scores in the supplementary prompt (S1.2) match the DANIEL human review data: AM=66, SW=80, HW=77, Y=61. **Verified.**
- The prompt version in `with_training_data_v1.md` shows HW's single review (77, "Do Not Fund") as the sole training example. This is a distinct experimental manipulation from multi_examples_v1 (which includes all four reviewers). **Confirmed as a separate, unreported condition.**
- Criterion-level scores for DANIEL in the prompt match criterion-level values in the database: AM (27,14,8,6,6,5=66), SW (25,24,9,7,9,6=80), HW (25,20,10,7,8,7=77), Y (20,17,6,5,6,7=61). **Verified.**

---

## 8) Statistical Review (Simple-First)

### Simple Adequacy

| Aspect | Assessment |
|---|---|
| Descriptive statistics present | Yes: means, SDs, ranges, percentages |
| Appropriate central tendency | Yes: means for continuous scores |
| Variance reported | Yes: SDs for both groups, within-applicant SDs |
| Sample sizes stated | Yes: throughout Tables 1, S1-S7 |
| Effect sizes reported | Yes: Glass's delta with CIs |
| Confidence intervals | Yes: for mean differences and Glass's delta (bootstrap) |
| Multiple comparison correction | Yes: Holm-Bonferroni for criterion-level tests |

### Advanced Considerations

**Pseudoreplication handling:** The authors correctly identify that three LLM iterations per vendor-application combination constitute pseudoreplication and address this by averaging to cell means. This is an appropriate and conservative approach. The effective sample sizes (9 for Experiment 1, 6 for Experiments 2-3) are clearly stated.

**Choice of Glass's delta:** Appropriate given the approximately 2.5-fold variance difference between groups (human SD ~13 vs. LLM SD ~5). Using the human SD as the denominator is the correct choice when the human group represents the reference standard.

**Bootstrap CIs:** The use of bias-corrected bootstrap (10,000 resamples) is appropriate for these small, potentially non-normal samples. The bootstrap CIs for Experiment 3 ([-20.11, -1.03]) excluding zero while the t-test does not reach significance (p = 0.097) is adequately discussed.

**ANOVA concerns:** Beyond the application-composition confound noted in Major Concern 2, the one-way ANOVA assumes independence of cell means across experiments. Since the same three LLM models were used in all experiments, the cell means are correlated across experiments (same vendor-application pairs under different prompts). A repeated-measures ANOVA or mixed-effects model would be more appropriate but would require the FC1+FC2-only balanced design.

**Cohen's kappa limitations:** As noted in Moderate Concern 2, the non-independence of pairs biases the kappa estimates. Additionally, with highly unequal marginal distributions (LLMs overwhelmingly choosing "Fund with Revisions"), kappa is known to be paradoxically low even when agreement is moderate (the kappa paradox). The authors should consider whether prevalence-adjusted bias-adjusted kappa (PABAK) or Gwet's AC1 would be more informative.

**Power considerations:** With 9 or 6 LLM cell means and 12 or 8 human scores, the study has very limited power to detect moderate effects. The non-significant p-values (especially Experiment 1: p = 0.347 and Experiment 2: p = 0.671) should not be interpreted as evidence of equivalence. The authors appropriately refrain from equivalence claims but could explicitly note that the study cannot distinguish "no difference" from "underpowered to detect a real difference."

---

## 9) Supplementary Materials Assessment

### Prompt Templates (S1)

The three prompt templates are clearly differentiated and the annotation of differences between conditions is helpful. The progressive addition of training examples (S1.2) and strict instructions (S1.3) is well-documented. The omitted sections are clearly noted with references to S1.1.

**Concern:** The template for with_training_data_v1 (the unreported fourth condition) exists in the repository (`llm/prompts/with_training_data_v1.md`) but is not included in the supplementary materials.

### Criterion-Level Tables (S1-S3)

All values verified against the database (see Section 7). The tables are appropriately formatted with both uncorrected and Holm-corrected p-values. The note about the Innovation & Impact effect in Experiment 3 (largest Glass's delta of -1.185, uncorrected p = 0.031, corrected p = 0.186) is transparently reported.

### Per-Vendor Tables (S4-S6)

All values verified. The use of raw LLM scores (not cell means) is clearly stated. The note about OpenAI Team Strength n = 5 in Table S6 is consistent with the manuscript's mention of one missing criterion value.

### Recommendation Distribution Table (S7)

All counts and percentages verified. The shared human comparison group for Experiments 2-3 is appropriately noted.

### API Configuration Table (S8)

Informative and appropriately detailed. The temperature asymmetry (0.1 for xAI vs. 1.0 for OpenAI and Google) is clearly stated.

### Missing from Supplementary Materials

- Results from the unreported with_training_data_v1 condition
- The with_training_data_v1 prompt template
- Scatter plots or individual data points that would allow visual inspection of the data distributions
- The actual kappa computation code or contingency tables underlying the kappa values

---

## 10) Claims That Overreach the Evidence

### Claim 1: "Few-shot prompting produced scores closest to human reviewers"

**Location:** Abstract, Section 3.1, Discussion

**Assessment:** This claim is numerically accurate for the three reported experiments but omits the unreported with_training_data_v1 condition, which produced a deviation of +1.82 points on the common application base (FC1+FC2) -- potentially closer to human scores than either the zero-shot (+1.27 on FC1+FC2) or the reported few-shot condition (-2.57). Whether with_training_data_v1 truly outperforms multi_examples_v1 depends on the metric (absolute deviation vs. signed deviation), but its omission makes the claim of "best alignment" for Experiment 2 incomplete.

### Claim 2: "Prompt engineering substantially affects LLM scoring behavior"

**Location:** Abstract, Discussion

**Assessment:** Supported by the ANOVA (F = 8.99, p = 0.002) and the 11.9-point spread. However, the word "substantially" in the abstract is a judgment that is not warranted from three applications. The 11.9-point spread is a descriptive observation from a pilot study. The claim would be strengthened by noting that this is based on the specific applications studied.

### Claim 3: "LLMs cannot yet reliably replicate human grant review judgments"

**Location:** Abstract (final sentence)

**Assessment:** This conclusion is appropriately hedged ("preliminary findings suggest") and is supported by the near-zero kappa values, failed rank ordering in two of three experiments, and the persistent "Fund with Revisions" bias. However, this is a generalization from three applications reviewed by four humans and three LLMs at a single institution using one rubric. The "yet" implies a temporal limitation of LLM capability rather than a limitation of the study design.

### Claim 4: "49-59% lower score dispersion"

**Location:** Abstract, Section 3.4

**Assessment:** These percentages are verified but the manuscript appropriately notes that this may reflect "range restriction rather than superior consistency." The abstract could more clearly flag this caveat, as the "49-59% lower score dispersion" figure will likely be cited without the qualifier.

---

## 11) Priority Revisions Before Reconsideration

### Priority 1 (Required): Report the Fourth Experimental Condition

Disclose the existence and results of the with_training_data_v1 condition. Options include: (a) incorporating it as a fourth experiment in the main analysis (preferred), (b) reporting its results in supplementary materials with a rationale for exclusion from the primary analysis, or (c) at minimum, acknowledging its existence and providing the rationale for its omission. Include the prompt template in the supplementary materials.

### Priority 2 (Required): Address the ANOVA Application-Set Confound

Either restrict the cross-experiment ANOVA to the common application base (FC1 + FC2, producing a balanced 6 vs. 6 vs. 6 comparison) or report both the current and balanced analyses. Discuss the potential confound between prompt condition and application composition in the results section.

### Priority 3 (Strongly Recommended): Caveat the "Best Alignment" Claim

Wherever Experiment 2 is described as producing the "best" or "closest" alignment (abstract, results, discussion), add an explicit note that this is relative to the three reported conditions and that the calibration-vs-anchoring confound prevents attributing the alignment to generalizable few-shot learning.

### Priority 4 (Recommended): Address Kappa Non-Independence

Either compute agreement on aggregated (majority-vote) LLM recommendations at the cell level or add an explicit caveat in the results section (not just the limitations) about the non-independence of pairs.

### Priority 5 (Recommended): Clarify Temperature Confound

State explicitly in the methods or results that vendor comparisons are confounded with temperature settings and should not be interpreted as reflecting inherent differences between LLM models.

### Priority 6 (Recommended): Report Human Reviewer Clustering

Provide individual reviewer means or ICCs in the supplementary materials to characterize the degree of within-reviewer consistency in the human data.

### Priority 7 (Minor): Clarify Abstract Counts

Revise "63 LLM reviews" to something like "63 LLM reviews entered the primary comparisons" and clarify that the human reference group comprised 12 reviews in Experiment 1 and 8 in Experiments 2-3.

---

## Appendix: Verification Methodology

All numerical claims were verified by querying the raw SQLite database at `data/results.db` using the `combined_reviews` table. Cell means were computed as the average of three iterations per vendor-application combination. Glass's delta was computed as (LLM mean - Human mean) / Human SD (ddof=1). Pair-level agreement was computed by crossing all human reviews with all LLM reviews within each application for each experiment. The ANOVA was computed using `scipy.stats.f_oneway`. All computations were performed in Python 3 with numpy and scipy.
