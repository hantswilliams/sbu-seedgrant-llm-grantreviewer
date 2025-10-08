# Can LLMs Replace Human Grant Reviewers?
## A Comparative Study of Prompt Engineering Strategies

---

## Slide 1: Title Slide
**Can LLMs Replace Human Grant Reviewers? A Comparative Study of Prompt Engineering Strategies**

- Research Team: [Your Names]
- Institution: Stony Brook University School of Health Professions
- Date: [Presentation Date]
- Funding: SBU Seed Grant Program

---

## Slide 2: Background & Motivation

**The Challenge of Grant Review**
- Grant review is time-intensive and resource-demanding
- Requires expertise across multiple evaluation criteria
- Inter-rater reliability varies among human reviewers
- Growing interest in AI-assisted academic workflows

**Research Question:**
Can Large Language Models (LLMs) provide reliable grant reviews comparable to human experts?

**Key Visual:**

![Grant Review Challenges](./slide2_problem_statement.png)

---

## Slide 3: Study Design

**Dataset:**
- 4 grant applications from SBU School of Health Professions Research Seed Grant Program
- 4 human reviewers per application (16 total human reviews)
- Multiple LLM models tested (OpenAI GPT, Google Gemini, xAI Grok, Anthropic Claude)

**Evaluation Criteria (100 points total):**
1. Innovation & Impact (30 pts)
2. Methodological Approach & Feasibility (30 pts)
3. Research Team Strength (10 pts)
4. External Funding Potential (10 pts)
5. Budget Clarity (10 pts)
6. Presentation Quality (10 pts)

**Key Visual:**

![Study Design Overview](./slide3_study_design.png)

---

## Slide 4: Prompt Engineering Experiments

**Four Experimental Conditions:**

1. **baseline_v1** - Standard instructions without examples
2. **with_training_data_v1** - Single training example (1 complete human review)
3. **multi_examples_v1** - Multiple training examples (4 human reviews showing score variance)
4. **strict_scoring_v1** - Emphasis on conservative/critical evaluation

**Important:** Experiments using training data exclude that applicant from analysis to prevent data leakage

**Key Visual:**

![Experiment Conditions](./slide4_experiment_conditions.png)

---

## Slide 5: Human vs. LLM Performance Overview

**Overall Score Comparison:**
- **Human reviewers** (n=16): 80.81 ± 12.55 points
  - Range: 61-99 points
  - Median (IQR): 80.5 (16.0)

- **LLM reviewers** (n=144): 79.81 ± 7.34 points
  - Range: 62-97 points
  - Median (IQR): 79.0 (12.0)

**Key Findings:**
- **No significant difference** in overall scores (t=0.476, p=0.635)
- Difference: -1.00 points (Cohen's d = -0.10, small effect)
- **LLMs show lower variability** (SD: 7.34 vs 12.55)
- Strong rank-order agreement (Spearman ρ=1.0, p<0.001)

**Key Visual:**

![Human vs. LLM Overall Scores](./slide5_human_vs_llm_overall.png)

---

## Slide 6: Performance by Evaluation Criteria

**Criterion-Level Analysis:**

| Criterion | Human % | LLM % | Difference | p-value |
|-----------|---------|-------|------------|---------|
| **Innovation & Impact** | 87.1% | 84.7% | -0.73 pts | ns |
| **Methodology** | 75.4% | 75.0% | -0.11 pts | ns |
| **Team Strength** | 84.4% | 85.2% | +0.09 pts | ns |
| **External Funding** | 79.4% | 84.4% | **+0.51 pts** | **p=0.035** |
| **Budget Clarity** | 80.6% | 77.4% | -0.33 pts | ns |
| **Presentation** | 76.2% | 72.6% | -0.37 pts | ns |

**Key Insights:**
- Minimal differences across most criteria
- **LLMs score significantly higher on External Funding potential** (p=0.035)
- No evidence of systematic "LLM optimism" - scores closely match humans

**Key Visual:**

![Performance by Criteria](./slide6_criteria_comparison.png)

---

## Slide 7: Impact of Prompt Engineering

**Experiment Performance Comparison:**

| Experiment | Mean ± SD | Diff from Human | n |
|------------|-----------|-----------------|---|
| **Baseline** (no examples) | 84.50 ± 5.88 | +3.69 pts | 36 |
| **Single Example** | 84.37 ± 6.39 | +3.56 pts | 27 |
| **Multiple Examples (4)** | **80.37 ± 5.60** | **-0.44 pts** | 27 |
| **Strict Instructions** | 72.30 ± 4.79 | -8.52 pts | 27 |

**Key Findings:**
- Experiments differ significantly (F=28.55, p<0.001)
- **Multiple examples achieved best alignment** with humans (0.44 pt difference)
- Strict instructions led to under-scoring (-8.52 pts)
- More examples > single example for calibration

**Answer:** Yes - training examples (especially multiple) improve LLM-human alignment

**Key Visual:**

![Experiment Comparison](./slide7_experiment_comparison.png)

---

## Slide 8: Model-Specific Performance

**Vendor Comparison (n=48 each):**

| Rank | Vendor | Mean ± SD | Diff from Human |
|------|--------|-----------|-----------------|
| **1** | **xAI (Grok)** | 80.71 ± 7.10 | **-0.10 pts** |
| 2 | Google (Gemini) | 83.19 ± 7.63 | +2.38 pts |
| 3 | OpenAI (GPT) | 75.54 ± 4.92 | -5.27 pts |

**Key Insights:**
- **xAI Grok shows best alignment** with human reviewers (0.10 pt difference)
- Google Gemini tends to score slightly higher than humans
- OpenAI GPT scores more conservatively
- All models maintain reasonable consistency (SD: 4.92-7.63)

**Implication:** Model choice matters - xAI Grok most suitable for this application

**Key Visual:**

![Model Comparison](./slide8_model_comparison.png)

---

## Slide 9: Inter-Rater Reliability & Agreement

**Consistency Analysis:**

**Variability (Average SD across applicants):**
- Human reviewers: 10.88 points
- LLM reviewers: 7.19 points
- **LLMs are 34% more consistent than humans**

**Human-LLM Score Agreement:**
- Pearson correlation: r = 0.91 (p=0.089)
- Spearman correlation: ρ = 1.00 (p<0.001)
- **Perfect rank-order agreement** on applicant scoring

**BUT: Recommendation Agreement:**
- **0% agreement on funding decisions**
- LLMs prefer "Fund with Revisions" (58%) vs Human split (37% Fund, 37% Do Not Fund)
- LLMs more optimistic about revision potential

**Critical Finding:** Strong numerical agreement doesn't guarantee decision alignment

**Key Visual:**

![Agreement Analysis](./slide9_agreement_analysis.png)

*Note: Applicants anonymized as S1-S4 to maintain blinding*

---

## Slide 10: Conclusions & Implications

**Key Takeaways:**

1. **LLMs can match human scoring accuracy** (no significant difference, r=0.91)
   - But more conservative in recommendations

2. **Prompt engineering significantly impacts performance**
   - Multiple training examples optimal for calibration
   - Strict instructions led to under-scoring

3. **Model selection matters**
   - xAI Grok showed best human alignment
   - 5-point spread between best and worst models

4. **LLMs offer advantages in consistency**
   - 34% lower variability than humans
   - Reduced inter-rater reliability concerns

**Critical Limitation:**
- **Perfect score correlation ≠ decision agreement (0% recommendation alignment)**
- Threshold effects and qualitative judgment still require human oversight

**Practical Implications:**

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

**Recommended Approach:** Hybrid system with LLM pre-screening + human final decisions

---

## Slide 11: Future Directions & Acknowledgments

**Next Steps for Research:**
1. **Expand sample size** - Test across multiple grant programs and cycles
2. **Hybrid system testing** - Evaluate LLM pre-screen + human review workflows
3. **Longitudinal validation** - Track prediction accuracy for funded projects
4. **Bias analysis** - Assess for demographic or institutional biases
5. **Qualitative analysis** - Compare rationale quality and feedback utility

**Broader Implications:**
- Potential for democratizing access to expert review
- Reducing time-to-decision in grant administration
- Standardization of evaluation criteria
- Cost reduction for funding agencies

**Acknowledgments:**
- SBU School of Health Professions Research Seed Grant Program
- Human reviewers who participated in this study
- [Funding sources]
- [Collaborators]

**Contact & Code:**
- GitHub: [github.com/your-repo]
- Email: [your.email@institution.edu]

---

## Supplementary Slides (If Needed)

### S1: Detailed Methodology
- Database schema
- LLM API configurations
- Statistical analysis methods

### S2: Example Reviews
- Side-by-side comparison of human vs. LLM review
- Highlighting similarities and differences in rationales

### S3: Limitations
- Sample size constraints
- Generalizability concerns
- Technical limitations

### S4: Ethical Considerations
- Data privacy and anonymization
- Bias detection and mitigation strategies
- Transparency in AI-assisted review
