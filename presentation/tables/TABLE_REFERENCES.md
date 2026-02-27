# Manuscript Table References

This document shows how to reference the generated tables in the manuscript markdown files.

## Methods Tables (2_methods.md)

### Table 1: Scoring Rubric
```markdown
![Table 1: Scoring Rubric](../presentation/tables/table1_scoring_rubric.png)
```

### Table 2: LLM Vendors and Models
```markdown
![Table 2: LLM Vendors and Models](../presentation/tables/table2_llm_vendors.png)
```

## Results Tables (3_results.md)

### Experiment 1 Tables

**Table 3: Experiment 1 - Overall Score Comparison**
```markdown
![Table 3: Experiment 1 Overall](../presentation/tables/table3_exp1_overall.png)
```

**Table 4: Experiment 1 - Criterion-Level Performance**
```markdown
![Table 4: Experiment 1 Criteria](../presentation/tables/table4_exp1_criteria.png)
```

**Table 5: Experiment 1 - Vendor Performance**
```markdown
![Table 5: Experiment 1 Vendors](../presentation/tables/table5_exp1_vendors.png)
```

### Experiment 2 Tables (Single Example)

**Table 6: Experiment 2 - Overall Scores**
```markdown
![Table 6: Experiment 2 Overall](../presentation/tables/table6_exp1_overall.png)
```

**Table 7: Experiment 2 - Criterion-Level**
```markdown
![Table 7: Experiment 2 Criteria](../presentation/tables/table7_exp1_criteria.png)
```

**Table 8: Experiment 2 - Vendor Performance**
```markdown
![Table 8: Experiment 2 Vendors](../presentation/tables/table8_exp1_vendors.png)
```

### Experiment 3 Tables (Multiple Examples)

**Table 9: Experiment 3 - Overall Scores**
```markdown
![Table 9: Experiment 3 Overall](../presentation/tables/table9_exp4_overall.png)
```

**Table 10: Experiment 3 - Criterion-Level**
```markdown
![Table 10: Experiment 3 Criteria](../presentation/tables/table10_exp4_criteria.png)
```

**Table 11: Experiment 3 - Vendor Performance**
```markdown
![Table 11: Experiment 3 Vendors](../presentation/tables/table11_exp4_vendors.png)
```

### Experiment 4 Tables (Strict Scoring)

**Table 12: Experiment 4 - Overall Scores**
```markdown
![Table 12: Experiment 4 Overall](../presentation/tables/table12_exp7_overall.png)
```

**Table 13: Experiment 4 - Criterion-Level**
```markdown
![Table 13: Experiment 4 Criteria](../presentation/tables/table13_exp7_criteria.png)
```

**Table 14: Experiment 4 - Vendor Performance**
```markdown
![Table 14: Experiment 4 Vendors](../presentation/tables/table14_exp7_vendors.png)
```

### Cross-Experiment and Aggregated Tables

**Table 15: Cross-Experiment Summary**
```markdown
![Table 15: Cross-Experiment Summary](../presentation/tables/table15_cross_experiment.png)
```

**Table 16: Overall Vendor Performance**
```markdown
![Table 16: Vendor Overall](../presentation/tables/table16_vendor_overall.png)
```

**Table 17: Aggregated Criterion-Level Performance**
```markdown
![Table 17: Criteria Aggregated](../presentation/tables/table17_criteria_aggregated.png)
```

---

## CSV Data Files

All tables are also available as CSV files for further analysis:
- `table1_scoring_rubric.csv` through `table17_criteria_aggregated.csv`

## Regenerating Tables

To regenerate all tables after data or analysis updates:

```bash
python presentation/generate_tables.py
```

This will:
1. Query the database (`data/results.db`)
2. Generate all 17 tables
3. Save as both CSV (data) and PNG (images)
4. Output to `presentation/tables/` directory
