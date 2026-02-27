# Detailed Sample Size Summary by Experiment


## Experiment 1: Zero Shot
**Baseline performance with no training examples**

*Exclusion Rule: None - all reviews included*

| Applicant | Human Count | Human Reviewers | LLM Count | LLM Breakdown |
|-----------|-------------|-----------------|-----------|---------------|
| CHRISTINA | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| KELLY | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| DANIEL | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| **TOTAL** | **12** | - | **27** | - |

## Experiment 3: Few Shot
**Multiple training examples using DANIEL data (DANIEL excluded from analysis)**

*Exclusion Rule: All reviews of DANIEL excluded (used as training data)*

| Applicant | Human Count | Human Reviewers | LLM Count | LLM Breakdown |
|-----------|-------------|-----------------|-----------|---------------|
| CHRISTINA | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| KELLY | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| DANIEL | 0 | None | 0 | Google=0, OpenAI=0, xAI=0 |
| **TOTAL** | **8** | - | **18** | - |

## Experiment 4: Stricter Prompt
**Stricter prompt with DANIEL training data (DANIEL excluded from analysis)**

*Exclusion Rule: All reviews of DANIEL excluded (used as training data)*

| Applicant | Human Count | Human Reviewers | LLM Count | LLM Breakdown |
|-----------|-------------|-----------------|-----------|---------------|
| CHRISTINA | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| KELLY | 4 | AM, HW, SW, Y | 9 | Google=3, OpenAI=3, xAI=3 |
| DANIEL | 0 | None | 0 | Google=0, OpenAI=0, xAI=0 |
| **TOTAL** | **8** | - | **18** | - |
