# Sample Size Pivot Table

| Experiment    |   Total Reviews |   Human Reviews |   LLM Reviews |   CHRISTINA (Human) |   KELLY (Human) |   DANIEL (Human) |   CHRISTINA (LLM) |   KELLY (LLM) |   DANIEL (LLM) |
|:--------------|----------------:|----------------:|--------------:|--------------------:|----------------:|-----------------:|------------------:|--------------:|---------------:|
| Exp1_ZeroShot |              39 |              12 |            27 |                   4 |               4 |                4 |                 9 |             9 |              9 |
| Exp3_FewShot  |              26 |               8 |            18 |                   4 |               4 |                0 |                 9 |             9 |              0 |
| Exp4_Stricter |              26 |               8 |            18 |                   4 |               4 |                0 |                 9 |             9 |              0 |

## Notes:
- Exp1 (baseline_v1): All reviews included (12 human + 27 LLM)
- Exp3 (multi_examples_v1): DANIEL completely excluded - used as training (8 human + 18 LLM)
- Exp4 (strict_scoring_v1): DANIEL completely excluded - used as training (8 human + 18 LLM)
