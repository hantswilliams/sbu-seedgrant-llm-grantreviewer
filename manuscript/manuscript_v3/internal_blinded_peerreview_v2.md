# Blinded Peer Review (V2 — Revised Manuscript)

## 0) Material Inventory and Review Scope

Sections received: Abstract, Introduction, Methods (2.1–2.5), Results (3.1–3.4), Discussion (4.0–4.2), Tables 1–2 (inline), Conflict of Interest, Author Contributions (incomplete), Funding, Acknowledgments, Data Availability Statement, References (1–13).

Sections/materials NOT received:

- Supplementary materials (referenced at end of manuscript: "Full prompt templates for all experimental conditions and detailed criterion-level statistical tables are available as Supplementary Material")
- Figures (none appear in this manuscript version)
- Author Contributions section remains incomplete ("Need to insert")

Review confidence: **Limited** — Supplementary materials containing prompt templates and criterion-level statistical tables are still not available for verification. Claims about criterion-level analyses (Section 3.2) and the nature of strict scoring instructions (Section 2.3) cannot be fully audited.

## 1) Overall Recommendation

**Minor Revision**

The revised manuscript represents a substantial improvement over the prior version. The pseudoreplication issue has been addressed through cell-mean aggregation, effect sizes now use an appropriate formula (Glass's delta), chance-corrected agreement is reported, multiple comparisons are corrected, and claims have been substantially tempered to match the case-study evidence level. Several moderate concerns remain, primarily around confidence intervals, residual non-independence in human scores, and manuscript completeness.

## 2) Summary Assessment

This exploratory pilot study compares three prompt engineering strategies (zero-shot, few-shot, few-shot + strict) across three commercial LLMs reviewing three de-identified seed grant applications, benchmarked against 12 human expert reviews. The revised manuscript addresses the most serious concerns from the prior review: pseudoreplication is handled through vendor-application cell-mean aggregation, Glass's delta replaces the unspecified Cohen's d, Cohen's kappa provides chance-corrected agreement, Holm-Bonferroni correction is applied to criterion-level analyses, and claims are reframed throughout as exploratory case-study evidence. The key finding that Experiment 3 (strict instructions) is no longer statistically significant (p = 0.097) after correction represents an honest and consequential revision. The manuscript now appropriately foregrounds the limitations of its small effective sample size.

## 3) Fatal Flaws

No fatal flaws were identified.

## 4) Major Concerns

No major concerns were identified. The prior major concerns (pseudoreplication, independence violations, small sample overclaiming, single-application training confound, multiple comparisons) have all been addressed to an adequate or substantially improved degree.

## 5) Moderate Concerns

### 5.1 Confidence intervals not reported for any effect estimate

Issue: Glass's delta values are reported without confidence intervals. No uncertainty intervals are provided for mean differences, kappa values, or the ANOVA effect.

Where it appears: Table 1, Results 3.1, throughout.

Why it matters: Point estimates without intervals provide no information about precision. Given the small sample sizes (n = 6–12), confidence intervals would likely be wide and informative for interpretation. For example, the Glass's Δ = -0.78 (Experiment 3) with n = 8 and n = 6 could have a 95% CI spanning from near zero to well beyond -1.5, which would contextualize the p = 0.097 finding.

What would strengthen it: Report 95% confidence intervals for Glass's delta (bootstrap or analytic), mean differences, and Cohen's kappa values. If intervals are computationally burdensome for kappa, note this limitation.

### 5.2 Human scores also exhibit non-independence

Issue: The aggregation strategy addresses pseudoreplication on the LLM side (averaging 3 iterations within vendor-application cells), but human scores are treated as independent observations despite being nested within 4 reviewers. Each human reviewer scored all 3 (or 2) applications, introducing within-reviewer correlation that the t-tests do not account for.

Where it appears: Methods 2.5, Results 3.1.

Why it matters: If human reviewers have systematic scoring tendencies (e.g., one reviewer consistently scores 10 points higher), the 12 human scores are not fully independent. This is a lesser concern than the original pseudoreplication (since human reviewers are genuinely different individuals, unlike repeated LLM iterations), but the nesting is real and unacknowledged.

What would strengthen it: Acknowledge this residual non-independence as a limitation, or note that the ideal approach would be a mixed-effects model with both reviewer and application as random effects. The current approach is a reasonable pragmatic compromise given the sample size.

### 5.3 Cohen's kappa computed on non-independent pairs

Issue: Methods 2.5 states kappa was "computed over all human-LLM review pairs within each application." This creates non-independent pairs: a single LLM review is paired with each of 4 human reviews, and a single human review is paired with each of 9 (or 6) LLM reviews. The resulting pair counts (n = 108 for Experiment 1; n = 72 for Experiments 2–3) overstate the effective sample size for kappa estimation.

Where it appears: Methods 2.5, Table 1, Results 3.4.

Why it matters: Non-independent pairs can bias kappa estimates and inflate apparent precision. The direction of bias depends on the marginal distributions. Given the near-zero kappa values, this is unlikely to change the qualitative conclusion, but it should be acknowledged.

What would strengthen it: Acknowledge the non-independence of kappa pairs as a limitation. Alternatively, compute kappa on modal (majority-vote) recommendations per application, yielding 3 (or 2) independent paired observations per experiment — though this would make kappa estimation unstable with so few observations.

### 5.4 Inconsistency in model naming across sections

Issue: The Introduction (paragraph 3) lists "OpenAI GPT-5 Nano, Google Gemini 2.5 Flash, xAI Grok 4" but the Abstract lists "xAI Grok 4 Fast Reasoning" with the full qualifier. Methods 2.4 uses the full name "xAI Grok 4 Fast Reasoning (grok-4-fast-reasoning)." Table 2 uses the abbreviated forms "Google Gemini," "OpenAI GPT-5 Nano," and "xAI Grok."

Where it appears: Abstract, Introduction, Methods 2.4, Table 2.

Why it matters: Inconsistent naming across sections could cause confusion about whether the same models are being referenced. Minor but should be standardized.

What would strengthen it: Introduce the full name with API identifier once in Methods 2.4, then use a consistent short form throughout (e.g., "GPT-5 Nano," "Gemini 2.5 Flash," "Grok 4").

### 5.5 Default temperature claim may be inaccurate

Issue: Section 2.4 states "OpenAI and Google models used default API parameters (temperature = 1.0)." The parenthetical asserts the default is 1.0 for both vendors. Default temperature values can vary by model and API version; Google Gemini's default may differ from 1.0.

Where it appears: Methods 2.4.

Why it matters: If the actual default temperature for Gemini 2.5 Flash is not 1.0, the reported parameter is incorrect. Since temperature directly affects output variability, this matters for reproducibility and for interpreting between-vendor variability differences.

What would strengthen it: Verify and report the actual default temperature for each model, or state "default API parameters" without asserting a specific value unless confirmed.

### 5.6 ANOVA effect size not reported

Issue: The one-way ANOVA reports F(2,18) = 8.99, p = 0.002 but does not report an effect size measure (eta-squared or partial eta-squared). The original manuscript reported η² = 0.478, which was removed in revision.

Where it appears: Results 3.1.

Why it matters: The p-value alone does not convey the magnitude of the cross-experiment difference. An effect size helps readers judge practical significance.

What would strengthen it: Report eta-squared for the corrected ANOVA on aggregated cell means.

## 6) Minor Concerns

### 6.1 Author Contributions section incomplete

Issue: Section reads "Need to insert."

Where it appears: Author Contributions.

Why it matters: Incomplete for submission. Unchanged from prior review.

### 6.2 Tangential references (5 and 6)

Issue: Reference 5 (Brown et al., 2020, "Language Models are Few-Shot Learners") is the GPT-3 paper, cited to support "potential advantages for grant review." Reference 6 (Goldfarb & Teodorescu, 2023) is a marketing journal paper cited in the same context. Neither directly supports claims about LLM advantages in grant review.

Where it appears: Introduction, paragraph 1.

Why it matters: Weak citation support for a motivating claim. There are now more directly relevant references available on LLMs in scholarly evaluation (e.g., papers from the 2024–2025 wave of LLM peer review studies).

What would strengthen it: Replace or supplement with references that more directly address LLM capabilities in structured evaluation or review tasks.

### 6.3 "49–59% reduction" range depends on cross-experiment SD pairing

Issue: The "49–59% reduction in score dispersion" is computed by comparing the smallest LLM within-applicant SD with the largest human within-applicant SD (yielding 59%) and the largest LLM SD with the smallest human SD (yielding 49%). This is not incorrect, but it obscures that within any single experiment the reduction is more consistent (approximately 49% in Experiment 1, 59% in Experiments 2–3).

Where it appears: Abstract, Results 3.4.

Why it matters: Minor reporting clarity issue.

What would strengthen it: Consider reporting per-experiment reduction values or specifying that the range spans experiments.

### 6.4 LLM range in Experiment 1 stated as 2.5 points

Issue: Results 3.4 states "LLMs ranked all three applications within a narrow 2.5-point range (82.1–84.6)." The actual range is 84.56 − 82.11 = 2.44, which rounds to 2.4 rather than 2.5.

Where it appears: Results 3.4.

Why it matters: A rounding discrepancy of 0.1 points. Negligible for interpretation but should be corrected for precision.

### 6.5 Supplementary materials still not available

Issue: The manuscript references supplementary materials containing prompt templates and criterion-level tables, but these are still not provided.

Where it appears: End of manuscript.

Why it matters: Prompt templates are essential for evaluating whether the strict instructions in Experiment 3 were appropriate in degree and wording. The brief quotes provided ("Apply high standards," "Reserve high scores for truly exceptional proposals," "Be critical in your assessment") are partial. Full evaluation of the experimental manipulation requires the complete prompts. This was flagged in the prior review and remains unresolved.

## 7) Internal Consistency Audit

The following numerical checks were performed against the raw data:

Total LLM reviews: 27 + 18 + 18 = 63. ✓ Matches abstract and methods.
Human reviews per experiment: 12 (Exp 1), 8 (Exp 2), 8 (Exp 3). ✓ Consistent with design.
Aggregated LLM observations: 9 (Exp 1), 6 (Exp 2), 6 (Exp 3). ✓ Matches 3 vendors × 3 or 2 applicants.

Mean differences from Table 1:
- Exp 1: 83.63 − 79.08 = +4.55 ✓
- Exp 2: 80.56 − 83.13 = −2.57 ✓ (actual computation: 80.556 − 83.125 = −2.569 ≈ −2.57)
- Exp 3: 72.44 − 83.13 = −10.69 (Table reports −10.68; rounding within ±0.01)

Table 2 vendor means averaging to Table 1 LLM means:
- Exp 1: (88.44 + 77.33 + 85.11) / 3 = 83.63 ✓
- Exp 2: (82.33 + 76.00 + 83.33) / 3 = 80.55 (Table 1 reports 80.56; rounding within ±0.01)
- Exp 3: (78.00 + 69.83 + 69.50) / 3 = 72.44 ✓

Table 2 deviations from human mean: All check within ±0.01 rounding tolerance. ✓

Discussion "15.2-point swing": +4.55 to −10.68 = 15.23 ≈ 15.2 ✓

Discussion "7.3-point vendor spread" (Experiment 2): 83.33 − 76.00 = 7.33. ✓ Now correctly qualified as applying to Experiment 2 only, with Experiment 1 vendor spread (11.1 points) noted as inconsistent. This addresses the selective comparison flagged in the prior review.

ANOVA df: F(2,18) implies N = 21 total aggregated observations (9 + 6 + 6). df_between = 2, df_within = 18. ✓ Consistent with the aggregated sample.

Cohen's kappa range in Abstract: "−0.07 to 0.10" corresponds to the broad kappa range from Table 1 (−0.071 to 0.100). The exact kappa range (−0.037 to 0.061) differs. The Abstract does not specify which kappa variant is cited, creating minor ambiguity.

LLM "Fund with Revisions" percentages: "52–78%"
- Exp 1: 14/27 = 51.9% ≈ 52% ✓
- Exp 2: 14/18 = 77.8% ≈ 78% ✓
- Exp 3: 13/18 = 72.2% (within the stated range)

Human "25%" Fund with Revisions: 3/12 = 25% (all experiments) ✓

Rank ordering claim (Results 3.4):
- "2.5-point range (82.1–84.6)": Actual values 82.11–84.56, range = 2.44 ≈ 2.4 (reported as 2.5, minor rounding up; see Minor 6.4)
- "18.2-point spread (71.0–89.2)": Actual values 71.0–89.25, range = 18.25 ≈ 18.2 ✓

Missing data statement: "one criterion-level value (Team Strength) was missing from a single review" — verified as row 95 in the dataset (OpenAI GPT-5 Nano, KELLY, strict_scoring_v1, iteration 1). ✓

No material internal numerical inconsistencies were identified beyond the minor rounding issues noted above.

## 8) Statistical Review (Simple-First)

**Denominators:** Clearly defined. The aggregation strategy (cell means) is explicitly described and yields transparent effective sample sizes (9 or 6 LLM observations). This represents a substantial improvement.

**Unit of analysis:** Appropriately shifted from individual iterations to vendor-application cell means for the LLM group. The human group still uses individual reviewer scores, which is reasonable given that human reviewers are genuinely different individuals, though the within-reviewer correlation (each reviewer scoring all applications) is not modeled.

**Missing data:** Reported. One null criterion value out of 63 reviews; total scores unaffected.

**Effect sizes:** Glass's delta with human SD as the reference denominator is appropriate given the ~2.5× variance ratio. The formula is specified. However, confidence intervals for effect sizes are not reported for any comparison (see Moderate 5.1).

**Confidence intervals:** Not reported for mean differences, Glass's delta, or Cohen's kappa. This is the most consequential remaining statistical reporting gap.

**Multiplicity:** Holm-Bonferroni correction is applied to criterion-level comparisons. Both uncorrected and corrected p-values are reported. The designation of criterion-level analyses as "exploratory" is appropriate. The three overall t-tests (one per experiment) are not corrected for multiplicity, which is acceptable given the exploratory framing.

**Clustering/non-independence:** Substantially improved. LLM pseudoreplication is addressed. Residual non-independence from human reviewers scoring multiple applications is not addressed but acknowledged implicitly through the exploratory framing. The kappa computation uses non-independent pairs (see Moderate 5.3).

**Would a simpler analysis be more appropriate?** The current approach is a reasonable pragmatic compromise. The ideal analysis (mixed-effects models with reviewer and application as random effects) is acknowledged in the Future Directions section as a recommendation for subsequent studies. Given only 3 applications and 4 human reviewers, mixed-effects models would likely be unstable, so the cell-mean approach is defensible.

**Primary endpoint clarity:** Clearly defined (total score out of 100).

## 9) Supplementary Materials Assessment

Supplementary materials were not provided for review. The manuscript references them at the end: "Full prompt templates for all experimental conditions and detailed criterion-level statistical tables are available as Supplementary Material."

Impact of missing supplements:

- Prompt templates remain essential for evaluating the appropriateness and degree of the strict scoring instructions in Experiment 3. The quotes provided in Section 2.3 are partial.
- Criterion-level statistical tables underpin the findings reported in Results 3.2. The Holm-corrected p-values cited for specific criteria cannot be verified without these tables.
- This is classified as a Moderate Concern (downgraded from Major in the prior review, since the main text now provides more complete criterion-level reporting with both uncorrected and corrected p-values).

## 10) Claims That Overreach the Evidence

The revised manuscript has substantially improved its claim calibration. The following residual observations are noted:

**Abstract:** "prompt engineering substantially affects LLM scoring behavior" — The ANOVA is significant (p = 0.002), but the three prompt conditions also differ in which applications are included (Experiment 1 includes FC3; Experiments 2–3 do not), confounding prompt effects with application effects. The claim is reasonable but could be more precisely qualified. Suggested direction: "prompt condition was associated with large differences in LLM scoring" or note the application confound inline.

**Discussion:** "the 15.2-point swing in mean LLM scores across experimental conditions" — This swing compares Experiment 1 (3 applications) with Experiment 3 (2 applications), so part of the swing may reflect the exclusion of FC3 rather than the prompt manipulation alone. The within-condition comparison (Experiment 2 vs. Experiment 3, both using the same 2 applications) shows a difference of 80.56 − 72.44 = 8.12 points, which is the cleaner estimate of the strict-instruction effect. This is noted here for precision, not as an error.

**Results 3.4:** "LLMs did not consistently differentiate between applications" — This is stated as a general conclusion but is based on rank-order comparison with only 2–3 applications. With so few applications, rank concordance is an unreliable metric (50% agreement expected by chance for 2 applications; 1/6 or 16.7% for 3 applications). The observation is valid but its statistical interpretation is limited.

No other overclaiming issues were identified. The manuscript's overall claim calibration is now appropriate for the evidence.

## 11) Priority Revisions Before Reconsideration

1. **Report confidence intervals for effect sizes.** At minimum, provide 95% CIs for Glass's delta and mean differences. Bootstrap CIs are straightforward to implement and appropriate for the small sample.

2. **Acknowledge residual non-independence in human scores and kappa pairs.** Add 1–2 sentences in the Limitations section noting that human scores are nested within reviewers and that kappa was computed on non-independent pairs.

3. **Standardize model naming across sections.** Use consistent abbreviations throughout (Abstract, Introduction, Methods, Tables).

4. **Complete the Author Contributions section.**

5. **Verify and clarify default temperature values** for OpenAI and Google APIs, or remove the parenthetical assertion "(temperature = 1.0)."

6. **Provide supplementary materials for review**, including full prompt templates and criterion-level statistical tables.

7. **Correct the "2.5-point range" to "2.4-point range"** in Results 3.4 (or report as "approximately 2.5").
