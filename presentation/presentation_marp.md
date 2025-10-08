---
marp: true
theme: default
paginate: true
footer: 'Can LLMs Replace Human Grant Reviewers? | SBU School of Health Professions'
style: |
  section {
    font-size: 24px;
  }
  h1 {
    color: #990000;
    font-size: 48px;
  }
  h2 {
    color: #990000;
    font-size: 36px;
  }
  table {
    font-size: 20px;
  }
  img[alt~="center"] {
    display: block;
    margin: 0 auto;
  }
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Can LLMs Replace Human Grant Reviewers?
## A Comparative Study of Prompt Engineering Strategies

**Research Team:** Hants Williams, Jack Lamberg, and Eric Lamberg
**Institution:** Stony Brook University School of Health Professions
**Date:** October 14, 2025
**Funding:** SBU Seed Grant Program

---

## Background & Motivation

### The Challenge of Grant Review
- Grant review is time-intensive and resource-demanding
- Requires expertise across multiple evaluation criteria
- Inter-rater reliability varies among human reviewers
- Growing interest in AI-assisted academic workflows

### Research Question:
**Can Large Language Models (LLMs) provide reliable grant reviews comparable to human experts?**

![w:800 center](./slide2_problem_statement.png)

---

## Study Design

### Dataset:
- **4 grant applications** originally submitted to SBU School of Health Professions Research Seed Grant Program
- **1 applicant excluded** - withdrew consent for LLM processing (remote or local)
- **Final dataset: 3 grant applications** analyzed
- 4 human reviewers per application (12 total human reviews)
- Multiple LLM models tested (OpenAI GPT, Google Gemini, xAI Grok)

### IRB Status: 
IRB2025-00534 - Exempt, Non-Human Subjects Research (Stony Brook University)

---

## Study Design (continued)


### Evaluation Criteria (100 points total):
1. Innovation & Impact (30 pts)
2. Methodological Approach & Feasibility (30 pts)
3. Research Team Strength (10 pts)
4. External Funding Potential (10 pts)
5. Budget Clarity (10 pts)
6. Presentation Quality (10 pts)

---

## Study Design (continued)

![w:700 center](./slide3_study_design.png)

---

## Prompt Engineering Experiments

### Four Experimental Conditions:

1. **baseline_v1** - Standard instructions without examples
2. **with_training_data_v1** - Single training example (1 complete human review)
3. **multi_examples_v1** - Multiple training examples (4 human reviews showing score variance)
4. **strict_scoring_v1** - Emphasis on conservative/critical evaluation

**Important:** Experiments using training data exclude that applicant from analysis to prevent data leakage

---

## Prompt Engineering Experiments (continued)

![w:950 center](./slide4_experiment_conditions.png)

---

## Human vs. LLM Performance Overview

### Overall Score Comparison:
- **Human reviewers** (n=12): 79.08 ± 13.32 points
  - Range: 61-99 points
  - Median (IQR): 78.5 (24.5)

- **LLM reviewers** (n=108): 79.56 ± 7.14 points
  - Range: 62-97 points
  - Median (IQR): 79.0 (10.0)

---

## Human vs. LLM Performance Overview (continued)

### Key Findings:
- **No significant difference in overall scores (t=-0.196, p=0.845)**
- Difference: +0.47 points (Cohen's d = 0.04, small effect)
- **LLMs show lower variability (SD: 7.14 vs 13.32)**
- Strong rank-order agreement (Spearman ρ=1.0, p<0.001)

---

## Human vs. LLM Performance (continued)

![w:900 center](./slide5_human_vs_llm_overall.png)

---

## Performance by Evaluation Criteria

| Criterion | Human % | LLM % | Difference | p-value |
|-----------|---------|-------|------------|---------|
| **Innovation & Impact** | 84.7% | 83.5% | -0.37 pts | ns |
| **Methodology** | 72.2% | 75.4% | **+0.96 pts** | ns |
| **Team Strength** | 85.8% | 83.1% | -0.27 pts | ns |
| **External Funding** | 76.7% | 83.5% | **+0.69 pts** | **p=0.022** |
| **Budget Clarity** | 83.3% | 80.7% | -0.26 pts | ns |
| **Presentation** | 74.2% | 72.2% | -0.19 pts | ns |

### Key Insights:
- Minimal differences across most criteria
- **LLMs score significantly higher on External Funding potential (p=0.022)**
- LLMs also score higher on Methodology (+0.96 pts, ns)
- No evidence of systematic "LLM optimism" - scores closely match humans

---

## Performance by Criteria (continued)

![w:800 center](./slide6_criteria_comparison.png)

---

## Impact of Prompt Engineering

| Experiment | Mean ± SD | Diff from Human | n |
|------------|-----------|-----------------|---|
| **Baseline** (no examples) | 83.63 ± 5.75 | +4.55 pts | 27 |
| **Single Example** | 84.94 ± 6.19 | +5.86 pts | 18 |
| **Multiple Examples (4)** | **80.56 ± 5.36** | **+1.47 pts** | 18 |
| **Strict Instructions** | 72.44 ± 5.34 | -6.64 pts | 18 |

### Key Findings:
- Experiments differ significantly (F=18.44, p<0.001)
- **Multiple examples achieved best alignment with humans (1.47 pt difference)**
- Strict instructions led to under-scoring (-6.64 pts)
- More examples > single example for calibration

**Answer:** Yes - training examples (especially multiple) improve LLM-human alignment

---

## Prompt Engineering Impact (continued)

![w:900 center](./slide7_experiment_comparison.png)

---

## Model-Specific Performance

### Vendor Comparison (n=48 each):

| Rank | Vendor | Mean ± SD | Diff from Human | n |
|------|--------|-----------|-----------------|---|
| **1** | **xAI (Grok)** | 79.72 ± 6.54 | **+0.64 pts** | 36 |
| 2 | OpenAI (GPT) | 75.44 ± 4.98 | -3.64 pts | 36 |
| 3 | Google (Gemini) | 83.50 ± 7.41 | +4.42 pts | 36 |

### Key Insights:
- **xAI Grok shows best alignment with human reviewers (0.64 pt difference)**
- Google Gemini tends to score higher than humans (+4.42 pts)
- OpenAI GPT scores more conservatively (-3.64 pts)
- All models maintain reasonable consistency (SD: 4.98-7.41)

**Implication:** Model choice matters - xAI Grok most suitable for this application

---

## Model Performance (continued)

![w:900 center](./slide8_model_comparison.png)

---

## Inter-Rater Reliability & Agreement

### Consistency Analysis:

**Variability (Average SD across applicants):**
- Human reviewers: 11.37 points; LLM reviewers: 6.94 points
- **LLMs are 39% more consistent than humans**

**Human-LLM Score Agreement:**
- Pearson correlation: r = 0.90 (p=0.283); Spearman correlation: ρ = 1.00 (p<0.001)
- **Perfect rank-order agreement on applicant scoring**

**Recommendation Agreement:**
- LLMs prefer "Fund with Revisions" (61%) vs Human split (42% Do Not Fund, 33% Fund, 25% Revisions)
- **LLMs more optimistic about revision potential**

---

## Inter-Rater Reliability (continued)

**Critical Finding:** Strong numerical agreement doesn't guarantee decision alignment

![w:900 center](./slide9_agreement_analysis.png)

*Note: Applicants anonymized as S1-S3 to maintain blinding*

---

## Conclusions & Implications

### Key Takeaways:

1. **LLMs can match human scoring accuracy** (no significant difference, r=0.91)
   - But more conservative in recommendations

2. **Prompt engineering significantly impacts performance**
   - Multiple training examples optimal for calibration
   - Strict instructions led to under-scoring

---

## Conclusions & Implications (continued)

3. **Model selection matters**
   - xAI Grok showed best human alignment
   - 5-point spread between best and worst models

4. **LLMs offer advantages in consistency**
   - 39% lower variability than humans
   - Reduced inter-rater reliability concerns

---

## Conclusions & Implications (continued)

### Practical Implications:

✅ **Where LLMs Can Help:**
- Initial screening and ranking
- Generating detailed feedback
- Calibration/norming exercises
- Reducing reviewer burden

❌ **Where Humans Remain Essential:**
- Final funding decisions
- Nuanced judgment calls
- Handling edge cases
- Accountability and transparency

---

## Recommended Approach:
Hybrid system with LLM pre-screening + human final decisions

---

## Future Directions & Acknowledgments

### Next Steps for Research:
1. **Expand sample size** - Test across multiple grant programs and cycles
2. **Hybrid system testing** - Evaluate LLM pre-screen + human review workflows
3. **Longitudinal validation** - Track prediction accuracy for funded projects
4. **Bias analysis** - Assess for demographic or institutional biases
5. **Qualitative analysis** - Compare rationale quality and feedback utility

### Broader Implications:
- Potential for democratizing access to expert review
- Reducing time-to-decision in grant administration
- Standardization of evaluation criteria
- Cost reduction for funding agencies

---

<!-- _class: lead -->

## Thank You!

### Acknowledgments:
- SBU School of Health Professions 
- Human reviewers who participated in this study

### Contact & Code:
- **Email:** [hants.williams@stonybrook.edu]



---

<!-- _class: lead -->
<!-- _paginate: false -->

# Supplementary Slides

---

## S1: Detailed Methodology

### Database Schema:
- Combined reviews table with human and LLM data
- Experiment tracking with prompt versions
- Criteria-level scoring breakdown

---

## S1: Detailed Methodology (continued)

### LLM API Configurations:
- OpenAI: GPT-5-nano (default)
- Google: Gemini 2.5 Flash
- xAI: Grok-4-fast-reasoning

### Statistical Analysis Methods:
- Two-sample t-tests for group comparisons
- Pearson and Spearman correlations
- One-way ANOVA for experiment comparison
- Effect sizes (Cohen's d) reported

---

## S2: Example Review Comparison

### Human Review Excerpt (Applicant S1):
*"The proposal addresses an important gap in physical therapy education regarding Lyme disease differential diagnosis. The methodology is sound but lacks detail on sampling strategy. Budget is well-justified. Recommend funding with minor revisions to strengthen the timeline section."*

### LLM Review Excerpt (Same Applicant):
*"This proposal demonstrates strong innovation in addressing Lyme disease education gaps for physical therapists. The methodological approach shows promise, though the convenience sampling limits generalizability. Budget allocation is appropriate and clearly justified. The absence of a detailed timeline is a significant weakness. Recommendation: Fund with Revisions to address timeline and sampling concerns."*

### Similarity: Both identify timeline weakness; LLM more detailed
### Difference: Human more concise; LLM more structured

---

## S3: Limitations

### Sample Size:
- Limited to 3 grant applications (originally 4)
- Single institution and program
- May not generalize to other grant types or disciplines

### Generalizability:
- Seed grants may differ from larger federal grants (NIH, NSF)
- Health professions context may not extend to other fields
- English-only applications

---

## S3: Limitations (continued)


### Technical Limitations:
- API costs and access restrictions
- Token limits for very long proposals
- Model versions subject to change

### Design Limitations:
- No real-time feedback incorporation
- Human reviewers not calibrated using training examples
- Recommendation categories may be institution-specific

---

## S4: Ethical Considerations

### Data Privacy & Anonymization:
- All applicant data de-identified in public presentations
- Grant applications stored securely
- IRB approval obtained (not human subject research)

### Bias Detection & Mitigation:
- No demographic information provided to LLMs
- Multiple models tested to identify vendor-specific biases
- Training examples selected to represent score range diversity

---

## S4: Ethical Considerations (continued)

### Transparency:
- Full prompt disclosure in supplementary materials
- Reproducible methodology with open-source code
- Clear communication of limitations to stakeholders

### Implementation Guidelines:
- Recommend human oversight for final decisions
- Regular auditing of LLM outputs
- Explicit disclosure to applicants if LLMs used in review
