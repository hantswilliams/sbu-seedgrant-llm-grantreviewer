# Table Generation Fix Summary

## Issues Identified and Resolved

### Issue 1: Missing Vendor Data (Tables 5, 8, 11, 14, 16)

**Problem**: Vendor tables showed no data because model names in database didn't match search terms.

**Database contained**:
- `gemini-2.5-flash` (not `gemini`)
- `gpt-5-nano` (not `gpt-4o`)
- `grok-4-fast-reasoning` (not `grok`)

**Fix**: Updated all vendor search arrays to use correct model names:

```python
# Before
vendors = ['grok', 'gemini', 'gpt-4o']

# After
vendors = ['grok-4-fast-reasoning', 'gemini-2.5-flash', 'gpt-5-nano']
```

**Functions updated**:
- `table_exp1_vendors()` - Line 253
- `table_experiment_vendors()` - Line 393
- `table_vendor_overall()` - Line 473

### Issue 2: Missing Human Data (Tables 3, 4, 5)

**Problem**: Human reviews don't have `prompt_experiment_name` values in database (NULL/empty), so filtering by experiment excluded them.

**Root cause**:
```python
exp1_df = df[df['prompt_experiment_name'] == 'baseline_v1']
human_scores = exp1_df[exp1_df['reviewer_type'] == 'Human']  # Returns empty!
```

**Fix**: Get human reviews separately from main dataframe (not filtered by experiment):

```python
# Human reviews don't have experiment_name, so get them separately
human_scores = df[df['reviewer_type'] == 'Human']['total_score'].dropna()
```

**Functions updated**:
- `table_exp1_overall()` - Line 168
- `table_exp1_criteria()` - Line 217
- `table_exp1_vendors()` - Line 251

## Verification Results

### Table 3 (Exp 1 Overall) ✅
```csv
Reviewer Type,Mean ± SD,Median,Range
Human (n=12),79.08 ± 13.32,78.50,61-99
LLM (n=27),83.63 ± 5.75,84.00,74-94
```
✓ Human data present
✓ LLM data present

### Table 4 (Exp 1 Criteria) ✅
```csv
Criterion (Max Points),Human Mean,LLM Mean,Difference,p-value
Innovation & Impact (30),25.42,26.11,+0.69,0.367
Methodology (30),21.67,24.48,+2.81,0.073
...
```
✓ Human means present
✓ LLM means present
✓ Statistics calculated

### Table 5 (Exp 1 Vendors) ✅
```csv
Vendor,Mean ± SD,Diff from Human,n
xAI (Grok),85.11 ± 2.37,+6.03,9
Google (Gemini),88.44 ± 4.59,+9.36,9
OpenAI (GPT),77.33 ± 2.74,-1.75,9
```
✓ All vendor data present

### Table 16 (Vendor Overall) ✅
```csv
Vendor,Mean ± SD,n,Diff from Human
xAI (Grok),79.72 ± 6.54,36,+0.64
Google (Gemini),83.50 ± 7.41,36,+4.42
OpenAI (GPT),75.44 ± 4.98,36,-3.64
```
✓ All vendor data present
✓ Counts correct (36 = 9 reviews × 4 experiments)

## Summary of Changes

### Files Modified
- `presentation/generate_tables.py`

### Changes Made
1. **Vendor name mapping** (3 locations):
   - Updated model search terms to match database values
   - Changed: `grok` → `grok-4-fast-reasoning`
   - Changed: `gemini` → `gemini-2.5-flash`
   - Changed: `gpt-4o` → `gpt-5-nano`

2. **Human data retrieval** (3 locations):
   - Fixed Experiment 1 tables to get human data from full dataframe
   - Added comments explaining why separate retrieval is needed
   - Human reviews don't have experiment names, only LLM reviews do

### All Tables Verified

| Table | Status | Notes |
|-------|--------|-------|
| Table 1 | ✅ | Methods - Rubric |
| Table 2 | ✅ | Methods - Vendors |
| Table 3 | ✅ | Exp 1 Overall (was missing human data) |
| Table 4 | ✅ | Exp 1 Criteria (was missing human data) |
| Table 5 | ✅ | Exp 1 Vendors (was missing all data) |
| Table 6 | ✅ | Exp 2 Overall |
| Table 7 | ✅ | Exp 2 Criteria |
| Table 8 | ✅ | Exp 2 Vendors (was missing all data) |
| Table 9 | ✅ | Exp 3 Overall |
| Table 10 | ✅ | Exp 3 Criteria |
| Table 11 | ✅ | Exp 3 Vendors (was missing all data) |
| Table 12 | ✅ | Exp 4 Overall |
| Table 13 | ✅ | Exp 4 Criteria |
| Table 14 | ✅ | Exp 4 Vendors (was missing all data) |
| Table 15 | ✅ | Cross-Experiment |
| Table 16 | ✅ | Vendor Overall (was missing all data) |
| Table 17 | ✅ | Criteria Aggregated |

## Database Schema Notes

For future reference, the `combined_reviews` table has:

**Human reviews** (n=12):
- `reviewer_type` = 'Human'
- `prompt_experiment_name` = NULL (empty)
- `model` = NULL
- `vendor` = NULL

**LLM reviews** (n=108):
- `reviewer_type` = 'LLM'
- `prompt_experiment_name` = 'baseline_v1', 'with_training_data_v1', etc.
- `model` = 'grok-4-fast-reasoning', 'gemini-2.5-flash', 'gpt-5-nano'
- `vendor` = 'xAI', 'Google', 'OpenAI'

This schema difference is why human data needs separate retrieval logic.

---

**Fix completed**: 2025-10-16
**All 17 tables verified**: ✅ Complete with data
