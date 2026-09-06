# REVIEWER #3 

Initial recommendation to the Editor: Major revision is required


The topic is timely and the methodological transparency is commendable. However, the study's core limitations are more consequential than acknowledged, and several issues require attention before publication:
1. Three grant applications from a single institution is insufficient to separate prompt engineering effects from application-specific effects, as the authors themselves acknowledge. However, this limitation is underplayed in the framing. The manuscript correctly labels these as exploratory, but the Discussion still draws directional conclusions that the data cannot support.
2. The few-shot training set consists of four human reviews of a single application (FC3) with scores ranging 61-80 points. The improved alignment in Experiment 2 is therefore uninterpretable: it cannot be distinguished from simple score anchoring to FC3's range.
3. The recommendation agreement data (Cohen's κ near zero across all experiments) is arguably the most important finding in the manuscript and is underemphasized relative to the score alignment results.
4. The LLM temperature settings are inconsistent across vendors: xAI Grok used temperature = 0.1 while OpenAI and Gemini used default = 1.0. This is a significant confound for all vendor-level comparisons and for the dispersion analysis.
5. The abstract contains a grammatical error: "to be considered in a overall holistic review" - should be "an overall."
6. Reference 11 (Hultgren et al., eLife 2025) does not appear to concern AI peer review - it addresses institutional affiliation blinding. Its citation in the context of LLM applications in manuscript peer review (lines 351-356) appears misplaced. The authors should verify this citation fits the claim it supports.
7. Table 4 quotes are presented as direct excerpts from LLM outputs. The manuscript should clarify whether these are verbatim or lightly edited, and confirm they were not selectively chosen to favor favorable-looking outputs.


Check List
 Reviewer 3 | 25 Apr 2026 | 15:45
#1
a. Is the quality of the figures and tables satisfactory?
- Yes

b. Does the reference list cover the relevant literature adequately and in an unbiased manner?
- No

c. Are the statistical methods valid and correctly applied? (e.g. sample size, choice of test)
- No

d. Is a statistician required to evaluate this study?
- Yes

e. Are the methods sufficiently documented to allow replication studies?
- Yes



# Reviewer 5

Independent review report submitted: 02 Jul 2026
Interactive review activated: 05 Jul 2026

Initial recommendation to the Editor: Major revision is required

 EVALUATION
Q 1

Please list your revision requests for the authors and provide your detailed comments, including highlighting limitations and strengths of the study and evaluating the validity of the methods, results, and data interpretation. If you have additional comments based on Q2 and Q3 you can add them as well.
 Reviewer 5 | 02 Jul 2026 | 21:47
#1
Major Revisions
1.Specify the Gemini 2.5 Flash model version. The manuscript cites only the unversioned alias gemini-2.5-flash. An updated snapshot was released September 25, 2025, meaning the alias used during October 2025 data collection may not match the originally described model. The exact snapshot string must be reported in Section 2.4 or Table 1 to allow replication .

2.Correct reference 14. The citation for Grok 4 Fast Reasoning points to xAI's general homepage rather than the Grok 4 Fast release page (https://x.ai/news/grok-4-fast). Additionally, the authors should specify whether the reasoning or non-reasoning flavor of Grok 4 Fast was used .

3.Revise statistical language to reflect exploratory status. The phrase "confirmed significant differences" in relation to the one-way ANOVA (Section 3.1) implies confirmatory inference, which is not warranted given 6 observations per group. Replace with language consistent with exploratory inference throughout .

4.Address non-independence of human reviewer scores. Four reviewers each scored all three applications. Standard t-tests treat these as independent observations, which inflates the effective degrees of freedom. Either apply a linear mixed-effects model or explicitly quantify the effect of this violation on the reported p-values .

5.Restate the Experiment 2 conclusion. The Abstract and Discussion present few-shot alignment as the primary positive finding, qualified only by the phrase "may partly reflect anchoring." Given that the training data came from a single application with scores between 61 and 80, and LLM test scores averaged 80.56, anchoring is a near-complete alternative explanation. The qualifier should be strengthened and the confound given equal standing with the calibration interpretation .

6.Reclassify the temperature inconsistency as a limitation of vendor comparisons. Grok used temperature 0.1 while GPT-5 Nano and Gemini 2.5 Flash used the vendor default of 1.0. This prevents valid vendor-level comparisons and should be stated as such in Section 2.4. Vendor-specific conclusions in Section 3.3 should carry explicit caveats accordingly .

7.Recompute Cohen's kappa over independent units. Kappa was computed over all human-LLM review pairs, producing n = 108 and n = 72 pairs that are not independent. The same human review appears in multiple pairs and the same LLM output appears in multiple pairs. Recompute using aggregated LLM scores paired with individual human reviews, matching the aggregation used in the t-tests, and describe the computation method explicitly .

8.Consider adding a figure/s. The manuscript contains no figures. Score distributions by experiment with human scores overlaid, or a chart showing application-level rank ordering across conditions, are needed to make the range restriction and dispersion findings interpretable without relying entirely on prose .

9.Include full prompt templates. The prompts used in all three experiments are absent from the Appendix. Without the exact text, the study cannot be replicated. Add these as Appendix B .

Minor Revisions
1.Replace reference 11. Hultgren et al. (2025, eLife) concerns blinding reviewers to institutional affiliations to reduce prestige bias. It is cited as an example of LLM applications in peer review, which it is not. Replace with a citation directly relevant to LLM-assisted peer review .

2.Reconsider reference 15. Perez et al. (arXiv:2212.09251, 2022) does not describe the instruction-following versus in-context learning trade-off cited as "instruction compliance bias." Either cite a more directly relevant source or reframe the claim as speculation .

3.Correct the typographical error on line 260: "wheather" should be "whether" .

4.Fix the abstract grammar: "in a overall holistic review" should read "in an overall holistic review" .

5.Resolve the corresponding author discrepancy. The cover page lists Hants Williams as corresponding author; the manuscript body lists Jack Lamberg. These must agree .

6.Clarify the sample selection. State whether the three applications represent the full eligible pool for that grant cycle or a selected subset.

Add comment
Q 2

Check List
 Reviewer 5 | 02 Jul 2026 | 21:47
#1
a. Is the quality of the figures and tables satisfactory?
- Yes

b. Does the reference list cover the relevant literature adequately and in an unbiased manner?
- No

c. Are the statistical methods valid and correctly applied? (e.g. sample size, choice of test)
- No

d. Is a statistician required to evaluate this study?
- No

e. Are the methods sufficiently documented to allow replication studies?
- No




# Reviewer 4

Independent review report submitted: 17 Jun 2026

Initial recommendation to the Editor: The manuscript should be rejected
This reviewer recommended rejection of the manuscript on 17 Jun 2026. Discussions for this review are closed.
Reason:
Other.

 EVALUATION
Q 1

Please list your revision requests for the authors and provide your detailed comments, including highlighting limitations and strengths of the study and evaluating the validity of the methods, results, and data interpretation. If you have additional comments based on Q2 and Q3 you can add them as well.
 Reviewer 4 | 17 Jun 2026 | 09:40
#1
While the rationale behind this study is timely and relevant, the extremely limited sample size substantially weakens the reliability of the evidence on which the authors base their conclusions. The authors do acknowledge this limitation; however, the small number of cases means that only very limited inferences can be drawn from the data. Perhaps the most interesting observation is the variation in human assessment. The authors argue that the assessment of grant applications represents an increasing burden on the academic system. If this is the central claim, then a substantially larger and more representative sample would be needed to support robust conclusions. In my view, the manuscript remains closer to a preliminary case study than a publishable empirical contribution. Because the study is statistically underpowered and does not provide sufficient evidence to substantiate its broader claims, I do not recommend publication in its current form.

Q 2

Check List
 Reviewer 4 | 17 Jun 2026 | 09:40
#1
a. Is the quality of the figures and tables satisfactory?
- Yes

b. Does the reference list cover the relevant literature adequately and in an unbiased manner?
- Yes

c. Are the statistical methods valid and correctly applied? (e.g. sample size, choice of test)
- Yes

d. Is a statistician required to evaluate this study?
- No

e. Are the methods sufficiently documented to allow replication studies?
- Yes







