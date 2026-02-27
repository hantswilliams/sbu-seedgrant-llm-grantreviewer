# Table Generation Update Summary

## Issue Identified

The initial table generation included all applicants (DANIEL, CHRISTINA, KELLY) in all experiments, but the manuscript describes that DANIEL should be excluded from Experiments 2-4 because DANIEL's application was used as a training example in those experiments.

## Changes Made

Updated `presentation/generate_tables.py` to exclude DANIEL from Experiments 2-4:

### Functions Updated

1. **`table_experiment_overall()`** - Lines 286-312
   - Added filtering: `exp_df = exp_df[exp_df['applicant_name'] != 'DANIEL']`
   - Applies to: with_training_data_v1, multi_examples_v1, strict_scoring_v1

2. **`table_experiment_criteria()`** - Lines 326-368
   - Added same DANIEL exclusion filter
   - Ensures criterion-level stats only use CHRISTINA and KELLY

3. **`table_experiment_vendors()`** - Lines 375-408
   - Added same DANIEL exclusion filter
   - Ensures vendor comparison only uses CHRISTINA and KELLY

4. **`table_cross_experiment_summary()`** - Lines 423-465
   - Added DANIEL exclusion for experiments 2-4
   - Ensures cross-experiment comparison is consistent

## Sample Size Changes

### Before Update (Incorrect)
- Experiment 1: 27 LLM reviews (3 applicants)
- Experiment 2: **27 LLM reviews** (should be 18)
- Experiment 3: **27 LLM reviews** (should be 18)
- Experiment 4: **27 LLM reviews** (should be 18)
- **Total: 108 LLM reviews**

### After Update (Correct)
- Experiment 1: 27 LLM reviews (DANIEL, CHRISTINA, KELLY)
- Experiment 2: **18 LLM reviews** (CHRISTINA, KELLY only)
- Experiment 3: **18 LLM reviews** (CHRISTINA, KELLY only)
- Experiment 4: **18 LLM reviews** (CHRISTINA, KELLY only)
- **Total: 81 LLM reviews used in analysis**

Note: The database still contains 108 total reviews, but 27 DANIEL reviews from experiments 2-4 are now correctly excluded from analysis.

## Verification

### Experiment 2 (Single Training Example)
```csv
Reviewer Type,Mean ± SD,Diff from Human
Human (n=12),79.08 ± 13.32,—
LLM (n=18),84.94 ± 6.19,+5.86
```
✓ Shows n=18 (correct)

### Cross-Experiment Summary
```csv
Experiment,LLM Mean,Diff from Human,p-value
Exp 1: Baseline,83.63,+4.55,0.141
Exp 2: Single Example,84.94,+5.86,0.114
Exp 3: Multiple Examples,80.56,+1.47,0.675
Exp 4: Strict Scoring,72.44,-6.64,0.067
```
✓ Statistics now match manuscript descriptions

## Database Breakdown

From `combined_reviews` table:
- **Human reviews**: 12 total (4 per applicant × 3 applicants)
- **LLM reviews per experiment**: 27 total
  - DANIEL: 9 reviews (3 vendors × 3 iterations)
  - CHRISTINA: 9 reviews (3 vendors × 3 iterations)
  - KELLY: 9 reviews (3 vendors × 3 iterations)

### Applicant Usage by Experiment
| Experiment | DANIEL | CHRISTINA | KELLY | Total Used |
|------------|--------|-----------|-------|------------|
| Exp 1: Baseline | ✓ (9) | ✓ (9) | ✓ (9) | **27** |
| Exp 2: Single Example | ✗ (excluded) | ✓ (9) | ✓ (9) | **18** |
| Exp 3: Multiple Examples | ✗ (excluded) | ✓ (9) | ✓ (9) | **18** |
| Exp 4: Strict Scoring | ✗ (excluded) | ✓ (9) | ✓ (9) | **18** |

**Rationale**: DANIEL's application and reviews were used as training examples in Experiments 2-4, so DANIEL must be excluded from those experiments to prevent data leakage.

## Files Regenerated

All 17 tables regenerated with correct filtering:
- ✓ table1_scoring_rubric.{csv,png}
- ✓ table2_llm_vendors.{csv,png}
- ✓ table3-5_exp1_*.{csv,png} (Experiment 1: 27 reviews)
- ✓ table6-8_exp1_*.{csv,png} (Experiment 2: 18 reviews) ← Updated
- ✓ table9-11_exp4_*.{csv,png} (Experiment 3: 18 reviews) ← Updated
- ✓ table12-14_exp7_*.{csv,png} (Experiment 4: 18 reviews) ← Updated
- ✓ table15_cross_experiment.{csv,png} ← Updated
- ✓ table16_vendor_overall.{csv,png}
- ✓ table17_criteria_aggregated.{csv,png}

## Impact on Results

The updated tables now correctly reflect:
1. **Proper sample sizes**: 27 for Exp 1, 18 for Exp 2-4
2. **No data leakage**: DANIEL excluded when used in training
3. **Accurate statistics**: Means, SDs, and p-values recalculated
4. **Manuscript alignment**: Tables match experimental design

## Code Documentation

Added docstrings to updated functions:
```python
def table_experiment_overall(df, exp_name, exp_num, exp_label):
    """Generate overall score table for a specific experiment.

    Experiments 2-4 exclude DANIEL (used as training example).
    """
```

This ensures future maintainers understand the filtering logic.

## Testing

Verified correct filtering:
```bash
# Check counts in database
sqlite3 data/results.db "
  SELECT prompt_experiment_name,
         COUNT(*) as Total,
         COUNT(CASE WHEN applicant_name = 'DANIEL' THEN 1 END) as DANIEL,
         COUNT(CASE WHEN applicant_name != 'DANIEL' THEN 1 END) as Others
  FROM combined_reviews
  WHERE reviewer_type = 'LLM'
  GROUP BY prompt_experiment_name;"

# Results:
# baseline_v1         | 27 | 9 | 18
# with_training_data  | 27 | 9 | 18
# multi_examples      | 27 | 9 | 18
# strict_scoring      | 27 | 9 | 18
```

✓ Filtering logic correctly excludes 9 DANIEL reviews from each of Experiments 2-4.

---

**Update completed**: 2025-10-16
**Tables regenerated**: All 17 tables
**Status**: ✅ Complete and verified
