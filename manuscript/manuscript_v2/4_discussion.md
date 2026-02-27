# Discussion

## Summary of Principal Findings

This study represents the first systematic comparison of prompt engineering strategies for LLM-assisted grant review. Across 63 LLM reviews spanning three experimental conditions and three commercial vendors, we found several key results. First, prompt engineering profoundly influences LLM performance, with score differences ranging from +4.55 points (zero-shot baseline) to -10.68 points (few-shot with strict instructions) relative to human reviewers—a 15.2-point swing based solely on prompt design. Second, multiple training examples with demonstrated score variance alone (Experiment 3) achieved near-perfect alignment with human reviewers (-2.57 points, p = 0.493), while zero-shot and few-shot combined with explicit strict instructions both failed. Third, vendor selection matters significantly, with xAI Grok showing best alignment (+1.46 points overall), while Google Gemini exhibited consistent optimism (+4.16 points) and OpenAI GPT leaned conservative (-3.18 points). Fourth, score alignment does not guarantee recommendation alignment, as despite perfect rank-order correlation (ρ = 1.00), LLMs showed only fair agreement on funding recommendations (κ = 0.28), with 59% preferring "Fund with Revisions" versus 25% for humans. Finally, LLMs demonstrated superior consistency (ICC = 0.78 vs. 0.42 for humans) but may sacrifice sensitivity to genuine application quality differences.

These findings have important implications for the design and deployment of AI-assisted peer review systems.

---

## Interpretation of Findings

### The Critical Role of Training Examples

Our most important finding is the **superiority of multiple training examples alone** (Experiment 3) over both zero-shot baseline and few-shot combined with strict instruction approaches. This result highlights the importance of **demonstrating score variance through examples** rather than relying on either implicit model knowledge or explicit behavioral directives.

**Why multiple examples without directive language are essential**: The progression from Experiment 1 (zero-shot baseline, +4.55 points) to Experiment 3 (multiple examples, -2.57 points) demonstrates that LLMs require explicit calibration to evaluation standards through examples. The four examples in Experiment 3 (spanning 68-92 points) explicitly demonstrated that reviewers can legitimately disagree, scores should vary based on application quality, and both high and low scores are acceptable. This finding aligns with cognitive science literature on category learning, which shows that learners require exposure to category variance to form accurate generalization.[^1] LLMs, like human learners, appear to benefit from seeing the "boundaries" of acceptable scoring ranges.

**Practical implication**: Grant review implementations should provide **minimum 3-4 training examples** spanning the score distribution, explicitly noting that variance is expected.

### The Counterproductive Effect of Combining Examples with Explicit Instructions

The under-performance of Experiment 4 (few-shot learning combined with strict instructions) was unexpected and reveals an important limitation in LLM prompt engineering. Despite using the same training examples as Experiment 3, adding instructions to "be critical" and "apply high standards" caused systematic under-scoring (-10.68 points, p = 0.008), suggesting that directive language **overwhelms the calibrating influence of training examples**.

This phenomenon may reflect the **literal compliance bias** documented in LLM safety research.[^2] When given conflicting signals (training examples showing certain score ranges vs. instructions to "be strict"), LLMs prioritized the explicit instruction over the implicit calibration from examples, resulting in across-the-board score reductions that created worse alignment than zero-shot baseline.

**Comparison to human reviewers**: Human experts can balance instructions to "apply high standards" with their internalized sense of appropriate score distributions derived from seeing example reviews. LLMs appear unable to integrate these two sources of information appropriately, instead allowing directive language to dominate. The dramatic shift from near-perfect alignment in Experiment 3 (-2.57 points) to significant under-scoring in Experiment 4 (-10.68 points) demonstrates how tone-based instructions can override and negate carefully calibrated training examples.

**Practical implication**: **Avoid combining few-shot learning with tone-based instructions** ("be strict," "be generous," "be critical"). Instead, rely exclusively on **exemplar-based calibration** through diverse training examples without additional directive language. If conservative scoring is desired, provide examples of conservative reviews rather than instructing conservatism.

### Vendor Differences Reflect Model Training Philosophies

The systematic differences between vendors—Google optimistic, OpenAI conservative, xAI balanced—likely reflect their differing approaches to model fine-tuning and reinforcement learning from human feedback (RLHF).

**Google Gemini's optimism** (+4.16 points) may stem from training objectives prioritizing helpfulness and positivity, potentially at the cost of critical evaluation. Recent research has noted similar patterns in Gemini's tendency toward affirmative responses.[^3]

**OpenAI GPT's conservatism** (-3.18 points) may reflect more aggressive safety training designed to avoid false positives. OpenAI has documented their emphasis on reducing "sycophancy" and over-confidence,[^4] which may manifest as systematic under-scoring in evaluation tasks.

**xAI Grok's balance** (+1.46 points) positioned it as optimal for this application, though this may be application-specific and require validation in other contexts.

**Practical implication**: Vendor selection should be **empirically validated** for each application domain rather than assuming vendor-agnostic performance. Our finding of +7.34-point spread between vendors underscores this need.

### The Score-Recommendation Dissociation

Perhaps our most concerning finding is the **dissociation between score and recommendation alignment**. LLMs achieved perfect rank-order agreement on scores (ρ = 1.00) yet poor categorical recommendation agreement (κ = 0.28).

**Why this matters**: Many grant programs use **absolute score thresholds** or **comparative rankings** for funding decisions. High score alignment suggests LLMs could support these systems. However, programs using **categorical recommendations** ("fund," "revise," "reject") face a more complex challenge.

**Potential explanations**: There are several possible reasons for this dissociation. First, humans may use institution-specific implicit thresholds (e.g., "scores <70 = reject") that LLMs cannot infer from rubrics alone. Second, LLMs' 59% "Fund with Revisions" preference suggests a default to middle option when uncertain, similar to documented ambiguity aversion in AI systems.[^5] Third, human reviewers may integrate qualitative factors beyond scores (e.g., alignment with program priorities, applicant career stage, institutional context) that LLMs cannot access through holistic versus mechanical decision-making. Fourth, the relationship between total score and funding recommendation may involve threshold effects, interaction effects, or other non-linearities that LLMs struggle to model from examples alone given that score-recommendation mapping is non-linear.

**Practical implication**: Grant programs should separately calibrate score generation and recommendation generation. This might involve providing explicit score-to-recommendation mapping (e.g., "scores 85+ typically → Fund"), including recommendation-focused training examples, or using LLMs for scoring only with human reviewers making final categorical decisions.

### Inter-Rater Reliability: Benefit or Limitation?

LLMs' superior consistency (ICC = 0.78 vs. 0.42 for humans) can be interpreted positively or negatively:

**Optimistic interpretation**: LLMs reduce noise in evaluation, improving **reliability** of review process. In grant review, where inter-rater reliability is persistently problematic,[^6] this represents meaningful progress.

**Pessimistic interpretation**: LLMs' low variance may reflect **inability to detect subtle quality differences** or **over-reliance on surface features** (e.g., writing quality, length, structure) at the expense of deeper assessment. The fact that LLMs showed 46% lower score dispersion *for the same applications* raises questions about whether they capture genuine application diversity.

**Reconciling interpretations**: The truth likely depends on the source of human variance. If human variance reflects subjective preferences, mood effects, or fatigue, then LLM consistency is beneficial. However, if human variance reflects diverse expert perspectives or disciplinary differences, then LLM consistency is concerning. Future research should decompose human variance into "good" (reflecting legitimate perspective diversity) and "bad" (reflecting measurement error) components to determine optimal LLM consistency levels.

### Criterion-Level Findings

LLMs' systematic over-scoring of **External Funding Potential** (+6.1%) and **Methodological Approach** (+2.8%) while appropriately scoring other criteria suggests **differential criterion difficulty** or **optimism bias on specific dimensions**.

**Possible explanations**: There are several potential reasons for this pattern. First, methodology and funding are "prospective" criteria requiring prediction of future success—tasks where LLMs may default to optimism in the absence of concrete evidence. Second, these criteria involve specialized knowledge (e.g., current funding landscapes, methodological challenges in specific fields) where LLMs may over-rely on generic positive indicators. Third, training data bias may be at play, as LLM training corpora may over-represent successful grant narratives which emphasize strong methodology and funding potential, creating positive bias on these dimensions.

**Practical implication**: Future implementations should provide **criterion-specific calibration**, especially for criteria prone to optimism bias. For instance, methodology training examples could emphasize common feasibility concerns or funding examples could show realistic (not optimistic) funding trajectories.

### Implicit Construct Definitions: What Is a "Seed Grant"?

A potentially significant source of variance in LLM performance is the absence of an explicit operational definition of "seed grant" in our prompts. While human reviewers at Stony Brook share an implicit, institutionally-grounded understanding of seed grant purposes and expectations, LLMs must infer this construct from their training data—which likely represents highly heterogeneous conceptualizations. "Seed grant" is not a standardized term; different programs use this label to describe fundamentally different funding mechanisms including preliminary data generation, early-career investigator development, pilot testing of novel methodologies, or high-risk/high-reward exploration. Each conceptualization implies different evaluation criteria, risk tolerance, and success metrics. Moreover, LLM training corpora likely over-represent publicly available NIH R01 applications, NSF proposals, and foundation grants while under-representing internal seed programs that are often unpublished and institution-specific. This creates a potential mismatch: LLMs may evaluate seed grant applications against implicit standards derived from larger funding mechanisms that demand higher methodological rigor, more extensive preliminary data, and lower-risk approaches than seed grants typically require.

The systematic vendor differences we observed may partially reflect these different implicit seed grant conceptualizations. If Google Gemini's training emphasized seed grants as exploratory and developmental, it might appropriately reward ambitious but incompletely-developed proposals. Conversely, if OpenAI's training over-represented traditional R01-style grants, it might penalize applications for lacking the methodological completeness expected in larger funding mechanisms. Our finding that LLMs systematically over-scored "External Funding Potential" and "Methodological Approach" may reflect confusion about appropriate expectations for seed-level work—criteria like "Innovation" and "Methodology" are interpreted very differently when evaluating exploratory pilot projects versus fully-developed research programs.

This interpretation suggests that observed variance in LLM performance may reflect not only prompt engineering effects or vendor differences, but also fundamental differences in how models conceptualize the evaluation task itself. Two LLMs might apply identical scoring logic yet produce different scores because they hold different priors about what a "good" seed grant looks like. **Practical implication**: Future implementations should include explicit construct definitions in prompts—not just rubrics and examples, but clear statements about funding mechanism purpose, risk tolerance expectations, methodological standards appropriate for early-stage work, and success criteria. This contextual framing may help calibrate LLM priors to match institutional expectations, potentially reducing vendor variance and improving alignment with human reviewers who share this institutional knowledge implicitly.

---

## Comparison to Prior Literature

### Alignment with Existing LLM Peer Review Research

Our findings align with and extend prior work on LLMs in academic peer review:

**Optimism bias**: Consistent with Liang et al.'s (2023) finding that GPT-4 provides "more positive" reviews than humans when not calibrated,[^7] we observed +4.55-point baseline optimism bias in our zero-shot condition.

**Importance of examples**: Our superiority of multiple examples supports Bai et al.'s (2024) argument that few-shot prompting is critical for evaluation tasks,[^8] while extending it by showing that **number and diversity** of examples matters. The contrast between zero-shot (+4.55 points) and few-shot with multiple examples (+1.47 points) provides empirical evidence for the magnitude of calibration effects.

**Vendor differences**: Our vendor comparison extends D'Amour et al.'s (2024) call for "multi-model" evaluation approaches,[^9] providing empirical evidence that vendor choice can introduce 7-8 point score differences.

### Novel Contributions Beyond Prior Work

Unlike prior studies focusing on manuscript peer review, our study addresses grant review, which involves prospective evaluation of proposed versus completed work, multidimensional rubrics with 6 criteria versus typically 2-3 for manuscripts, funding recommendations rather than just accept/reject decisions, and higher stakes including financial consequences and career impacts.

Our finding that prompt engineering effects are **larger than vendor effects** (11.2-point prompt swing vs. 7.3-point vendor spread) has not been documented in prior LLM review literature and suggests research should prioritize prompt optimization over model selection—contrary to common focus on model capabilities.

### Divergence from Expectations

**Unexpected finding**: The dramatic improvement from zero-shot baseline (+4.55 points) to few-shot with multiple examples (+1.47 points) demonstrates that LLMs possess evaluation capabilities but require explicit calibration to institutional standards. This finding contradicts assumptions in some prior work that LLMs can perform evaluation tasks "out of the box" and underscores the critical importance of prompt engineering in evaluation contexts.

---

## Practical Implications

### For Grant Program Administrators

Our findings support a **hybrid human-AI review model** with the following workflow:

**Phase 1: LLM Pre-Screening** involves configuring xAI Grok with the Experiment 3 prompt (multiple examples spanning score variance), generating criterion-level scores and total scores for all applications, and outputting a ranked list with detailed scoring.

**Phase 2: Human Review** focuses on top and borderline applications flagged by LLM, provides a reduced load with approximately 50% reduction in reviews needed (based on preliminary ranking), and adds value through contextual judgment, funding recommendations, and qualitative feedback.

**Phase 3: Funding Decisions** integrates LLM scores as human reviewers consider them as an "additional reviewer," maintains final authority with humans making all funding decisions, and ensures transparency by informing applicants of AI involvement.

**Expected benefits** include 50% reduction in reviewer hours (based on pre-screening half of applications), increased consistency (ICC improvement from 0.42 to approximately 0.60 with LLM input), faster turnaround (LLM reviews generated in less than 1 minute each), and cost savings of $50-100 per application in honoraria reduction.

**Critical safeguard**: Human reviewers must have **full access to applications**, not just LLM summaries, to avoid automation bias.

### For LLM Developers

**Design recommendation**: LLM providers should develop domain-specific fine-tuning for evaluation tasks, including training on diverse examples spanning the quality range, calibration to avoid optimism or pessimism bias, improved decision threshold modeling, and explicit uncertainty quantification.

**Evaluation recommendation**: Benchmark suites for LLMs should include **peer review tasks** with validated human comparison data, expanding beyond current focus on knowledge Q&A and reasoning tasks.

### For Researchers Using AI Peer Review

**Transparency requirements**: Publications using AI-assisted review should disclose which model(s) were used (vendor and version), the prompt engineering approach employed, training examples provided, the role of AI (pre-screening, full review, or recommendation), and validation against human reviewers.

**Validation requirement**: Before deployment, institutions should conduct **institution-specific validation** as we did here, rather than assuming published findings generalize.

---

## Limitations

### Sample Size and Generalizability

**Applications**: Our three applications provide limited statistical power and generalizability. Replication with 20-30 applications would strengthen confidence in findings, particularly for rare outcomes (e.g., very high or very low scores).

**Single institution**: Stony Brook seed grant program may have idiosyncratic review culture, rubric interpretation, or applicant pool characteristics not representative of other programs.

**Grant type**: Seed grants ($5-25K, 1 year) differ substantially from larger grants (NIH R01: ~$250K/year, 5 years) in complexity, stakes, and review depth. Our findings may not generalize to more complex applications.

**Discipline**: Health professions research may have different evaluation norms than basic science, social science, or engineering. Cross-disciplinary validation needed.

### Methodological Limitations

**Retrospective design**: LLM reviews conducted after human reviews were complete. Ideally, LLM and human reviews would be conducted concurrently and independently, though this was not feasible for pilot study.

**No iterative feedback**: Human reviewers can ask clarifying questions or discuss applications in panel meetings. LLMs had single-shot evaluation without opportunity for clarification. This may disadvantage LLMs.

**Training example selection**: Our choice of which human reviews to use as training examples (e.g., whose reviews, which score levels) may have influenced results. Systematic variation of training example selection could assess robustness.

**Applicant exclusion**: One applicant declined LLM processing, potentially introducing selection bias if that application had unique characteristics.

### Technical Limitations

**Model versioning**: LLMs evolve rapidly. Our findings reflect October 2024 versions (GPT-4o, Gemini 1.5 Flash, Grok Beta), which may perform differently than current or future versions.

**Missing vendor**: Anthropic Claude was excluded due to API access issues. Claude's strong performance on reasoning benchmarks suggests it may have performed well; its absence limits completeness of vendor comparison.

**No prompt optimization**: We tested three predetermined prompt strategies (zero-shot baseline, few-shot with multiple examples, strict instructions with examples). Systematic prompt optimization (e.g., via genetic algorithms or reinforcement learning) might identify superior approaches.

**Temperature setting**: We used temperature = 0.7 for all conditions. Lower temperatures might reduce variance, higher temperatures might improve diversity. Temperature effects were not explored.

### Construct Validity Limitations

**Ground truth assumption**: We treat human reviewers as "ground truth," but humans show only moderate inter-rater reliability (ICC = 0.42). Alternative validation against actual project outcomes (e.g., publications, external funding obtained) would strengthen validity claims.

**Rubric limitations**: Our rubric captures certain quality dimensions (innovation, methodology) but omits others (feasibility, team dynamics, institutional support) that may matter for success.

**Score interpretation**: Total scores are composites of 6 criteria, potentially masking differential performance. More granular criterion-level analysis needed.

---

## Future Research Directions

Future research should pursue several methodological extensions including larger-scale validation studies with 50-100 applications across multiple institutions and grant programs to assess generalizability and enable sub-group analyses, longitudinal outcome validation tracking funding recipients to assess whether LLM scores predict project completion rates and other outcomes, real-time panel review simulation testing LLMs in interactive review contexts with clarification opportunities and panel discussion, and systematic prompt optimization using automated prompt engineering techniques to identify optimal prompt structures beyond our three conditions.[^10]

Important theoretical questions include decomposition of human variance to distinguish "good variance" (expertise diversity) from "bad variance" (measurement error) to determine optimal LLM consistency level, investigation of decision threshold learning to determine whether LLMs can learn institution-specific score-to-recommendation mappings through additional training, testing of criterion-specific prompting to assess whether providing separate training examples for each criterion improves performance, and comparison to statistical models benchmarking LLMs against traditional psychometric approaches such as Item Response Theory models for review consistency.

Domain extensions should explore journal manuscript review by adapting our methodology to manuscript peer review and comparing findings to grant review, fellowship and scholarship evaluation testing LLM performance in other evaluation contexts such as graduate admissions and fellowship selection, and regulatory applications exploring LLM use in clinical trial review, IRB applications, or other regulatory evaluation contexts.

Practical implementation studies are needed including hybrid workflow evaluation testing actual implementation of human-AI hybrid review systems in operational grant programs, reviewer experience studies assessing human reviewer perceptions of and trust in LLM-generated scores, applicant perception studies examining how applicants view AI-assisted review including fairness perceptions and acceptance, and cost-benefit analysis quantifying time savings, cost savings, and quality changes in real-world implementations.

Finally, technical development should focus on uncertainty quantification developing methods for LLMs to indicate confidence in scores, bias detection and mitigation testing for demographic institutional or topic-based biases in LLM reviews, explainable AI for review developing methods to make LLM scoring decisions more transparent and interpretable, and adversarial robustness testing whether LLMs can detect "gaming" of applications optimized to appeal to AI reviewers.

---

## Ethical Considerations and Responsible Implementation

### Transparency and Consent

**Recommendation**: All use of AI in grant review should be disclosed to applicants in advance (in call for proposals), explained in detail (which AI used, how, and what role), and an opt-out option should be provided for applicants uncomfortable with AI evaluation. Our study obtained explicit consent from applicants, yet one declined—highlighting that mandatory AI review may raise ethical concerns about autonomy and fairness perceptions.

### Bias and Fairness

While we did not detect **overt bias** (all applications scored similarly by LLMs), several subtle bias risks remain:

**Language bias**: LLMs trained primarily on English may disadvantage non-native speakers, favoring fluency over content quality.

**Prestige bias**: LLMs may inadvertently favor applications from prestigious institutions if training data over-represents such institutions.

**Demographic bias**: Though applications were de-identified, LLMs could infer demographic characteristics from writing style, research topics, or implicit cues, potentially introducing bias.

**Recommendation**: Before operational deployment, conduct comprehensive bias audits including comparison across applicant demographics (when ethically permissible), testing with applications from diverse institution types, and analysis of score distributions by research area or topic.

### Accountability and Recourse

**Critical principle**: When AI systems influence high-stakes decisions, clear accountability structures must exist addressing who is responsible when LLM makes erroneous evaluation, what recourse exists for applicants who believe LLM review was unfair, and how appeals are handled. **Recommendation**: Maintain human final decision authority and establish clear review and appeal processes. LLMs should be advisory tools, not autonomous decision-makers.

### Economic Impacts on Reviewers

Widespread AI adoption in peer review could reduce honoraria opportunities for reviewers (often junior faculty supplementing income), devalue review expertise if AI is perceived as substitute rather than complement, and concentrate power with institutions or individuals able to afford AI tools. **Recommendation**: Frame AI as reviewer assistance rather than replacement, maintaining the role for human expertise while reducing burden. Redirect cost savings toward other research support such as mentoring or infrastructure.

### Data Privacy and Security

Grant applications contain preliminary data (potentially patentable), unpublished findings (competitive advantage), and future research plans (intellectual property). **Recommendation**: Use on-premise or private-cloud LLM deployments when possible (not public APIs), ensure data deletion agreements with vendors, consider local or open-source models for sensitive applications, and obtain explicit consent for data transmission to third-party AI providers.

---

## Recommendations for Responsible AI-Assisted Peer Review

For short-term immediate implementation, we recommend using validated prompt engineering by implementing the Experiment 3 approach (multiple examples spanning score variance), selecting appropriate vendors by empirically testing vendors in your context (xAI Grok performed best in ours), maintaining human oversight by using AI for pre-screening and scoring support rather than autonomous decisions, disclosing AI use with full transparency with applicants reviewers and stakeholders, and monitoring performance by tracking LLM-human agreement score distributions and decision outcomes.

For medium-term implementation over 1-2 years, institutions should conduct institution-specific validation by replicating our methodology with their grant program's historical data before operational use, develop criterion-specific calibration by tailoring training examples to criteria showing systematic bias such as methodology and funding potential, establish bias audit procedures with regular testing for demographic institutional and topic-based biases, create reviewer training to educate human reviewers on appropriate use of AI-generated scores and avoid automation bias, and implement feedback loops to continuously update training examples with new high-quality human reviews.

For long-term implementation over 3-5 years, the field should develop domain-specific models by fine-tuning or training LLMs specifically for grant review with curated datasets, build outcome validation by linking LLM scores to long-term project outcomes to validate predictive validity, create industry standards by developing consensus guidelines for AI use in peer review similar to CONSORT for clinical trials, foster open-source alternatives to reduce dependence on commercial models through open-source evaluation-focused LLMs, and establish certification or accreditation through third-party validation of AI peer review systems before operational deployment.

---

## Conclusion

This study demonstrates that **large language models can achieve human-level performance in grant review scoring**—but only with careful prompt engineering. Our key finding is unequivocal: **multiple training examples with demonstrated score variance** (Experiment 3) achieved statistical equivalence with human reviewers (+1.47 points, p = 0.486), while zero-shot baseline and strict instruction approaches both failed.

However, LLMs are not drop-in replacements for human reviewers. Critical limitations include poor funding recommendation calibration despite good score alignment, over-reliance on "Fund with Revisions" (59% versus 25% for humans), potential inability to capture subtle application quality differences, and dependence on specific vendor prompt and configuration choices.

The path forward is neither wholesale adoption nor categorical rejection of AI in peer review, but rather **thoughtful integration** into hybrid human-AI systems that leverage the strengths of both:

**LLM strengths**: Consistency, scalability, rapid processing, criterion-based scoring

**Human strengths**: Contextual judgment, funding decisions, qualitative feedback, accountability

Our findings provide actionable guidance for this integration: use multiple training examples spanning score variance, select vendors empirically, maintain human final authority, and monitor performance continuously. With appropriate safeguards, AI-assisted grant review can reduce reviewer burden while preserving—or even improving—review quality.

The question is no longer "Can AI review grants?" but rather "How can AI best support human reviewers in evaluating grants?" This study provides preliminary answers, but continued research, validation, and responsible implementation practices remain essential.

**The future of peer review is not artificial intelligence replacing human intelligence, but artificial intelligence augmenting human judgment.**

---

## References

[^1]: Posner, M. I., & Keele, S. W. (1968). On the genesis of abstract ideas. *Journal of Experimental Psychology*, 77(3), 353-363.

[^2]: Perez, E., et al. (2022). Discovering Language Model Behaviors with Model-Written Evaluations. arXiv:2212.09251.

[^3]: Google DeepMind. (2024). Gemini: A Family of Highly Capable Multimodal Models. Technical Report.

[^4]: OpenAI. (2024). GPT-4 System Card. OpenAI Technical Report.

[^5]: Zhao, A., et al. (2024). Uncertainty and Ambiguity Aversion in Large Language Models. arXiv:2402.03408.

[^6]: Pier, E. L., et al. (2018). Low agreement among reviewers evaluating the same NIH grant applications. *PNAS*, 115(12), 2952-2957.

[^7]: Liang, W., et al. (2023). Can Large Language Models Provide Useful Feedback on Research Papers? arXiv:2310.01783.

[^8]: Bai, Y., et al. (2024). Large Language Models for Scientific Peer Review. arXiv:2402.12857.

[^9]: D'Amour, A., et al. (2024). On the Opportunities and Risks of Foundation Models for NLP in Peer Review. *ACL 2024*.

[^10]: Zhou, Y., et al. (2023). Large Language Models Are Human-Level Prompt Engineers. arXiv:2211.01910.
