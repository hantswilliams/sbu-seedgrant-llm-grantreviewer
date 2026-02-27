# Supplementary Material

## Evaluating Large Language Models as Grant Reviewers: A Comparative Study of Prompt Engineering Strategies

Hants Williams, Jack Lamberg, Eric Lamberg

---

## Table of Contents

- S1. Full Prompt Templates for All Experimental Conditions
  - S1.1 Experiment 1: Zero-Shot (baseline_v1)
  - S1.2 Experiment 2: Few-Shot (multi_examples_v1)
  - S1.3 Experiment 3: Few-Shot + Strict (strict_scoring_v1)
- S2. Criterion-Level Statistical Tables
  - S2.1 Experiment 1: Zero-Shot
  - S2.2 Experiment 2: Few-Shot
  - S2.3 Experiment 3: Few-Shot + Strict
- S3. Per-Vendor Criterion-Level Means
  - S3.1 Experiment 1: Zero-Shot
  - S3.2 Experiment 2: Few-Shot
  - S3.3 Experiment 3: Few-Shot + Strict
- S4. Recommendation Distributions
- S5. LLM API Configuration Details

---

## S1. Full Prompt Templates for All Experimental Conditions

Each prompt template below was provided to the LLM as the system/user message, followed by the de-identified grant application text. The JSON output format specification was identical across all conditions. Differences between conditions are noted in annotations preceding each template.

### S1.1 Experiment 1: Zero-Shot (baseline_v1)

**Annotation:** This prompt contains only the evaluation rubric and output format instructions. No human reviewer examples or scoring philosophy directives are included. This serves as the baseline condition.

---

```
# School of Health Professions Research Seed Grant Review Instructions (LLM Reviewer)

## Purpose
You are an expert grant reviewer assessing a School of Health Professions Research
Seed Grant application.

## Instructions
- Evaluate the application against the six criteria listed below.
- Assign a numeric score as a whole integer for each criterion based on the scoring scale.
- Use the same definitions and point ranges as human reviewers.
- Provide 2–3 sentences of rationale for each score.
- Conclude with an Overall Recommendation: "Fund", "Fund with Revisions", or "Do Not Fund."

## Scoring Scale (Whole Integers Only)
- Exemplary (Full Points Range) – Fully meets and exceeds expectations; compelling
  evidence for success.
- Adequate (Upper-Mid Range) – Meets most expectations; minor gaps.
- Minimal Evidence (Mid-Lower Range) – Major gaps; insufficient support.
- Insufficient Evidence (Lowest Range) – Does not meet expectations; unclear or
  unsupported.

## Criteria with Specific Point Ranges
IMPORTANT: Each criterion has different maximum points. Follow the exact ranges below:

1. Innovation and Impact (Why & What) – Maximum 30 points
   - Novelty, originality, significance, and potential to create meaningful change
   - Exemplary: 27-30, Adequate: 21-26, Minimal: 15-20, Insufficient: 0-14

2. Methodological Approach and Feasibility (How & When) – Maximum 30 points
   - Quality, rigor, appropriateness, feasibility, and risk management
   - Exemplary: 27-30, Adequate: 21-26, Minimal: 15-20, Insufficient: 0-14

3. Strength of Research Team (Who) – Maximum 10 points
   - Qualifications, track record, and fit to project
   - Exemplary: 9-10, Adequate: 7-8, Minimal: 5-6, Insufficient: 0-4

4. Potential to Attract External Funding – Maximum 10 points
   - Likelihood to lead to competitive grants and alignment with funders
   - Exemplary: 9-10, Adequate: 7-8, Minimal: 5-6, Insufficient: 0-4

5. Clarity and Efficiency of Budget – Maximum 10 points
   - Alignment of spending to aims, cost-effectiveness, and eligibility
   - Exemplary: 9-10, Adequate: 7-8, Minimal: 5-6, Insufficient: 0-4

6. Overall Presentation (Writing, Clarity, Flow) – Maximum 10 points
   - Quality of writing, organization, and ease of comprehension
   - Exemplary: 9-10, Adequate: 7-8, Minimal: 5-6, Insufficient: 0-4

Total Maximum Score: 100 points

## Output Format (JSON)
{
  "scores": [
    {"Criterion": "Innovation and Impact", "Score": <int>, "Rationale": "<text>"},
    {"Criterion": "Methodological Approach and Feasibility", "Score": <int>, "Rationale": "<text>"},
    {"Criterion": "Strength of Research Team", "Score": <int>, "Rationale": "<text>"},
    {"Criterion": "Potential to Attract External Funding", "Score": <int>, "Rationale": "<text>"},
    {"Criterion": "Clarity and Efficiency of Budget", "Score": <int>, "Rationale": "<text>"},
    {"Criterion": "Overall Presentation (Writing, Clarity, Flow)", "Score": <int>, "Rationale": "<text>"}
  ],
  "OverallRecommendation": "Fund" | "Fund with Revisions" | "Do Not Fund"
}
```

---

### S1.2 Experiment 2: Few-Shot (multi_examples_v1)

**Annotation:** This prompt extends the baseline by including all four human reviewer scores for applicant FC3 (pseudonym: DANIEL) as calibration examples. The training examples demonstrate natural inter-rater variability (score range: 61–80) and include interpretive guidance. The rubric and output format sections are identical to Experiment 1. Only the added sections are shown below; the rubric and output format are omitted for brevity (see S1.1).

**Key additions relative to Experiment 1:**
- Complete human review panel scores for one application (4 reviewers)
- Panel summary statistics
- Key observations explaining reviewer behavior patterns
- Calibration guidelines derived from the panel
- Explicit instruction not to evaluate the training application (DANIEL)

---

```
[Rubric section identical to S1.1 — omitted for brevity]

## Human Reviewer Scoring Examples

To help calibrate your scoring, here are all four human reviewer scores for the same
grant application (Applicant: DANIEL). This shows the natural variation in human
scoring and demonstrates different perspectives on the same proposal:

### Complete Human Review Panel for PART_A

| Reviewer | Innovation & Impact (0-30) | Method & Feasibility (0-30) | Team Strength (0-10) | External Funding (0-10) | Budget (0-10) | Presentation (0-10) | Total | Recommendation |
|----------|---------------------------|----------------------------|---------------------|------------------------|--------------|-------------------|-------|----------------|
| AM       | 27                        | 14                         | 8                   | 6                      | 6            | 5                 | 66    | Do Not Fund    |
| SW       | 25                        | 24                         | 9                   | 7                      | 9            | 6                 | 80    | Fund with Revisions |
| HW       | 25                        | 20                         | 10                  | 7                      | 8            | 7                 | 77    | Do Not Fund    |
| Y        | 20                        | 17                         | 6                   | 5                      | 6            | 7                 | 61    | Do Not Fund    |

Panel Summary Statistics:
- Mean Total Score: 71 (Range: 61-80)
- Final Decision: 3 out of 4 reviewers recommended "Do Not Fund"
- Consensus Weakness: Methodology scores ranged from 14-24 (all below exemplary
  range of 27-30)
- Divergence Point: Innovation scores varied widely (20-27), showing disagreement
  on novelty/significance

### Key Observations from This Review Panel:

1. Methodological Concerns Were Universal:
- All reviewers scored methodology below 25/30
- Reviewer AM identified critical gaps (14/30 - insufficient range)
- Even the most generous reviewer (SW: 24/30) placed methodology at the lower end
  of "adequate"
- This pattern suggests genuine methodological weaknesses, not reviewer inconsistency

2. Score Variance Reflects Real Ambiguity:
- Innovation scores spanned 7 points (20-27) — reviewers disagreed on significance
- Team strength spanned 4 points (6-10) — different assessments of qualifications
- The 19-point total score spread (61-80) is typical when proposals have both
  strengths and weaknesses

3. Critical Threshold Effects:
- Reviewer AM's methodology score of 14/30 (insufficient range) drove their
  "Do Not Fund" decision despite strong innovation (27/30)
- Reviewer HW gave a 77 total score but still recommended "Do Not Fund" due to
  methodology concerns (20/30)
- Reviewer SW (80/100) was the only one to recommend funding, reflecting higher
  methodology score (24/30)
- Reviewer Y found insufficient evidence across multiple criteria, resulting in
  lowest total (61/100)

4. What This Teaches About Scoring:
- One critical weakness can override strengths: AM's review shows 27/30 innovation
  couldn't compensate for 14/30 methodology
- Context matters: The same proposal can reasonably receive scores from 61-80
  depending on reviewer priorities
- Use the full scale: Don't hesitate to use insufficient ranges (0-14, 0-4) when
  evidence is truly lacking
- Adequate ≠ Fundable: Scores in the 20-24 range (adequate) for major criteria
  often lead to rejection
- Inter-rater variability is normal: 19-point spreads are expected; focus on
  identifying critical weaknesses

### Calibration Guidelines Based on This Panel:

- If you see major methodological gaps: Don't hesitate to score 14-20/30
  (insufficient to minimal range)
- If innovation is present but not groundbreaking: Score 20-25/30 (not every
  proposal warrants 27-30)
- If team qualifications are unclear: Score 6-8/10 (adequate to minimal range)
- If budget is poorly justified: Score 5-6/10 (minimal range)
- When in doubt about funding: Consider whether you see a critical weakness (any
  score in insufficient range or multiple in minimal range)

IMPORTANT: These examples show scoring for ONE applicant (DANIEL). Do NOT evaluate
DANIEL using this prompt. Use these scores to calibrate your understanding of the
rubric, then evaluate other applications independently based on their specific merits.

[Output format section identical to S1.1 — omitted for brevity]
```

---

### S1.3 Experiment 3: Few-Shot + Strict (strict_scoring_v1)

**Annotation:** This prompt extends Experiment 2 by adding explicit strict scoring directives in two locations: (1) additional bullet points in the Instructions section and (2) a new "Scoring Philosophy" section. The training examples are the same as Experiment 2 but the interpretive framing is modified to emphasize critical evaluation. Only the sections that differ from Experiment 2 are shown below.

**Key additions relative to Experiment 2:**
- Two additional instruction bullets: "Be conservative in your scoring" and "Critically evaluate weaknesses"
- New "Scoring Philosophy" section with five directives (default to skepticism, no halo effect, use the full range, score conservatively when in doubt, high scores are earned)
- Modified framing of human reviewer examples emphasizing critical evaluation tendency
- Explicit directive: "Match this level of critical evaluation. Be conservative, identify weaknesses clearly, and do not inflate scores."

---

```
[Purpose section identical to S1.1]

## Instructions
- Evaluate the application against the six criteria listed below.
- **Be conservative in your scoring** - when uncertain, score lower rather than higher
- **Critically evaluate weaknesses** - do not allow strong performance in one area
  to overshadow deficiencies in others
- Assign a numeric score as a whole integer for each criterion based on the scoring scale.
- Use the same definitions and point ranges as human reviewers.
- Provide 2–3 sentences of rationale for each score.
- Conclude with an Overall Recommendation: "Fund", "Fund with Revisions", or
  "Do Not Fund."

## Scoring Philosophy
- Default to skepticism: Proposals must provide compelling evidence to earn high scores
- No halo effect: Strong innovation does NOT compensate for weak methodology or
  unclear feasibility
- Use the full range: Do not avoid low scores when gaps are present
- When in doubt, score conservatively: Better to be stringent than lenient
- High scores are earned, not given: Scores of 27-30 should be reserved for truly
  exceptional work with compelling evidence

[Scoring Scale and Criteria sections identical to S1.1]

## Human Reviewer Scoring Examples

[Training example table identical to S1.2]

### Key Observations from This Review Panel:

Human reviewers are critical evaluators who:
- Assign low scores (14/30 or lower) when evidence is insufficient, regardless of
  other strengths
- Reject proposals with major methodological gaps even when innovation is strong
- Show natural variation in scoring (19-point spread from 61-80), demonstrating
  different evaluative perspectives
- Reserve high scores (27-30) for exceptional work, not merely good work
- Do not allow the "halo effect" - a single weakness can result in rejection
- Score conservatively when claims are not well-supported by preliminary data or
  clear plans

Critical Principle: These examples show that expert reviewers can disagree
substantially (61-80 point range) on the same proposal. However, they share a common
tendency toward critical evaluation. Note that even the highest-scoring reviewer
(SW: 80) recommended "Fund with Revisions," not unconditional funding, recognizing
methodology gaps. Three of four reviewers rejected the proposal despite acknowledging
innovation.

Your task: Match this level of critical evaluation. Be conservative, identify
weaknesses clearly, and do not inflate scores. Use these examples to understand the
full range of the scoring scale and the appropriate level of scrutiny.

[Output format section identical to S1.1]
```

---

## S2. Criterion-Level Statistical Tables

All LLM scores were aggregated by averaging three iterations within each vendor-application cell before statistical testing. Human scores are individual reviewer scores. Glass's delta uses the human group standard deviation as the reference denominator. Holm-Bonferroni correction was applied across the six criterion comparisons within each experiment. No criterion-level comparison reached statistical significance after correction in any experiment.

### Supplementary Table S1. Criterion-level comparisons for Experiment 1 (Zero-Shot).

| Criterion | Max | Human Mean ± SD (n) | LLM Mean ± SD (n) | Diff | t | p (uncorrected) | p (Holm) | Glass's Δ |
|---|---|---|---|---|---|---|---|---|
| Innovation & Impact | 30 | 25.42 ± 2.50 (12) | 26.11 ± 1.77 (9) | +0.69 | -0.708 | 0.4876 | 1.0000 | +0.277 |
| Methodology & Feasibility | 30 | 21.67 ± 7.02 (12) | 24.48 ± 2.30 (9) | +2.81 | -1.150 | 0.2643 | 1.0000 | +0.401 |
| Team Strength | 10 | 8.58 ± 1.56 (12) | 8.48 ± 0.50 (9) | -0.10 | 0.187 | 0.8535 | 1.0000 | -0.065 |
| External Funding Potential | 10 | 7.67 ± 1.61 (12) | 8.78 ± 0.55 (9) | +1.11 | -1.969 | 0.0637 | 0.3822 | +0.688 |
| Budget Clarity | 10 | 8.33 ± 1.44 (12) | 8.37 ± 1.63 (9) | +0.04 | -0.055 | 0.9565 | 1.0000 | +0.026 |
| Presentation Quality | 10 | 7.42 ± 1.56 (12) | 7.41 ± 0.76 (9) | -0.01 | 0.016 | 0.9872 | 1.0000 | -0.006 |

Note: Human n = 12 (4 reviewers × 3 applications). LLM n = 9 aggregated cell means (3 vendors × 3 applications). All three applications (FC1, FC2, FC3) included.

### Supplementary Table S2. Criterion-level comparisons for Experiment 2 (Few-Shot).

| Criterion | Max | Human Mean ± SD (n) | LLM Mean ± SD (n) | Diff | t | p (uncorrected) | p (Holm) | Glass's Δ |
|---|---|---|---|---|---|---|---|---|
| Innovation & Impact | 30 | 26.00 ± 2.20 (8) | 25.06 ± 1.83 (6) | -0.94 | 0.850 | 0.4118 | 1.0000 | -0.429 |
| Methodology & Feasibility | 30 | 23.12 ± 7.90 (8) | 23.17 ± 1.59 (6) | +0.04 | -0.013 | 0.9901 | 1.0000 | +0.005 |
| Team Strength | 10 | 8.75 ± 1.58 (8) | 8.39 ± 0.88 (6) | -0.36 | 0.501 | 0.6254 | 1.0000 | -0.228 |
| External Funding Potential | 10 | 8.38 ± 1.41 (8) | 8.44 ± 0.40 (6) | +0.07 | -0.116 | 0.9094 | 1.0000 | +0.049 |
| Budget Clarity | 10 | 8.88 ± 1.13 (8) | 7.89 ± 1.61 (6) | -0.99 | 1.351 | 0.2015 | 1.0000 | -0.876 |
| Presentation Quality | 10 | 8.00 ± 1.51 (8) | 7.61 ± 0.65 (6) | -0.39 | 0.586 | 0.5684 | 1.0000 | -0.257 |

Note: Human n = 8 (4 reviewers × 2 applications). LLM n = 6 aggregated cell means (3 vendors × 2 applications). FC3 excluded (used as training example).

### Supplementary Table S3. Criterion-level comparisons for Experiment 3 (Few-Shot + Strict).

| Criterion | Max | Human Mean ± SD (n) | LLM Mean ± SD (n) | Diff | t | p (uncorrected) | p (Holm) | Glass's Δ |
|---|---|---|---|---|---|---|---|---|
| Innovation & Impact | 30 | 26.00 ± 2.20 (8) | 23.39 ± 1.61 (6) | -2.61 | 2.443 | 0.0310 | 0.1858 | -1.185 |
| Methodology & Feasibility | 30 | 23.12 ± 7.90 (8) | 19.28 ± 2.31 (6) | -3.85 | 1.146 | 0.2741 | 0.7391 | -0.487 |
| Team Strength | 10 | 8.75 ± 1.58 (8) | 7.72 ± 1.20 (6) | -1.03 | 1.326 | 0.2094 | 0.7391 | -0.650 |
| External Funding Potential | 10 | 8.38 ± 1.41 (8) | 7.78 ± 0.81 (6) | -0.60 | 0.925 | 0.3730 | 0.7391 | -0.424 |
| Budget Clarity | 10 | 8.88 ± 1.13 (8) | 7.72 ± 1.58 (6) | -1.15 | 1.598 | 0.1360 | 0.6802 | -1.024 |
| Presentation Quality | 10 | 8.00 ± 1.51 (8) | 7.06 ± 0.71 (6) | -0.94 | 1.407 | 0.1848 | 0.7391 | -0.625 |

Note: Human n = 8 (4 reviewers × 2 applications). LLM n = 6 aggregated cell means (3 vendors × 2 applications). FC3 excluded (used as training example). Innovation & Impact showed the largest effect (Glass's Δ = -1.185) with uncorrected p = 0.031, but this did not survive Holm correction (p = 0.186).

---

## S3. Per-Vendor Criterion-Level Means

Values represent raw LLM scores (mean ± SD across iterations and applications) prior to cell-mean aggregation.

### Supplementary Table S4. Per-vendor criterion means for Experiment 1 (Zero-Shot).

| Criterion | Gemini 2.5 Flash | GPT-5 Nano | Grok 4 |
|---|---|---|---|
| Innovation & Impact | 28.00 ± 0.87 | 24.22 ± 1.20 | 26.11 ± 1.83 |
| Methodology & Feasibility | 26.00 ± 2.12 | 22.78 ± 2.99 | 24.67 ± 1.41 |
| Team Strength | 8.22 ± 0.83 | 8.33 ± 0.50 | 8.89 ± 0.33 |
| External Funding Potential | 9.22 ± 0.44 | 8.33 ± 0.71 | 8.78 ± 0.44 |
| Budget Clarity | 9.22 ± 1.09 | 6.56 ± 1.59 | 9.33 ± 1.00 |
| Presentation Quality | 7.78 ± 1.30 | 7.11 ± 0.33 | 7.33 ± 0.50 |
| **Total Score** | **88.44 ± 4.59** | **77.33 ± 2.74** | **85.11 ± 2.37** |

Note: n = 9 per vendor (3 applications × 3 iterations). All three applications included.

### Supplementary Table S5. Per-vendor criterion means for Experiment 2 (Few-Shot).

| Criterion | Gemini 2.5 Flash | GPT-5 Nano | Grok 4 |
|---|---|---|---|
| Innovation & Impact | 27.00 ± 1.26 | 23.17 ± 0.41 | 25.00 ± 0.63 |
| Methodology & Feasibility | 22.83 ± 1.47 | 22.00 ± 2.19 | 24.67 ± 1.21 |
| Team Strength | 7.67 ± 1.75 | 8.83 ± 0.41 | 8.67 ± 0.52 |
| External Funding Potential | 8.67 ± 0.52 | 8.00 ± 0.00 | 8.67 ± 0.52 |
| Budget Clarity | 8.33 ± 1.97 | 6.67 ± 1.21 | 8.67 ± 1.21 |
| Presentation Quality | 7.83 ± 1.47 | 7.33 ± 0.82 | 7.67 ± 0.82 |
| **Total Score** | **82.33 ± 6.83** | **76.00 ± 3.41** | **83.33 ± 1.21** |

Note: n = 6 per vendor (2 applications × 3 iterations). FC3 excluded.

### Supplementary Table S6. Per-vendor criterion means for Experiment 3 (Few-Shot + Strict).

| Criterion | Gemini 2.5 Flash | GPT-5 Nano | Grok 4 |
|---|---|---|---|
| Innovation & Impact | 25.33 ± 1.03 | 22.83 ± 0.98 | 22.00 ± 0.00 |
| Methodology & Feasibility | 19.17 ± 1.83 | 20.33 ± 3.33 | 18.33 ± 1.37 |
| Team Strength | 7.83 ± 1.94 | 8.20 ± 0.84 | 7.00 ± 0.00 |
| External Funding Potential | 8.67 ± 0.82 | 7.17 ± 0.41 | 7.50 ± 0.55 |
| Budget Clarity | 9.33 ± 0.82 | 6.00 ± 0.89 | 7.83 ± 1.17 |
| Presentation Quality | 7.67 ± 0.82 | 6.67 ± 0.52 | 6.83 ± 0.75 |
| **Total Score** | **78.00 ± 3.29** | **69.83 ± 5.00** | **69.50 ± 2.35** |

Note: n = 6 per vendor (2 applications × 3 iterations), except GPT-5 Nano Team Strength (n = 5 due to one missing criterion-level value). FC3 excluded. Under strict instructions, all vendors scored below the human mean (83.13), with GPT-5 Nano and Grok 4 showing the largest deviations.

---

## S4. Recommendation Distributions

### Supplementary Table S7. Funding recommendation frequencies by reviewer type and experiment.

| Experiment | Reviewer Type | Fund | Fund with Revisions | Do Not Fund | Total |
|---|---|---|---|---|---|
| Exp 1: Zero-Shot | Human | 4 (33.3%) | 3 (25.0%) | 5 (41.7%) | 12 |
| Exp 1: Zero-Shot | LLM | 13 (48.1%) | 14 (51.9%) | 0 (0.0%) | 27 |
| Exp 2: Few-Shot | Human | 4 (50.0%) | 2 (25.0%) | 2 (25.0%) | 8 |
| Exp 2: Few-Shot | LLM | 3 (16.7%) | 14 (77.8%) | 1 (5.6%) | 18 |
| Exp 3: Few-Shot + Strict | Human | 4 (50.0%) | 2 (25.0%) | 2 (25.0%) | 8 |
| Exp 3: Few-Shot + Strict | LLM | 0 (0.0%) | 13 (72.2%) | 5 (27.8%) | 18 |

Note: Experiments 2 and 3 share the same human comparison group (FC1 and FC2 only; FC3 excluded). LLMs produced zero "Do Not Fund" recommendations in the zero-shot condition and zero "Fund" recommendations under strict instructions, demonstrating strong sensitivity to prompt framing in recommendation behavior.

---

## S5. LLM API Configuration Details

### Supplementary Table S8. API configuration parameters for each LLM vendor.

| Parameter | OpenAI (GPT-5 Nano) | Google (Gemini 2.5 Flash) | xAI (Grok 4) |
|---|---|---|---|
| Model ID | gpt-5-nano-2025-08-07 | gemini-2.5-flash | grok-4-fast-reasoning |
| API version | October 2025 | October 2025 | October 2025 |
| Temperature | Default (1.0) | Default (1.0) | 0.1 |
| Max tokens | Default | Default | 4000 |
| System prompt | None | None | None |
| Iterations per combination | 3 | 3 | 3 |

Note: Temperature values for OpenAI and Google reflect the documented default at the time of data collection. The low temperature setting (0.1) for xAI Grok may contribute to reduced output variability for that vendor. No additional system prompts were used beyond the experimental prompt templates described in S1.
