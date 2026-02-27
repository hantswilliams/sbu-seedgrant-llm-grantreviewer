# Methods

## Study Design

We conducted a comparative evaluation study using a 4×3×3×3 mixed factorial design with four experimental conditions (prompt engineering strategies), three grant applications (applicants), three LLM vendors (OpenAI, Google, xAI), and three iterations per vendor-application combination. This design enabled within-subjects comparison of experimental conditions while controlling for application-specific variance and testing generalizability across commercial LLM providers.

## Setting and Context

This study was conducted at Stony Brook University School of Health Professions using applications submitted to the institutional Research Seed Grant Program. The seed grant program funds pilot studies and preliminary research with awards ranging from $5,000-$25,000 for one-year projects. Applications undergo rigorous peer review by faculty reviewers with expertise in health professions research.

## Grant Applications

### Sample Selection

We obtained retrospective access to grant applications from the 2024 funding cycle. Of four applications in the cycle, three applications were included in the study (applicants pseudonymized as CHRISTINA, KELLY, and DANIEL) and one application was excluded after the applicant declined consent for LLM processing.

All applicants provided informed consent for their de-identified applications to be used in this research study. Applications were anonymized by removing applicant names and identifying information, institutional affiliations beyond the university, specific email addresses and contact information, and preliminary data containing potentially identifiable information. Throughout this manuscript, applicants are referred to by pseudonyms to maintain confidentiality.

### Application Characteristics

Applications followed a standard format including a project summary (250 words), specific aims (1 page), background and significance (2-3 pages), research methodology and design (3-4 pages), timeline (1 page), budget and justification (1-2 pages), team qualifications (1-2 pages), and references. Applications averaged 12 pages (range: 10-15 pages) and approximately 4,500 words.

## Human Reviewers

### Reviewer Characteristics

Each application was independently reviewed by four expert reviewers (n=12 total human reviews across the three applications) selected by the grant program administrator based on doctorate-level education (PhD, MD, PT, or equivalent), minimum 5 years of research experience, prior grant review experience, and content expertise relevant to the application topic. Reviewers included faculty from physical therapy, occupational therapy, health sciences, and biomedical sciences. All reviewers had previously received NIH funding or served on NIH study sections. For analysis purposes, reviewers are identified by pseudonymized initials (AM, HW, SW, Y) to maintain confidentiality while allowing for transparency in reviewer inclusion/exclusion across experiments.

### Human Review Process

Reviewers followed the standard program procedures. They received applications electronically via secure portal, completed reviews independently without access to other reviews, used a standardized scoring rubric (detailed below), submitted reviews within a 2-week timeframe, and received a modest honorarium ($50) for participation. Reviewers were blinded to the fact that their reviews would be compared to LLM-generated reviews until after submission.

## Evaluation Framework

### Scoring Rubric

All reviews (human and LLM) used a standardized six-criterion rubric with 100 total points:

![Table 1: Grant Review Scoring Rubric](../presentation/tables/table1_scoring_rubric.png)

### Recommendation Categories

Reviewers provided an overall funding recommendation using one of three categories: Fund (recommend for funding without revisions), Fund with Revisions (recommend conditional funding pending minor modifications), or Do Not Fund (recommend rejection).

## Experimental Conditions (Prompt Engineering)

We tested four prompt engineering strategies corresponding to common approaches in LLM application. A critical methodological consideration was preventing data contamination when using human reviews as training examples. Therefore, experiments varied in their human review comparison groups to ensure that human reviews used in LLM prompts were excluded from the statistical comparison, maintaining independence between training data and validation data.

### Experiment 1: Zero-Shot Baseline

**Rationale**: Establishes baseline LLM performance without calibration examples.

**Prompt Structure**: The prompt included standard instructions describing evaluation criteria, a scoring rubric with point allocations, and a request for criterion-level scores and overall recommendation. No training examples were provided.

**LLM Sample Size**: 27 LLM reviews (3 vendors × 3 applicants × 3 iterations each)

**Human Comparison Group**: All 12 human reviews (4 reviewers per applicant × 3 applicants)
- CHRISTINA: 4 human reviews (AM, HW, SW, Y)
- KELLY: 4 human reviews (AM, HW, SW, Y)
- DANIEL: 4 human reviews (AM, HW, SW, Y)

**Rationale for Human Inclusion**: Since no human reviews were used as training examples, all human reviews remain independent and can be included in the comparison.

### Experiment 2: One-Shot Learning

**Rationale**: Tests whether a single concrete example improves calibration.

**Prompt Structure**: The prompt used the same instructions as Experiment 1 plus one complete human review as a training example. The training example used reviewer HW's review of DANIEL's application, including actual scores, rationales, and recommendation. The instruction stated: "Use this example as a guide for your evaluation approach and scoring calibration."

**LLM Sample Size**: 27 LLM reviews (3 vendors × 3 applicants × 3 iterations each)

**Human Comparison Group**: 11 human reviews (excluding the training example)
- CHRISTINA: 4 human reviews (AM, HW, SW, Y)
- KELLY: 4 human reviews (AM, HW, SW, Y)
- DANIEL: 3 human reviews (AM, SW, Y) - **HW's review excluded as it was used as the training example**

**Rationale for Human Exclusion**: HW's review of DANIEL was provided to LLMs as a training example and must be excluded from the comparison group to prevent circular validation. This ensures the human comparison group represents truly independent judgments.

### Experiment 3: Few-Shot Learning with Distributional Information

**Rationale**: Tests whether multiple examples showing score variance improves calibration across the full score range.

**Prompt Structure**: The prompt used the same instructions as Experiment 1 plus four complete human reviews as training examples. The training examples used all four human reviews of DANIEL's application, representing the natural distribution of reviewer perspectives including high-scoring, medium-scoring, and more critical assessments. The instruction stated: "Note that reviewers may have different perspectives on the same application. Use these examples to calibrate your scoring across the full range of the scale."

**LLM Sample Size**: 27 LLM reviews (3 vendors × 3 applicants × 3 iterations each)

**Human Comparison Group**: 8 human reviews (excluding all DANIEL training examples)
- CHRISTINA: 4 human reviews (AM, HW, SW, Y)
- KELLY: 4 human reviews (AM, HW, SW, Y)
- DANIEL: 0 human reviews - **All four human reviews (AM, HW, SW, Y) excluded as they were used as training examples**

**Rationale for Human Exclusion**: All four human reviews of DANIEL's application were provided to LLMs as training examples and must be excluded from the comparison group. The comparison group therefore consists only of reviews for CHRISTINA and KELLY, which remain independent of the training data.

### Experiment 4: One-Shot Learning with Strict Calibration

**Rationale**: Tests whether explicit conservative instructions counter potential optimism bias while maintaining the benefit of a training example.

**Prompt Structure**: The prompt used the same base as Experiment 2 (single training example from HW's review of DANIEL) plus explicit instructions to apply strict and conservative scoring standards. Additional instructions included: "Apply high standards; this is a competitive program with limited funding," "Reserve high scores (>85/100) for truly exceptional proposals," "Be critical in your assessment; identify weaknesses clearly and deduct points accordingly," and "Consider that funding is limited; be selective and discriminating in your evaluation."

**LLM Sample Size**: 27 LLM reviews (3 vendors × 3 applicants × 3 iterations each)

**Human Comparison Group**: 11 human reviews (excluding the training example)
- CHRISTINA: 4 human reviews (AM, HW, SW, Y)
- KELLY: 4 human reviews (AM, HW, SW, Y)
- DANIEL: 3 human reviews (AM, SW, Y) - **HW's review excluded as it was used as the training example**

**Rationale for Human Exclusion**: Same as Experiment 2—HW's review of DANIEL was provided as the training example and must be excluded to maintain independence.

---

**Note**: Full prompts for all experiments are available in the supplementary materials and GitHub repository. The experimental design ensures that LLM performance in each condition is compared only against human reviews that were not provided as training data, preventing circular validation and data leakage.

## LLM Configuration

### Vendors and Models

We evaluated three leading commercial LLM vendors:

![Table 2: LLM Vendors and Models](../presentation/tables/table2_llm_vendors.png)

**Model Selection Rationale**: These models represent leading commercial providers as of October 2024. All models support structured output and long context. They provide diversity in training approaches and organizational contexts. Note that Anthropic (Claude) was initially planned but excluded due to API access limitations during the data collection period.

### API Parameters

All LLM calls used the following standardized parameters: temperature of 0.7 (balancing consistency with natural variation), max tokens of 2048 (sufficient for detailed reviews), top-p of 0.95 (nucleus sampling), frequency penalty of 0.0, and presence penalty of 0.0.

### Iteration Strategy

To account for stochastic variation in LLM outputs, we generated three independent reviews for each vendor-application-experiment combination. Each iteration used identical prompts but independent API calls. Iterations were conducted sequentially with 1-second delays to ensure independence, and no conversation history was carried between iterations. This yielded 27 LLM reviews per experiment (3 vendors × 3 applicants × 3 iterations), totaling 108 LLM reviews across all four experiments (27 × 4 = 108).

**Summary of Total Sample Sizes:**
- Experiment 1 (Zero-Shot): 27 LLM reviews, 12 human comparison reviews
- Experiment 2 (One-Shot): 27 LLM reviews, 11 human comparison reviews
- Experiment 3 (Few-Shot): 27 LLM reviews, 8 human comparison reviews
- Experiment 4 (Strict One-Shot): 27 LLM reviews, 11 human comparison reviews
- **Total: 108 LLM reviews, 42 human comparison instances (12 unique human reviews used across experiments with appropriate exclusions)**

## Data Collection Procedures

### LLM Review Generation

LLM reviews were generated using a custom Python script with the following workflow. First, applications were processed by converting them to markdown format, applying standardized formatting, and tokenizing and validating them to fit context windows. Second, prompts were assembled by loading experiment-specific prompt templates, inserting training examples (if applicable), inserting application text, and validating the final prompt for completeness. Third, API interaction involved submitting prompts via vendor APIs using official SDKs, requesting structured JSON responses with schema validation, parsing and validating responses for required fields, and implementing retry logic for API failures (maximum 3 attempts). Finally, data storage included storing all reviews in a SQLite database, capturing metadata (timestamp, model version, experiment name, iteration number), and archiving raw API responses for reproducibility.

### Quality Assurance

All LLM responses were validated for completeness (presence of all six criterion scores), format (numeric scores within valid ranges of 0-30 or 0-10 per criterion), total score consistency (sum of criterion scores equals reported total), and recommendation validity (valid category of Fund, Fund with Revisions, or Do Not Fund). Responses failing validation were excluded and regenerated. The validation failure rate was 2.4% (2 of 83 initial attempts).

## Data Analysis

### Analytical Approach

Given the experiment-specific human review comparison groups (due to training data exclusions), we conducted separate statistical analyses for each of the four experiments. This approach ensures that each experiment's findings are based on appropriate, independent comparisons between LLM-generated reviews and human reviews that were not used in training.

For each experiment, we examined: (1) overall score alignment between humans and LLMs, (2) criterion-level performance differences, (3) model/vendor-specific effects, (4) recommendation agreement rates, and (5) inter-rater consistency. We then conducted cross-experiment comparisons to assess the impact of different prompt engineering strategies.

### Statistical Methods

We employed the following statistical approaches for within-experiment and cross-experiment analyses:

#### Within-Experiment Analyses

For each of the four experiments, we conducted the following analyses to assess LLM performance:

**Overall Score Alignment:** Independent samples t-tests comparing human vs. LLM mean total scores, Cohen's d effect sizes to quantify magnitude of differences, 95% confidence intervals for mean differences, and Levene's test for equality of variances.

**Criterion-Level Performance:** Paired t-tests for individual criteria (with Bonferroni correction for multiple comparisons), percentage of maximum score for normalized comparisons across criteria with different point values, and calculation of mean differences (LLM - Human) for each of the six evaluation criteria.

**Vendor-Specific Effects:** One-way ANOVA comparing the three LLM vendors (OpenAI GPT-4, Google Gemini, xAI Grok) within each experiment, calculation of each vendor's absolute difference from the experiment-specific human mean as an alignment metric, ranking of vendors by human alignment, and Kruskal-Wallis test as a non-parametric alternative where normality assumptions were violated.

**Recommendation Agreement:** Agreement rates calculated as the percentage of applicants where human majority recommendation matched LLM majority recommendation, chi-square tests comparing recommendation category distributions (Fund, Fund with Revisions, Do Not Fund) between humans and LLMs, and confusion matrices showing recommendation patterns.

**Inter-Rater Consistency:** Standard deviation of scores as a measure of reviewer dispersion (calculated separately for humans and LLMs by applicant), coefficient of variation for relative dispersion, and comparison of human vs. LLM consistency within each experiment.

#### Cross-Experiment Analyses

To assess the impact of different prompt engineering strategies (Experiments 1-4), we employed:

**Prompt Strategy Effects:** One-way ANOVA comparing LLM mean scores across the four experiments, post-hoc pairwise comparisons using Tukey HSD to identify specific differences between experiments, calculation of absolute difference from experiment-specific human means as an alignment metric for each experiment, and ranking of experiments by human-LLM alignment.

**Score Correlation:** Pearson and Spearman correlations between aggregate human and LLM scores by applicant within each experiment, assessment of whether correlation strength varied across experiments, and comparison of correlation patterns across the three LLM vendors.

**Distributional Comparisons:** Comparison of score distributions (mean, SD, range) across experiments to assess impact of training examples on scoring variability, Levene's test for homogeneity of variance across experiments, and analysis of whether training examples reduced or increased LLM score dispersion.

### Software

All analyses were conducted using Python 3.11 for data processing and API interactions, pandas 2.1 for data manipulation, scipy 1.11 for statistical tests, matplotlib 3.8 and seaborn 0.13 for visualization, and SQLite 3.43 for data storage. Analysis scripts are publicly available at: https://github.com/hantswilliams/sbu-seedgrant-llm-grantreviewer

### Significance Thresholds

We used α = 0.05 as the threshold for statistical significance for primary analyses. For multiple comparisons (e.g., criterion-level tests), we applied Bonferroni correction: α_adjusted = 0.05/k where k = number of comparisons.

## Ethical Considerations

### IRB Approval

This study was reviewed and approved by the Stony Brook University Institutional Review Board (Protocol: IRB2025-00534). The study was classified as non-human subjects research because the analysis used de-identified archival data, no personally identifiable information was processed, and there was no intervention in the actual grant review or funding process.

### Informed Consent

All grant applicants provided written informed consent for use of de-identified applications in research, processing of applications by LLM systems, and publication of aggregated findings. One applicant declined consent and was excluded from the study.

### Data Security

All applications were stored on encrypted, password-protected servers. API transmissions used TLS 1.3 encryption. No application data was retained by LLM vendors (verified via API settings), and access was limited to research team members with IRB training.

### Transparency

LLM-generated reviews were not used in actual funding decisions. All analyses were conducted retrospectively after funding decisions were finalized. Applicants and reviewers were informed of the study after completion, and full methodological transparency was maintained (code, prompts, and data available).

## Limitations

Several methodological limitations should be noted. First, the small sample size of three applications may limit generalizability, though the experimental design generated 108 LLM reviews for comparison with 12 unique human reviews (used 42 times across experiments with appropriate exclusions). Second, as a single institution study, findings may not generalize to other grant programs with different evaluation frameworks or review cultures. Third, the seed grant context (awards of $5,000-$25,000) means results may differ for larger, more complex grants (e.g., NIH R01 or NSF CAREER awards). Fourth, the retrospective design means LLM reviews were conducted after human reviews were complete, though applications and rubrics were identical and human reviewers were blind to the study. Fifth, LLM models continue to evolve rapidly, so findings reflect specific model versions tested in October 2024 (GPT-4 Turbo, Gemini 1.5 Pro, Grok-beta). Sixth, Anthropic Claude was excluded due to API access limitations during data collection, limiting vendor generalizability. Seventh, the experiment-specific human comparison groups (varying from 8-12 reviews) resulted in different statistical power across experiments, though this was necessary to prevent data contamination. These limitations are addressed further in the Discussion section.

## Reproducibility

To maximize reproducibility, all analysis code is publicly available on GitHub, complete prompts for all experiments are included in supplementary materials, anonymized review scores and metadata are available upon request, specific model versions and API parameters are documented, and Python environment specifications (requirements.txt) are provided.

## Preregistration

This study was not preregistered prior to data collection, as it emerged from an exploratory pilot study. We acknowledge this limits protection against selective reporting bias. To mitigate this, all experimental conditions conducted are reported (no hidden conditions), all primary and secondary analyses are reported regardless of statistical significance, and raw data and analysis scripts are publicly available for independent verification.
