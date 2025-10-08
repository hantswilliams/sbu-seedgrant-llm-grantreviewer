# Update Summary: Rosie Data Exclusion

## Date: October 14, 2025

### Changes Made

Due to the requirement to exclude Rosie's data from the analysis, all presentation materials have been updated to reflect the revised dataset (3 applicants instead of 4).

---

## Files Updated

### 1. Data Processing
- ✅ **`combine_reviews.py`** - Updated to exclude Rosie from both human and LLM reviews
- ✅ **Database regenerated** - `data/results.db` combined_reviews table now excludes Rosie

### 2. Analysis & Figures
- ✅ **`presentation/generate_analyses.py`** - Re-run with updated data
- ✅ **`presentation/generate_figures.py`** - Re-run to regenerate all 8 figures
- ✅ **`presentation/analysis_output.txt`** - Updated with new statistics
- ✅ **`presentation/analysis_results.json`** - Updated with new data
- ✅ **All slide*.png files** - Regenerated with 3 applicants (S1-S3)

### 3. Presentation Materials
- ✅ **`presentation/presentation_marp.md`** - All statistics updated
- ✅ **`presentation/README.md`** - Data notes updated

---

## Key Statistical Changes

### Dataset Size
| Metric | Before (4 applicants) | After (3 applicants) | Change |
|--------|----------------------|---------------------|--------|
| Human reviews | 16 | 12 | -4 |
| LLM reviews | 144 | 108 | -36 |
| Total reviews | 160 | 120 | -40 |
| Applicants | 4 (including Rosie) | 3 (Christina, Daniel, Kelly) | -1 |

### Overall Performance (Slide 5)
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Human Mean ± SD** | 80.81 ± 12.55 | 79.08 ± 13.32 | -1.73 pts |
| **LLM Mean ± SD** | 79.81 ± 7.34 | 79.56 ± 7.14 | -0.25 pts |
| **Difference** | -1.00 pts | +0.47 pts | +1.47 pts |
| **p-value** | 0.635 | 0.845 | More ns |
| **Cohen's d** | -0.10 | 0.04 | Closer to 0 |

### Criteria Performance (Slide 6)
**External Funding (only significant finding):**
- Before: +0.51 pts (p=0.035)
- After: +0.69 pts (p=0.022)
- **Still significant, stronger effect**

**Methodology:**
- Before: -0.11 pts (ns)
- After: +0.96 pts (ns)
- **Direction changed to LLM advantage**

### Prompt Engineering (Slide 7)
| Experiment | Before (n) | After (n) | Mean Change |
|------------|-----------|----------|-------------|
| Baseline | 84.50 (36) | 83.63 (27) | -0.87 pts |
| Single Example | 84.37 (27) | 84.94 (18) | +0.57 pts |
| **Multi Examples** | **80.37 (27)** | **80.56 (18)** | **+0.19 pts** |
| Strict | 72.30 (27) | 72.44 (18) | +0.14 pts |

**Best alignment:**
- Before: Multi Examples (0.44 pts from human)
- After: Multi Examples (1.47 pts from human)
- **Still best, slightly larger difference**

### Model Performance (Slide 8)
| Vendor | Before (n=48) | After (n=36) | Change |
|--------|--------------|--------------|---------|
| **xAI (Rank)** | **#1: -0.10 pts** | **#1: +0.64 pts** | Still best |
| OpenAI (Rank) | #3: -5.27 pts | #2: -3.64 pts | Improved rank |
| Google (Rank) | #2: +2.38 pts | #3: +4.42 pts | Lower rank |

**xAI still best**, but ranking order changed.

### Inter-Rater Reliability (Slide 9)
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| **Human SD** | 10.88 | 11.37 | +0.49 (more variable) |
| **LLM SD** | 7.19 | 6.94 | -0.25 (more consistent) |
| **LLM consistency advantage** | 34% | **39%** | **+5%** |
| **Pearson r** | 0.91 | 0.90 | -0.01 (still strong) |
| **Spearman ρ** | 1.00 | 1.00 | No change (perfect) |
| **Recommendation agreement** | 0% | 0% | No change |

**LLMs even MORE consistent** after Rosie exclusion.

---

## Interpretation

### What Stayed the Same ✓
- ✅ No significant difference in overall scores (still p>0.05)
- ✅ External Funding still the only significant criterion
- ✅ Multiple examples still best prompt engineering approach
- ✅ xAI still best model for alignment
- ✅ Perfect rank-order agreement (Spearman ρ=1.0)
- ✅ 0% recommendation agreement (critical finding intact)

### What Changed 📊
- 📈 LLMs became **even more consistent** (39% vs 34% advantage)
- 📈 External Funding effect **stronger** (0.69 vs 0.51 pts)
- 📈 LLMs now score **higher** on Methodology (was negative before)
- 📊 Overall difference flipped from -1.00 to +0.47 (LLMs now slightly higher, but still ns)
- 📊 Model ranking changed: OpenAI moved to #2, Google to #3

### Key Insight 💡
**Rosie's data was moderating the LLM consistency advantage.** Without her data:
- Human variability increased slightly (11.37 vs 10.88)
- LLM consistency improved (6.94 vs 7.19)
- LLM advantage more pronounced (39% vs 34%)

This **strengthens the reliability argument** for LLMs.

---

## Presentation Impact

### Main Conclusions - UNCHANGED ✅
The core narrative of the presentation remains valid:
1. ✅ LLMs match human scoring accuracy
2. ✅ Prompt engineering matters (multi examples best)
3. ✅ Model selection matters (xAI best)
4. ✅ LLMs more consistent than humans
5. ✅ **Critical limitation: 0% recommendation agreement**

### Numbers to Update in Talks
When presenting verbally, use:
- "3 grant applications" (not 4)
- "12 human reviews" (not 16)
- "108 LLM reviews" (not 144)
- "39% more consistent" (not 34%)
- "S1-S3" in figures (not S1-S4)

---

## Files Ready for Presentation

All materials are now current and consistent:

✅ **Marp Presentation**: `presentation/presentation_marp.md`
   - Export with: `marp presentation_marp.md -o slides.pdf`

✅ **Figures**: All 8 PNG files regenerated with 3 applicants

✅ **Analysis Results**:
   - JSON: `analysis_results.json`
   - Text: `analysis_output.txt`

✅ **Documentation**: README updated with correct sample sizes

---

## Quality Checks Performed ✓

- [x] All n values correct (12 human, 108 LLM)
- [x] All statistics recalculated and updated
- [x] Figures regenerated with anonymized labels (S1-S3)
- [x] p-values and effect sizes updated
- [x] Percentages and proportions recalculated
- [x] Conclusions still supported by data
- [x] No references to "4 applicants" or "Rosie" in presentation
- [x] Consistency between Marp slides and analysis results

---

## Next Steps

1. ✅ **Review the updated presentation_marp.md**
2. ✅ **Generate final slides**: `marp presentation/presentation_marp.md -o presentation/slides.pdf`
3. ✅ **Practice presentation** with updated numbers
4. ✅ **Prepare to discuss** why 3 applicants (if asked)

The presentation is now **publication-ready** with the corrected dataset! 🎉
