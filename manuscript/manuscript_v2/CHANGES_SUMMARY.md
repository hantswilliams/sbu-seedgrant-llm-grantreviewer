# Summary of Changes from Manuscript v1 to v2

## Overview
Updated manuscript to reflect the restructuring from 4 experiments to 3 experiments, removing Experiment 2 (One-Shot Learning / with_training_data_v1).

## Global Changes Across All Files

### Sample Size Updates
- **Total LLM Reviews**: 108 → 81 (27 per experiment × 3 experiments)
- **Exp1 (Zero-Shot)**: 12 human + 27 LLM (unchanged)
- **Exp2 (One-Shot)**: REMOVED ENTIRELY
- **Exp3 (Few-Shot)**: 8 human + 18 LLM (DANIEL completely excluded - both human and LLM)
- **Exp4 (Stricter)**: 8 human + 18 LLM (DANIEL completely excluded - both human and LLM)

### Figure Path Updates
- All figure references changed from `scripts/output/` to `scripts/output_v2/`

### Agreement Metrics
- Added distinction between "Broad Agreement" (Positive vs Negative) and "Exact Agreement"
- Updated all agreement rate discussions to reflect both metrics

## File-by-File Changes

### 1_intro.md
✅ **COMPLETED**
- Updated from "four experiments" to "three experiments"
- Removed Experiment 2 (One-Shot Learning) description
- Updated research questions section to list only Experiments 1, 3, and 4
- Updated study contributions to mention "broad vs exact agreement metrics"
- Updated experimental design description to clarify that BOTH human AND LLM reviews of training applicants are excluded

### 2_methods.md
**TO BE UPDATED**
- Update study design from "4×3×3×3" to "3×3×3×3"
- Remove entire "Experiment 2: One-Shot Learning" section
- Update Experiment 3 description to clarify BOTH human and LLM exclusion for DANIEL
- Update Experiment 4 description to clarify BOTH human and LLM exclusion for DANIEL
- Update total sample size summary from 108 to 81 LLM reviews
- Update human comparison instances from 42 to 28
- Update iteration strategy totals: 81 LLM reviews (3 vendors × 3 applicants × 3 iterations) × 3 experiments

### 3_results.md
**TO BE UPDATED**
- Remove entire "Experiment 2: One-Shot Learning" section (including all subsections)
- Update Overview from "four prompt engineering experiments" to "three"
- Update Sample Sizes table to show only Experiments 1, 3, and 4
- Update all figure references from output/ to output_v2/
- Update cross-experiment comparison section:
  - Remove Exp2 from all tables and figures
  - Update post-hoc comparisons to only include Exp1, Exp3, Exp4
  - Update vendor performance table to remove Exp2 column
- Update recommendation agreement analysis with broad vs exact metrics
- Update all "four experiments" language to "three experiments"

### 4_discussion.md
**TO BE UPDATED**
- Update summary of principal findings to reference 3 experiments instead of 4
- Remove all references to Experiment 2 findings
- Update score difference range discussion (removing Exp2 data)
- Update "why multiple examples outperformed single examples" section to remove comparison to Exp2
- Update cross-experiment comparisons removing Exp2
- Update vendor performance tables and discussions
- Update all statistical comparisons that included Exp2
- Update best practice recommendations to remove Exp2 references
- Update conclusion to reflect 3-experiment design

## Key Methodological Updates

### Experiment 3 & 4 Exclusion Logic
**IMPORTANT CHANGE**: Both experiments now exclude DANIEL **completely** (both human AND LLM reviews), not just human reviews. This is because:
- All 4 human reviews of DANIEL were used as training data
- Therefore, DANIEL LLM reviews would be "contaminated" by training on that applicant
- To maintain independence, BOTH human and LLM reviews of DANIEL are excluded from analysis
- This reduces sample sizes from 27 LLM + 8 human to 18 LLM + 8 human for Exp3 and Exp4

### Agreement Metrics Enhancement
Added two-level agreement analysis:
1. **Exact Agreement**: Matching on specific recommendation (Fund, Fund with Revisions, Do Not Fund)
2. **Broad Agreement**: Matching on funding decision category (Positive = Fund or Fund with Revisions, Negative = Do Not Fund)

This provides more nuanced understanding of LLM-human alignment on funding decisions.

## Files Status
- ✅ 1_intro.md - COMPLETED
- ⏳ 2_methods.md - IN PROGRESS
- ⏳ 3_results.md - PENDING
- ⏳ 4_discussion.md - PENDING
