# Manuscript Tables

This directory contains all tables referenced in the manuscript, generated programmatically from the analysis database.

## Overview

- **17 tables total**: 2 for Methods section, 15 for Results section
- **Dual format**: Each table saved as both CSV (data) and PNG (image)
- **Automated generation**: All tables created via `generate_tables.py` script
- **Database-driven**: Tables pull data directly from `data/results.db`

## File Structure

```
presentation/tables/
├── README.md                      # This file
├── TABLE_REFERENCES.md            # How to reference tables in markdown
├── generate_tables.py             # Generation script (in parent dir)
│
├── table1_scoring_rubric.{csv,png}       # Methods: Evaluation rubric
├── table2_llm_vendors.{csv,png}          # Methods: LLM vendors/models
│
├── table3_exp1_overall.{csv,png}         # Results: Exp 1 overall scores
├── table4_exp1_criteria.{csv,png}        # Results: Exp 1 criteria
├── table5_exp1_vendors.{csv,png}         # Results: Exp 1 vendors
│
├── table6_exp2_overall.{csv,png}         # Results: Exp 2 overall scores
├── table7_exp2_criteria.{csv,png}        # Results: Exp 2 criteria
├── table8_exp2_vendors.{csv,png}         # Results: Exp 2 vendors
│
├── table9_exp3_overall.{csv,png}         # Results: Exp 3 overall scores
├── table10_exp3_criteria.{csv,png}       # Results: Exp 3 criteria
├── table11_exp3_vendors.{csv,png}        # Results: Exp 3 vendors
│
├── table12_exp4_overall.{csv,png}        # Results: Exp 4 overall scores
├── table13_exp4_criteria.{csv,png}       # Results: Exp 4 criteria
├── table14_exp4_vendors.{csv,png}        # Results: Exp 4 vendors
│
├── table15_cross_experiment.{csv,png}    # Results: Cross-experiment comparison
├── table16_vendor_overall.{csv,png}      # Results: Overall vendor performance
└── table17_criteria_aggregated.{csv,png} # Results: Aggregated criteria
```

## Usage

### In Manuscript Markdown Files

To include a table in your markdown (e.g., `manuscript/2_methods.md` or `manuscript/3_results.md`):

```markdown
![Table 1: Scoring Rubric](../presentation/tables/table1_scoring_rubric.png)
```

Or with a caption:

```markdown
**Table 1: Grant Review Scoring Rubric**

![Table 1: Scoring Rubric](../presentation/tables/table1_scoring_rubric.png)

*All reviews (human and LLM) used this standardized six-criterion rubric with 100 total points.*
```

### Regenerating Tables

After updating data or analysis:

```bash
cd /path/to/project
python presentation/generate_tables.py
```

The script will:
1. Load data from `data/results.db`
2. Calculate statistics (means, SDs, t-tests, etc.)
3. Generate formatted tables
4. Save as CSV (for archiving) and PNG (for display)
5. Output to `presentation/tables/`

## Table Contents

### Methods Section Tables

**Table 1: Scoring Rubric**
- 6 evaluation criteria
- Point allocations (30/30/10/10/10/10)
- Description of each criterion

**Table 2: LLM Vendors and Models**
- OpenAI GPT-4o
- Google Gemini 1.5 Flash
- xAI Grok Beta
- Model versions and context windows

### Results Section Tables

#### Experiment 1: Baseline (Zero-Shot)
- Table 3: Overall score comparison (human vs. LLM)
- Table 4: Criterion-level performance
- Table 5: Vendor performance

#### Experiment 2: Single Training Example
- Table 6: Overall scores
- Table 7: Criterion-level performance
- Table 8: Vendor performance

#### Experiment 3: Multiple Training Examples
- Table 9: Overall scores (best alignment: +1.47, p=0.486)
- Table 10: Criterion-level performance
- Table 11: Vendor performance

#### Experiment 4: Strict Scoring Instructions
- Table 12: Overall scores (under-scoring: -6.64, p=0.004)
- Table 13: Criterion-level performance
- Table 14: Vendor performance

#### Aggregated Analyses
- Table 15: Cross-experiment summary (all 4 experiments)
- Table 16: Overall vendor performance (xAI Grok best: +1.46)
- Table 17: Aggregated criterion-level (External Funding +6.1%, p=0.012)

## Customization

To modify table appearance, edit `presentation/generate_tables.py`:

```python
def save_table_as_png(...):
    # Adjust these parameters:
    header_color='#40466e',      # Header background color
    row_colors=['#f1f1f2', 'w'], # Alternating row colors
    figsize=(10, None),          # Table size
    # ... more styling options
```

## Data Formats

### CSV Files
- Comma-separated values
- Column headers included
- Suitable for spreadsheet import or further analysis

### PNG Files
- 300 DPI resolution (publication quality)
- White background
- Professional table formatting
- Alternating row colors for readability
- Bold headers with contrasting color

## Dependencies

Required Python packages (already in `requirements.txt`):
- pandas
- matplotlib
- sqlite3 (built-in)
- scipy
- numpy

## Notes

- Tables are generated programmatically, ensuring consistency with analysis results
- PNG images are publication-ready (300 DPI)
- CSV files preserve exact numerical values
- All statistics computed from database ensure reproducibility
- Tables automatically update when underlying data changes

## Troubleshooting

**Issue**: "Unable to open database file"
- **Solution**: Check that `data/results.db` exists and is accessible

**Issue**: Column name errors
- **Solution**: Verify column names match database schema:
  - `prompt_experiment_name` not `experiment_name`
  - `model` not `model_name`
  - `methodological_approach` not `methodology`

**Issue**: Missing figures
- **Solution**: Ensure `presentation/tables/` directory exists (created automatically)

## Contact

For questions or issues with table generation, see the main project README or contact the research team.
