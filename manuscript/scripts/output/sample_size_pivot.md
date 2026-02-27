# Sample Size Pivot Table

| Experiment    |   Total Reviews |   Human Reviews |   LLM Reviews |   CHRISTINA (Human) |   KELLY (Human) |   DANIEL (Human) |   CHRISTINA (LLM) |   KELLY (LLM) |   DANIEL (LLM) |
|:--------------|----------------:|----------------:|--------------:|--------------------:|----------------:|-----------------:|------------------:|--------------:|---------------:|
| Exp1_ZeroShot |              39 |              12 |            27 |                   4 |               4 |                4 |                 9 |             9 |              9 |
| Exp2_OneShot  |              38 |              11 |            27 |                   4 |               4 |                3 |                 9 |             9 |              9 |
| Exp3_FewShot  |              35 |               8 |            27 |                   4 |               4 |                0 |                 9 |             9 |              9 |
| Exp4_Stricter |              38 |              11 |            27 |                   4 |               4 |                3 |                 9 |             9 |              9 |

## Notes:
- Exp1 (baseline_v1): All human reviews included
- Exp2 (with_training_data_v1): HW's review of DANIEL excluded
- Exp3 (multi_examples_v1): All DANIEL human reviews excluded
- Exp4 (strict_scoring_v1): HW's review of DANIEL excluded
