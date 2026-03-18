# Evaluating Large Language Models as Grant Reviewers: A Comparative Study of Prompt Engineering Strategies

Hants Williams^1\*, Jack Lamberg^2, Eric Lamberg^1

1. School of Health Professions, Stony Brook University, Stony Brook, NY, USA
2. Binghamton University, Binghamton, NY, USA 

\* Correspondence: Hants Williams, hants.williams@stonybrook.edu

**Keywords:** large language models, grant review, peer review, prompt engineering, artificial intelligence, few-shot learning, research funding, natural language processing

## Abstract

Grant application review is resource-intensive and subject to inter-rater variability. Large language models (LLMs) may augment this process, but their reliability in grant evaluation remains unexplored. This exploratory pilot study compared LLM-generated grant reviews to human expert reviews across three prompt engineering strategies: zero-shot (no examples), few-shot (multiple training examples), and few-shot with strict scoring instructions. Three commercial LLMs (OpenAI GPT-5 Nano, Google Gemini 2.5 Flash, xAI Grok 4 Fast Reasoning) each reviewed three de-identified faculty seed grant applications ($5,000 awards) under each condition, generating 63 LLM reviews compared against 12 human expert reviews. Among the three conditions tested, few-shot prompting produced scores closest to human reviewers (mean difference: -2.57 points on a 100-point scale, p = 0.671, Glass's Δ = -0.19), though this alignment may partly reflect anchoring to the training application's score range rather than generalizable calibration. Zero-shot prompting showed moderate optimism bias (+4.55 points, p = 0.347) and strict instructions produced substantial under-scoring (-10.68 points, p = 0.097). LLMs demonstrated 49–59% lower score dispersion than humans (49% in Experiment 1; 59% in Experiments 2–3), and likely reflects range restriction: LLMs compressed scores into a narrow band and failed to consistently reproduce the human rank ordering of applications. These preliminary findings suggest that prompt engineering substantially affects LLM scoring behavior, but LLMs cannot yet reliably replicate human grant review judgments.

## 1 Introduction

The evaluation of research grant applications is a cornerstone of academic funding, yet it remains resource-intensive, placing substantial demands on expert reviewers (1, 2). Studies have consistently identified bias and inter-rater inconsistency as persistent limitations of peer review (3, 4). Large language models (LLMs) have demonstrated consistency in applying structured evaluation criteria (5) and may reduce the burden of initial screening in peer review workflows (6), suggesting potential advantages for grant review. However, significant concerns remain about whether LLMs can capture the nuanced judgment that experienced human reviewers bring to holistic evaluation, and prior research has documented "optimism bias" in LLM evaluations (7).

A growing body of evidence suggests that LLM performance is highly sensitive to prompt engineering: the design of instructions and examples provided to guide model behavior (8, 9). Despite the recognized importance of prompt design, no prior study has systematically compared prompt engineering strategies in the context of grant review. While several studies have explored LLM applications in journal manuscript peer review (10, 11), the grant review context presents unique challenges: assessment across diverse criteria (innovation, methodology, team, budget, feasibility), evaluation of proposed rather than completed research, and funding decisions with direct financial implications.

This exploratory pilot study investigated whether LLMs can generate grant review scores that align with human expert reviewers and how different prompt engineering strategies affect this alignment. We tested three conditions: (1) zero-shot prompting with only rubric instructions, (2) few-shot prompting with multiple human review examples demonstrating natural score variance, and (3) few-shot prompting combined with explicit strict scoring instructions. Three commercial LLMs (OpenAI GPT-5 Nano, Google Gemini 2.5 Flash, xAI Grok 4 Fast Reasoning) were evaluated across all conditions using applications from an institutional seed grant program.

## 2 Method

### 2.1 Study Design

We conducted a multi-condition, multi-vendor comparative evaluation at Stony Brook University School of Health Professions using applications from the Research Seed Grant Program (awards up to $5,000). This study was approved by the Stony Brook University IRB (Protocol: IRB2025-00534, classified as non-human subjects research). All applicants provided informed consent; one applicant declined and was excluded.

### 2.2 Grant Applications and Human Reviews

Three de-identified applications (pseudonymized as FC1, FC2, and FC3) were each independently reviewed by four expert reviewers (n = 12 total human reviews). Reviewers held doctoral degrees with minimum 5 years of research experience and prior grant review experience. All reviews used a standardized six-criterion rubric totaling 100 points: Innovation and Impact (30), Research Methods (30), Team Qualifications (10), Funding Potential (10), Budget (10), and Writing Quality (10). Reviewers also provided a funding recommendation: Fund, Fund with Revisions, or Do Not Fund.

### 2.3 Experimental Conditions

Three prompt engineering strategies were tested (Table 1). To prevent data contamination in experiments using training examples (Experiments 2–3), FC3's application and its four human reviews served as training data and were excluded from all comparisons in those experiments.

**Experiment 1 (Zero-Shot):** LLMs received only evaluation instructions, the scoring rubric, and application text, with no training examples. All 12 human reviews served as the comparison group (27 LLM reviews: 3 vendors × 3 applicants × 3 iterations).

**Experiment 2 (Few-Shot):** LLMs received all four human reviews of FC3's application as training examples demonstrating natural score variance (range: 61–80 points). Only FC1 and FC2 reviews were compared (18 LLM reviews vs. 8 human reviews).

**Experiment 3 (Few-Shot + Strict):** Same training examples as Experiment 2, supplemented with explicit instructions to apply conservative scoring (e.g., "Apply high standards," "Reserve high scores for truly exceptional proposals," "Be critical in your assessment"). Same comparison groups as Experiment 2 (18 LLM vs. 8 human reviews).

### 2.4 LLM Configuration

Three commercial LLMs were evaluated using October 2025 API versions: OpenAI GPT-5 Nano (gpt-5-nano-2025-08-07), Google Gemini 2.5 Flash (gemini-2.5-flash), and xAI Grok 4 Fast Reasoning (grok-4-fast-reasoning). xAI Grok used temperature = 0.1 and max tokens = 4000; OpenAI and Google models used default API parameters (documented default temperature = 1.0 for both vendors at the time of data collection). The low temperature setting for xAI Grok may contribute to lower output variability for that vendor. No system prompts were used beyond the experimental prompt templates. Three independent iterations per vendor-application-experiment combination yielded 81 LLM reviews across the three experiments (27 per experiment), of which 63 entered the primary analyses (all 27 in Experiment 1; 18 each in Experiments 2–3 after excluding the training application). No LLM calls failed or were excluded; one criterion-level value (Team Strength) was missing from a single review but the total score was still produced.

### 2.5 Statistical Analysis

Given the small sample size (n = 3 applications) and the nested structure of the data, all statistical analyses should be interpreted as exploratory rather than confirmatory. Because each LLM produced three non-independent repeated outputs per application, these iterations were averaged within each vendor-application combination to yield a single representative score, resulting in 9 independent LLM observations in Experiment 1 (3 vendors × 3 applications) and 6 in each of Experiments 2 and 3 (3 vendors × 2 applications). Within-experiment t-tests compared these averaged LLM scores against individual human scores. Effect sizes were calculated using Glass's Δ, which uses the human group's standard deviation as the baseline; this measure was chosen because LLM scores showed roughly 2.5 times less variability than human scores. We report 95% confidence intervals for mean differences; confidence intervals for Glass's Δ were computed via bias-corrected bootstrap (10,000 resamples).

Human scores are treated as independent observations in the t-tests, though the four reviewers each scored all applications, introducing correlation among scores from the same reviewer that the t-tests do not account for; this may reduce effective degrees of freedom below nominal values. To compare LLM scores across prompt conditions, a one-way ANOVA was restricted to the two applications common to all experiments (FC1 and FC2) to ensure balanced group sizes. Criterion-level analyses are exploratory; to control for multiple comparisons across the six scoring criteria within each experiment, Holm-Bonferroni correction was applied, and both uncorrected and corrected p-values are reported. Recommendation agreement was assessed using Cohen's κ, a chance-corrected measure of agreement, at both the exact category level (Fund/Fund with Revisions/Do Not Fund) and the broad level (positive vs. negative funding direction), computed over all human-LLM review pairs within each application. Analyses were conducted in Python 3.13 using the following python packages: scipy, scikit-learn, and pandas.

## 3 Results

### 3.1 Overall Score Alignment

Table 1 summarizes results across all three experiments. All LLM statistics use averaged scores (aggregated across 3 iterations per vendor-application combination) as described in Section 2.5.

In the zero-shot condition (Experiment 1), LLMs scored applications 4.55 points higher than humans (83.63 ± 5.24 vs. 79.08 ± 13.32; p = 0.347, Glass's Δ = 0.34, 95% CI [-0.28, 1.18]), indicating moderate optimism bias.

Few-shot prompting (Experiment 2) achieved the best alignment, with LLMs scoring 2.57 points below humans (80.56 ± 4.81 vs. 83.13 ± 13.73; p = 0.671, Glass's Δ = -0.19, 95% CI [-1.44, 0.59]), a non-significant difference representing approximately 3% of the total scale.

Adding strict instructions (Experiment 3) produced substantial under-scoring, with LLMs scoring 10.68 points below humans (72.44 ± 4.98 vs. 83.13 ± 13.73; p = 0.097, Glass's Δ = -0.78, 95% CI [-2.61, -0.08]). This trend did not reach statistical significance; notably, the bootstrap confidence interval for the mean difference ([-20.11, -1.03]) excludes zero while the parametric p-value does not, a discrepancy that reflects the different assumptions of each method, which can diverge with small samples.

One-way ANOVA restricted to the common application base (FC1 and FC2 only, n = 6 per experiment) confirmed significant differences in averaged LLM scores across prompt conditions (F(2,15) = 8.18, p = 0.004, η² = 0.522).

**Table 1. Summary of experimental results across three prompt engineering conditions.**

| Metric | Exp 1: Zero-Shot | Exp 2: Few-Shot | Exp 3: Few-Shot + Strict |
|---|---|---|---|
| Human reviews (n) | 12 | 8 | 8 |
| LLM reviews (n raw / aggregated) | 27 / 9 | 18 / 6 | 18 / 6 |
| Human mean ± SD | 79.08 ± 13.32 | 83.13 ± 13.73 | 83.13 ± 13.73 |
| LLM mean ± SD (aggregated) | 83.63 ± 5.24 | 80.56 ± 4.81 | 72.44 ± 4.98 |
| Mean difference [95% CI] | +4.55 [-3.36, +12.33] | **-2.57 [-11.83, +6.97]** | -10.68 [-20.11, -1.03] |
| p-value (aggregated) | 0.347 | **0.671** | 0.097 |
| Glass's Δ [95% CI] | 0.34 [-0.28, 1.18] | **-0.19 [-1.44, 0.59]** | -0.78 [-2.61, -0.08] |
| Broad agreement (pair-level) | 58.3% | **75.0%** | 58.3% |
| Cohen's κ (broad) | 0.000 | **0.100** | -0.071 |
| Exact agreement (pair-level) | 33.3% | **30.6%** | 22.2% |
| Cohen's κ (exact) | 0.061 | **0.020** | -0.037 |

Note: LLM scores were averaged across 3 iterations within each vendor-application combination before statistical testing. Glass's Δ uses the human SD as the baseline. 95% CIs computed via bias-corrected bootstrap (10,000 resamples). Agreement percentages and Cohen's κ are computed over all human-LLM review pairs per application (n = 108 pairs for Exp 1; n = 72 for Exps 2–3). Bold indicates best alignment.

### 3.2 Criterion-Level Performance

Criterion-level analyses are exploratory and should be interpreted with caution given the small sample. In the zero-shot condition, the largest deviations were on Methodology (+2.81 points, uncorrected p = 0.264) and External Funding Potential (+1.11 points, uncorrected p = 0.064); neither reached significance after Holm correction (all corrected p > 0.38). Few-shot prompting reduced criterion-level deviations: no criterion showed significant differences in Experiment 2, with the largest deviation being Budget Clarity (-0.99 points). Under strict instructions (Experiment 3), the largest deviation was on Innovation and Impact (-2.61 points, uncorrected p = 0.031, Holm-corrected p = 0.186). No criterion-level comparison reached statistical significance after correction for multiple comparisons in any experiment.

### 3.3 Vendor Performance

Vendor alignment varied descriptively across conditions (Table 2); no inferential statistics are reported for vendor comparisons given the small sample, and these observations may reflect sampling variability as well as confounding with temperature settings (xAI Grok used temperature = 0.1 vs. 1.0 for other vendors). In the few-shot condition, xAI Grok achieved the closest alignment with human scores (+0.21 points from human mean). Google Gemini shifted from the strongest optimism in Experiment 1 (+9.36) to slight under-scoring in Experiment 2 (-0.79). Under strict instructions, all vendors scored below the human mean, with OpenAI (-13.29) and xAI (-13.62) showing the largest deviations.

**Table 2. LLM vendor mean scores and deviation from human mean across experiments.**

| Vendor | Exp 1 (deviation) | Exp 2 (deviation) | Exp 3 (deviation) |
|---|---|---|---|
| Gemini 2.5 Flash | 88.44 (+9.36) | 82.33 (-0.79) | 78.00 (-5.12) |
| GPT-5 Nano | 77.33 (-1.75) | 76.00 (-7.12) | 69.83 (-13.29) |
| Grok 4 | 85.11 (+6.03) | **83.33 (+0.21)** | 69.50 (-13.62) |

Bold indicates best alignment.

### 3.4 Recommendation Agreement and Consistency

Pair-level exact recommendation agreement ranged from 22.2% to 33.3% across experiments, but Cohen's κ values were near zero (exact κ: 0.061, 0.020, -0.037; broad κ: 0.000, 0.100, -0.071 for Experiments 1–3), indicating agreement at or below chance levels. These κ estimates should be interpreted cautiously because each human review is paired with multiple LLM reviews, creating non-independent pairs that may affect the estimates. LLMs consistently favored "Fund with Revisions" (52–78%) compared to humans (25%). In the zero-shot condition, LLMs generated zero "Do Not Fund" recommendations; strict instructions increased this to 27.8% but at the cost of zero "Fund" recommendations. Broad pair-level agreement was highest in Experiment 2 (75.0%) compared to 58.3% in Experiments 1 and 3, though κ values indicate this largely reflects chance overlap in how often each group chose the same category rather than true systematic agreement.

LLMs demonstrated substantially lower score variability across all conditions, with average within-applicant standard deviations of 5.18–5.78 points compared to 11.37–12.56 for humans, representing a 49% reduction in Experiment 1 and 59% in Experiments 2–3. However, this lower variability likely reflects a compressed scoring range rather than superior consistency. LLMs did not consistently differentiate between applications: in Experiment 1, LLMs ranked all three applications within a narrow 2.4-point range (82.1–84.6) while humans distinguished a wider 18.2-point spread (71.0–89.2). LLMs matched the human rank ordering of applications only in Experiment 2.

## 4 Discussion

This exploratory pilot study provides case-study-level evidence on the effects of prompt engineering on LLM grant review scoring, based on three applications at a single institution. No experimental condition produced statistically significant score differences from human reviewers after accounting for repeated iterations, though descriptive patterns were informative. Few-shot prompting with diverse training examples (Experiment 2) produced the smallest deviation from human scores (-2.57 points, p = 0.671), while both zero-shot and strict instruction approaches introduced larger biases in opposing directions. On a common application base (FC1 and FC2 only), mean LLM scores ranged from 84.4 (zero-shot) to 72.4 (strict), an 11.9-point spread attributable to prompt condition, underscoring that prompt engineering substantially affects LLM scoring behavior. In the best-aligned experiment (Experiment 2), vendor-level spread (7.3 points) was smaller than the cross-experiment prompt effect (11.9 points), though this pattern was not consistent (Experiment 1 vendor spread: 11.1 points). However, the improved alignment in Experiment 2 cannot be definitively attributed to generalizable few-shot learning, as discussed in the limitations.

The counterproductive effect of strict instructions (Experiment 3) is noteworthy. Adding directives to "be critical" shifted LLM scores from near-alignment to substantial under-scoring (10.68 points below human mean), though this difference did not reach statistical significance after accounting for repeated iterations (p = 0.097). One speculative explanation is that LLMs may prioritize explicit instructions over the calibrating influence of training examples, a tendency sometimes described as instruction compliance bias (12); however, this interpretation cannot be confirmed from our data alone. If replicated, this pattern would suggest that providing examples of desired scoring behavior may be more effective than directive language for calibrating LLM outputs.

The gap between how well scores aligned and how poorly recommendations agreed warrants attention. Even in the best-aligned condition, LLMs overwhelmingly favored "Fund with Revisions" (77.8% in Experiment 2 vs. 25% for humans), achieved only 30.6% pair-level exact agreement, and produced near-zero chance-corrected agreement (Cohen's κ: -0.04 to 0.10 across experiments), indicating that the observed agreement was largely due to chance overlap rather than true concordance. LLMs may default to intermediate options when uncertain, consistent with documented ambiguity aversion in AI systems (13). The mapping from scores to funding recommendations likely involves implicit thresholds that LLMs cannot infer from rubrics alone.

A potential source of LLM scoring variance is the absence of an explicit operational definition of "seed grant" in our prompts. While human reviewers share institutional understanding of seed grant expectations, LLMs must infer this from training data that likely over-represents larger funding mechanisms (e.g., NIH R01), potentially creating a mismatch in evaluation standards. Future implementations may benefit from including explicit construct definitions alongside rubrics and examples.

### 4.1 Limitations

Several limitations constrain the generalizability of these findings. Most fundamentally, only three applications from a single institution were evaluated, meaning the study cannot distinguish prompt engineering effects from application-specific effects. The 11.9-point spread in LLM means across prompt conditions (on a common application base) could be confounded with idiosyncratic application characteristics. All statistical tests are underpowered given these effective sample sizes (9 or 6 aggregated LLM observations per experiment), and p-values should be interpreted as descriptive guides rather than confirmatory evidence.

The few-shot training examples in Experiments 2 and 3 were derived from reviews of a single application (FC3), with human scores ranging from 61 to 80 points. This makes it difficult to determine whether the LLM learned general scoring behavior or simply anchored to that particular application's score range; the improved alignment in Experiment 2 could reflect either mechanism. Future studies should use training examples drawn from multiple applications to separate these effects.

Additionally, while repeated LLM iterations were addressed through averaging, human scores remain nested within four reviewers who each scored all applications, introducing correlation among scores from the same reviewer that the t-tests do not account for. Cohen's κ was computed over all human-LLM review pairs per application, creating non-independent pairs that may affect the κ estimates; however, given that all κ values were near zero, this is unlikely to change the overall conclusion of chance-level agreement.

The observed 49–59% reduction in LLM score variability should be interpreted cautiously. LLMs compressed scores into a narrow range and failed to rank applications in the same order as humans in two of three experiments, suggesting that this lower variability reflects a narrower scoring range and reduced sensitivity to differences in application quality rather than superior consistency. The low-temperature setting for xAI Grok (0.1) may further contribute to reduced variability for that vendor. The seed grant context ($5,000) may not generalize to larger, more complex grants. Model versions tested (October 2025) may perform differently from current versions. The retrospective design and lack of preregistration should also be noted. Despite these limitations, the systematic experimental design with appropriate controls for data contamination provides a methodological framework for future, larger-scale studies.

### 4.2 Implications and Future Directions

These findings generate several hypotheses for future testing. First, the observation that few-shot prompting without directive language produced the best-aligned scores warrants replication with larger application pools and training examples drawn from multiple applications. Second, the gap between score calibration and recommendation agreement suggests that these may require separate calibration strategies in future implementations. Third, the near-zero kappa values across all conditions indicate that LLM-generated funding recommendations do not yet provide meaningful signal beyond chance, reinforcing that any future hybrid model must retain human authority over funding decisions. Future research should employ larger, multi-institutional application samples, mixed-effects models to properly account for the nested data structure, and preregistered designs to enable confirmatory inference.

## Conflict of Interest

The authors declare that the research was conducted in the absence of any commercial or financial relationships that could be construed as a potential conflict of interest.

## Author Contributions

HW: Conceptualization, Methodology, Software, Formal Analysis, Investigation, Data Curation, Writing – Original Draft, Writing – Review & Editing, Project Administration. JL: Writing – Review & Editing. EL: Writing – Review & Editing.

## Funding

None. 

## Acknowledgments

The authors thank the grant applicants who consented to participate and the anonymous reviewers whose data made this research possible.

## Data Availability Statement

The analysis code and anonymized review scores are publicly available at: https://github.com/hantswilliams/sbu-seedgrant-llm-grantreviewer. Additional data are available upon reasonable request.

## References

1. Guthrie S, Klemperer S, Lichten CA. Innovating in the Research Funding Process: Peer Review Alternatives and Adaptations. AcademyHealth (2019).
2. National Institutes of Health. Simplified Peer Review Framework: Background. U.S. Department of Health and Human Services (2024).
3. Marsh HW, Jayasinghe UW, Bond NW. Improving the peer-review process for grant applications: Reliability, validity, bias, and generalizability. *Am Psychol* (2008) 63(3):160–168. doi: 10.1037/0003-066X.63.3.160
4. Pier EL, Brauer M, Filut A, Kaatz A, Raclaw J, Mitchell DA, et al. Low agreement among reviewers evaluating the same NIH grant applications. *PNAS* (2018) 115(12):2952–2957. doi: 10.1073/pnas.1714379115
5. Zhang DW, Boey M, Tan YY, Jia AHS. Evaluating large language models for criterion-based grading from agreement to consistency. *npj Sci Learn* (2024) 9:79. doi: 10.1038/s41539-024-00291-1
6. Checco A, Bracciale L, Loreti P, Pinfield S, Bianchi G. AI-assisted peer review. *Humanit Soc Sci Commun* (2021) 8:25. doi: 10.1057/s41599-020-00703-8
7. Liang W, Zhang Y, Cao H, Wang B, Ding D, Yang X, et al. Can Large Language Models Provide Useful Feedback on Research Papers? A Large-Scale Empirical Analysis. arXiv:2310.01783 (2024).
8. Wei J, Wang X, Schuurmans D, Bosma M, Ichter B, Xia F, et al. Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS* (2022).
9. Sahoo P, Singh AK, Saha S, Jain V, Mondal S, Chadha A. A Systematic Survey of Prompt Engineering in Large Language Models: Techniques and Applications. arXiv:2402.07927 (2024).
10. Hosseini M, Horbach SPJM. Fighting reviewer fatigue or amplifying bias? Considerations on the use of AI and generative AI in scholarly peer review. *Res Integr Peer Rev* (2023) 8:4. doi: 10.1186/s41073-023-00133-5
11. Hultgren AR, Carnahan ND, Bhatt DL, Lauer MS. Blinding reviewers to applicants' institutional affiliations reduces institutional prestige bias in research funding. *eLife* (2025).
12. Perez E, Ringer S, Lukosiute K, Nguyen K, Chen E, Heiner S, et al. Discovering Language Model Behaviors with Model-Written Evaluations. arXiv:2212.09251 (2022).
13. Zhao A, Wu Z, Awadallah A, Smith NA. Uncertainty and Ambiguity Aversion in Large Language Models. arXiv:2402.03408 (2024).

## Supplementary Material

Full prompt templates for all experimental conditions and detailed criterion-level statistical tables are available as Supplementary Material.
