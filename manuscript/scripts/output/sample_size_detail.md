# Detailed Sample Size Summary by Experiment


## Experiment 1: Zero Shot
**Baseline performance with no training examples**

*Exclusion Rule: None - all human reviews included*

| Applicant | Human Count | Human Reviewers | LLM Count | LLM Breakdown |
|-----------|-------------|-----------------|-----------|---------------|
| CHRISTINA | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| KELLY | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| DANIEL | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| **TOTAL** | **12** | - | **27** | - |

## Experiment 2: One Shot
**Single training example added**

*Exclusion Rule: HW's review of DANIEL excluded (used as training data)*

| Applicant | Human Count | Human Reviewers | LLM Count | LLM Breakdown |
|-----------|-------------|-----------------|-----------|---------------|
| CHRISTINA | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| KELLY | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| DANIEL | 3 | AM, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| **TOTAL** | **11** | - | **27** | - |

## Experiment 3: Few Shot
**Multiple training examples with variance**

*Exclusion Rule: All human reviews of DANIEL excluded (used as training data)*

| Applicant | Human Count | Human Reviewers | LLM Count | LLM Breakdown |
|-----------|-------------|-----------------|-----------|---------------|
| CHRISTINA | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| KELLY | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| DANIEL | 0 | None | 9 | Google=3, OpenAI=3, xAI=3 |
| **TOTAL** | **8** | - | **27** | - |

## Experiment 4: Stricter Prompt
**Stricter prompt with one shot example**

*Exclusion Rule: HW's review of DANIEL excluded (used as training data)*

| Applicant | Human Count | Human Reviewers | LLM Count | LLM Breakdown |
|-----------|-------------|-----------------|-----------|---------------|
| CHRISTINA | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| KELLY | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| DANIEL | 3 | AM, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| **TOTAL** | **11** | - | **27** | - |
