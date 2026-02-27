# Applicant Pseudonym Mapping

**CONFIDENTIAL - Do not include in submission or public repository.**

This file maps the de-identified applicant codes used in the manuscript to the original pseudonyms used in the internal database and analysis scripts.

| Manuscript Code | Internal Pseudonym | Notes |
|---|---|---|
| FC1 | CHRISTINA | Faculty Candidate 1 |
| FC2 | KELLY | Faculty Candidate 2 |
| FC3 | DANIEL | Faculty Candidate 3; used as training data source in Experiments 2–3 |

## Context

- The internal database (`data/results.db`) and analysis scripts (`generate_analyses_v2.py`) use the original pseudonyms (CHRISTINA, KELLY, DANIEL).
- The manuscript uses FC1, FC2, FC3 for an additional layer of de-identification.
- FC3 (DANIEL) was randomly selected as the training data applicant; all FC3 human and LLM reviews are excluded from Experiments 2 and 3 comparisons.
