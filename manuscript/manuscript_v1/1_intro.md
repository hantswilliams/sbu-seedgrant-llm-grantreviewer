# Introduction

## Background

The evaluation of research grant applications is a cornerstone of academic funding systems, yet it remains a resource-intensive process that places substantial demands on expert reviewers. In the United States alone, federal agencies such as the National Institutes of Health (NIH) and National Science Foundation (NSF) process tens of thousands of grant applications annually, requiring hundreds of thousands of expert review hours.[^1][^2] This review burden is compounded by growing application volumes, limited reviewer availability, and concerns about inter-rater reliability and potential bias.[^3][^4]

Recent advances in large language models (LLMs), including GPT-4, Gemini, and Claude, have demonstrated remarkable capabilities in complex reasoning, scientific comprehension, and structured evaluation tasks.[^5][^6] These models have shown promise in various academic applications, from literature review assistance to peer review support.[^7][^8] However, their potential to augment or replace human judgment in high-stakes decision-making contexts such as grant review remains largely unexplored.

## The Promise and Challenges of AI in Peer Review

LLMs offer several theoretical advantages for grant review processes. First, unlike human reviewers who may exhibit fatigue, mood effects, or variable interpretation of rubrics, LLMs can apply evaluation criteria with mechanical consistency. Second, LLMs can process applications in seconds rather than hours, potentially enabling rapid pre-screening of large applicant pools. Third, LLMs can be calibrated to specific evaluation frameworks, reducing variability across reviewer cohorts. Finally, AI-assisted review could democratize access to expert-level feedback for under-resourced institutions or early-career researchers.

However, significant concerns remain about the reliability, validity, and ethics of AI-based evaluation systems. Prior research has documented "optimism bias" in LLMs, where models tend to generate overly positive assessments.[^9] Questions persist about whether LLMs can capture the nuanced judgment that experienced human reviewers bring to holistic evaluation. Furthermore, the reproducibility and transparency of LLM-based decisions remain open challenges given the proprietary nature of most commercial models.

## Prompt Engineering as a Critical Variable

A growing body of evidence suggests that LLM performance is highly sensitive to "prompt engineering"—the design of instructions and examples provided to guide model behavior.[^10][^11] In evaluation tasks, this includes zero-shot prompting (providing instructions without examples), few-shot prompting (including one or more demonstration examples), chain-of-thought prompting (encouraging step-by-step reasoning), and explicit calibration (providing score distributions or explicit thresholds).

Despite the recognized importance of prompt design, no prior study has systematically compared prompt engineering strategies in the context of grant review. Most existing research on AI peer review has used single prompt configurations, making it impossible to determine whether observed performance reflects inherent model capabilities or specific prompting choices.[^12][^13]

## Gap in Current Literature

While several studies have explored LLM applications in academic peer review of journal manuscripts,[^14][^15] the grant review context presents unique challenges. First, grant applications require assessment across diverse criteria including innovation, methodology, team qualifications, budget, and feasibility, unlike manuscript review which focuses primarily on scientific rigor and novelty. Second, grants require evaluation of proposed research rather than completed work, demanding assessment of potential, risk, and feasibility. Third, unlike manuscript review with its accept/reject/revise decisions, grant review involves comparative ranking and funding threshold decisions with direct financial implications. Finally, grant funding decisions impact careers, institutional resources, and research directions, warranting more rigorous validation than lower-stakes applications.

To date, no published study has compared LLM performance to human expert reviewers in grant evaluation, systematically tested multiple prompt engineering strategies in this context, or examined multiple commercial LLM vendors within the same evaluation framework with proper controls for training data contamination.

## Research Questions

This study investigates whether large language models can generate grant review scores and funding recommendations that align with human expert reviewers, and how different prompt engineering strategies affect this alignment. We address these questions through four systematic experiments:

**Experiment 1 (Zero-Shot Baseline):** Can LLMs generate grant review scores that align with human expert reviewers when provided only with evaluation instructions and scoring rubrics, without any training examples? This experiment establishes baseline LLM performance and identifies whether models exhibit systematic biases (e.g., optimism bias) in their evaluations.

**Experiment 2 (One-Shot Learning):** Does providing a single complete human review as a training example improve LLM alignment with human judgment compared to the zero-shot baseline? This experiment tests whether one concrete exemplar is sufficient to calibrate LLM scoring behavior.

**Experiment 3 (Few-Shot Learning with Distributional Information):** Does providing multiple human reviews of the same application—demonstrating natural variance in expert judgment—improve LLM calibration beyond a single example? This experiment tests whether exposure to the full range of human scoring improves LLM understanding of appropriate score distributions.

**Experiment 4 (One-Shot with Strict Calibration):** Does adding explicit instructions to apply conservative, critical standards—combined with a training example—reduce potential optimism bias and improve alignment with human reviewers? This experiment tests whether prompt-based calibration can correct for systematic scoring tendencies.

Within each experiment, we analyze: (1) overall score alignment between LLMs and humans, (2) criterion-level performance across the six evaluation dimensions (innovation, methodology, team strength, external funding potential, budget clarity, presentation quality), (3) inter-model consistency and variance across three commercial LLM vendors (OpenAI GPT-4, Google Gemini, xAI Grok), (4) funding recommendation agreement, and (5) inter-rater reliability compared to human reviewers.

To ensure methodological rigor and prevent data contamination, each experiment was analyzed with appropriate human review comparison groups. Specifically, experiments using training examples excluded human reviews that were incorporated into the LLM prompts, ensuring independent validation of LLM performance against truly held-out human assessments.

## Study Contributions

This study makes several novel contributions to the literature on AI-assisted peer review. First, it provides the first systematic comparison of prompt engineering strategies in grant review, offering empirically-grounded guidance for LLM implementation in evaluation contexts. Second, the multi-vendor evaluation (OpenAI, Google, xAI) enables assessment of whether findings generalize across commercial LLM providers rather than reflecting idiosyncrasies of a single model. Third, by analyzing both numerical scores across multiple evaluation criteria and categorical funding recommendations, the study provides comprehensive assessment of LLM performance on different dimensions of grant review. Fourth, the rigorous experimental design includes proper controls for data contamination, with experiment-specific human comparison groups ensuring that training examples do not circularly validate performance. Finally, the study develops a practical methodological framework for implementing and evaluating hybrid human-AI grant review systems in resource-constrained academic settings.

## Ethical Considerations

This research was conducted with careful attention to ethical implications. All human reviewer and applicant data were de-identified prior to analysis. Institutional Review Board (IRB) approval was obtained (Protocol: IRB2025-00534, classified as non-human subjects research). Applicant consent was obtained for LLM processing of applications, with one applicant declining and therefore being excluded from the study. No AI-generated reviews were used in actual funding decisions; all analyses were retrospective. Full transparency regarding AI involvement is maintained in all dissemination.

## Manuscript Organization

The remainder of this manuscript is organized as follows. Section 2 describes the study design, data collection procedures, experimental conditions, and statistical analysis approach. Section 3 presents findings organized by research question, including overall performance, experiment-specific analyses, and cross-experiment comparisons. Section 4 interprets findings in the context of existing literature, addresses limitations, and provides recommendations for practice and future research.

---

[^1]: NIH Data Book. (2023). Success Rates. https://report.nih.gov/nihdatabook/category/17
[^2]: NSF. (2023). Proposal and Award Policies and Procedures Guide. National Science Foundation.
[^3]: Marsh, H. W., Jayasinghe, U. W., & Bond, N. W. (2008). Improving the peer-review process for grant applications: Reliability, validity, bias, and generalizability. *American Psychologist*, 63(3), 160-168.
[^4]: Pier, E. L., et al. (2018). Low agreement among reviewers evaluating the same NIH grant applications. *PNAS*, 115(12), 2952-2957.
[^5]: OpenAI. (2024). GPT-4 Technical Report. arXiv:2303.08774.
[^6]: Google DeepMind. (2024). Gemini: A Family of Highly Capable Multimodal Models. arXiv:2312.11805.
[^7]: Liang, W., et al. (2024). Can Large Language Models Provide Useful Feedback on Research Papers? arXiv:2310.01783.
[^8]: Hosseini, M., & Horbach, S. P. J. M. (2023). Fighting reviewer fatigue or amplifying bias? *Research Integrity and Peer Review*, 8, 4.
[^9]: Zheng, C., et al. (2024). Bias and Fairness in Large Language Models: A Survey. arXiv:2309.00770.
[^10]: Wei, J., et al. (2022). Chain-of-Thought Prompting Elicits Reasoning in Large Language Models. *NeurIPS*.
[^11]: Brown, T. B., et al. (2020). Language Models are Few-Shot Learners. *NeurIPS*.
[^12]: Bai, Y., et al. (2024). Large Language Models for Scientific Peer Review. arXiv:2402.12857.
[^13]: D'Amour, A., et al. (2024). On the Opportunities and Risks of Foundation Models for NLP in Peer Review. *ACL*.
[^14]: Liang, W., et al. (2023). Monitoring AI-Modified Content at Scale. arXiv:2302.07234.
[^15]: Hosseini, M., et al. (2024). The future of peer review in the age of generative AI. *Scientometrics*, 129, 1-15.
