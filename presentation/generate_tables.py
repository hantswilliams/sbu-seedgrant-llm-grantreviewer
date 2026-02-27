"""
Generate manuscript tables from database and save as CSV and PNG files.

This script creates all tables referenced in the manuscript (2_methods.md and 3_results.md),
saves them as CSV files for data archiving, and generates PNG images for markdown inclusion.
"""

import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import numpy as np

# Set up paths
DB_PATH = Path(__file__).parent.parent / "data" / "results.db"
OUTPUT_DIR = Path(__file__).parent / "tables"
OUTPUT_DIR.mkdir(exist_ok=True)

# Set matplotlib style for publication-quality tables
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10


def save_table_as_png(df, filename, title="", figsize=(10, None), header_color='#40466e',
                       row_colors=['#f1f1f2', 'w'], edge_color='w', col_widths=None):
    """
    Save a pandas DataFrame as a PNG image with nice formatting.

    Parameters:
    -----------
    df : pd.DataFrame
        The DataFrame to save
    filename : str
        Output filename (without extension)
    title : str
        Table title
    figsize : tuple
        Figure size (width, height). If height is None, auto-calculate
    header_color : str
        Color for header row
    row_colors : list
        Colors for alternating rows
    edge_color : str
        Color for cell edges
    col_widths : list or None
        Relative column widths
    """
    # Auto-calculate height if not provided
    if figsize[1] is None:
        figsize = (figsize[0], len(df) * 0.4 + 1.5)

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis('tight')
    ax.axis('off')

    # Add title if provided
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', pad=20)

    # Create table
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='left',
                     loc='center', colWidths=col_widths)

    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.8)

    # Color header
    for i in range(len(df.columns)):
        cell = table[(0, i)]
        cell.set_facecolor(header_color)
        cell.set_text_props(weight='bold', color='white')

    # Color rows
    for i in range(1, len(df) + 1):
        for j in range(len(df.columns)):
            cell = table[(i, j)]
            cell.set_facecolor(row_colors[i % len(row_colors)])
            cell.set_edgecolor(edge_color)

    plt.savefig(OUTPUT_DIR / f"{filename}.png", dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close()
    print(f"✓ Saved {filename}.png")


def load_data():
    """Load data from database."""
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM combined_reviews", conn)
    conn.close()
    return df


# =====================================================================
# TABLE 1: Scoring Rubric (Methods)
# =====================================================================
def table_scoring_rubric():
    """Generate scoring rubric table."""
    data = {
        'Criterion': [
            'Innovation & Impact',
            'Methodological Approach & Feasibility',
            'Research Team Strength',
            'External Funding Potential',
            'Budget Clarity',
            'Presentation Quality'
        ],
        'Points': [30, 30, 10, 10, 10, 10],
        'Description': [
            'Originality of approach; potential to advance field; significance of expected outcomes',
            'Rigor of research design; appropriateness of methods; feasibility within timeline/budget',
            'Qualifications of PI and team; relevant expertise and track record',
            'Likelihood of project leading to external funding (e.g., NIH, NSF)',
            'Justification of costs; appropriate allocation of resources',
            'Clarity of writing; organization; completeness of application'
        ]
    }
    df = pd.DataFrame(data)

    # Save CSV
    df.to_csv(OUTPUT_DIR / "table1_scoring_rubric.csv", index=False)

    # Save PNG with adjusted column widths for long descriptions
    save_table_as_png(df, "table1_scoring_rubric",
                      title="Table 1: Grant Review Scoring Rubric",
                      figsize=(12, None), col_widths=[0.15, 0.08, 0.77])

    return df


# =====================================================================
# TABLE 2: LLM Vendors and Models (Methods)
# =====================================================================
def table_llm_vendors():
    """Generate LLM vendors/models table."""
    data = {
        'Vendor': ['OpenAI', 'Google', 'xAI'],
        'Model': ['GPT-4o', 'Gemini', 'Grok'],
        'Version': ['gpt-4o-2024-08-06', 'gemini-1.5-flash', 'grok-beta'],
        'Context Window': ['128K tokens', '1M tokens', '128K tokens']
    }
    df = pd.DataFrame(data)

    # Save CSV
    df.to_csv(OUTPUT_DIR / "table2_llm_vendors.csv", index=False)

    # Save PNG
    save_table_as_png(df, "table2_llm_vendors",
                      title="Table 2: LLM Vendors and Models",
                      figsize=(10, None))

    return df


# =====================================================================
# TABLE 3: Experiment 1 - Overall Scores (Results)
# =====================================================================
def table_exp1_overall(df):
    """Generate Experiment 1 overall score comparison table."""
    exp1_df = df[df['prompt_experiment_name'] == 'baseline_v1']

    # Experiment 1 includes all applicants
    # Human reviews don't have experiment_name, so get them separately
    human_scores = df[df['reviewer_type'] == 'Human']['total_score'].dropna()
    llm_scores = exp1_df[exp1_df['reviewer_type'] == 'LLM']['total_score'].dropna()

    data = {
        'Reviewer Type': ['Human (n=12)', 'LLM (n=27)'],
        'Mean ± SD': [
            f"{human_scores.mean():.2f} ± {human_scores.std():.2f}",
            f"{llm_scores.mean():.2f} ± {llm_scores.std():.2f}"
        ],
        'Median': [f"{human_scores.median():.2f}", f"{llm_scores.median():.2f}"],
        'Range': [
            f"{human_scores.min():.0f}-{human_scores.max():.0f}",
            f"{llm_scores.min():.0f}-{llm_scores.max():.0f}"
        ]
    }
    df_table = pd.DataFrame(data)

    # Save CSV
    df_table.to_csv(OUTPUT_DIR / "table3_exp1_overall.csv", index=False)

    # Save PNG
    save_table_as_png(df_table, "table3_exp1_overall",
                      title="Table 3: Experiment 1 - Overall Score Comparison",
                      figsize=(10, None))

    return df_table


# =====================================================================
# TABLE 4: Experiment 1 - Criterion-Level (Results)
# =====================================================================
def table_exp1_criteria(df):
    """Generate Experiment 1 criterion-level performance table."""
    from scipy import stats

    exp1_df = df[df['prompt_experiment_name'] == 'baseline_v1']

    criteria = [
        ('innovation_impact', 'Innovation & Impact (30)'),
        ('methodological_approach', 'Methodology (30)'),
        ('research_team_strength', 'Team Strength (10)'),
        ('external_funding_potential', 'External Funding (10)'),
        ('budget_clarity', 'Budget Clarity (10)'),
        ('presentation_quality', 'Presentation (10)')
    ]

    results = []
    for col_name, display_name in criteria:
        # Human reviews don't have experiment_name, so get them separately
        human_vals = df[df['reviewer_type'] == 'Human'][col_name].dropna()
        llm_vals = exp1_df[exp1_df['reviewer_type'] == 'LLM'][col_name].dropna()

        diff = llm_vals.mean() - human_vals.mean()
        t_stat, p_val = stats.ttest_ind(llm_vals, human_vals)

        results.append({
            'Criterion (Max Points)': display_name,
            'Human Mean': f"{human_vals.mean():.2f}",
            'LLM Mean': f"{llm_vals.mean():.2f}",
            'Difference': f"{diff:+.2f}",
            'p-value': f"{p_val:.3f}"
        })

    df_table = pd.DataFrame(results)

    # Save CSV
    df_table.to_csv(OUTPUT_DIR / "table4_exp1_criteria.csv", index=False)

    # Save PNG
    save_table_as_png(df_table, "table4_exp1_criteria",
                      title="Table 4: Experiment 1 - Criterion-Level Performance",
                      figsize=(12, None))

    return df_table


# =====================================================================
# TABLE 5: Experiment 1 - Vendor Performance (Results)
# =====================================================================
def table_exp1_vendors(df):
    """Generate Experiment 1 vendor performance table."""
    exp1_df = df[df['prompt_experiment_name'] == 'baseline_v1']
    # Human reviews don't have experiment_name, so get them separately
    human_mean = df[df['reviewer_type'] == 'Human']['total_score'].mean()

    vendors = ['grok-4-fast-reasoning', 'gemini-2.5-flash', 'gpt-5-nano']
    vendor_display = {
        'grok-4-fast-reasoning': 'xAI (Grok)',
        'gemini-2.5-flash': 'Google (Gemini)',
        'gpt-5-nano': 'OpenAI (GPT)'
    }

    results = []
    for vendor in vendors:
        vendor_df = exp1_df[(exp1_df['reviewer_type'] == 'LLM') &
                           (exp1_df['model'] == vendor)]
        scores = vendor_df['total_score'].dropna()

        results.append({
            'Vendor': vendor_display[vendor],
            'Mean ± SD': f"{scores.mean():.2f} ± {scores.std():.2f}",
            'Diff from Human': f"{scores.mean() - human_mean:+.2f}",
            'n': len(scores)
        })

    df_table = pd.DataFrame(results)

    # Save CSV
    df_table.to_csv(OUTPUT_DIR / "table5_exp1_vendors.csv", index=False)

    # Save PNG
    save_table_as_png(df_table, "table5_exp1_vendors",
                      title="Table 5: Experiment 1 - Vendor Performance",
                      figsize=(10, None))

    return df_table


# =====================================================================
# TABLE 6-11: Experiments 2, 3, 4 - Similar tables
# =====================================================================
def table_experiment_overall(df, exp_name, exp_num, exp_label):
    """Generate overall score table for a specific experiment.

    Experiments 2-4 exclude DANIEL (used as training example).
    """
    exp_df = df[df['prompt_experiment_name'] == exp_name]

    # Experiments 2-4 exclude DANIEL from LLM reviews (used in training examples)
    if exp_name in ['with_training_data_v1', 'multi_examples_v1', 'strict_scoring_v1']:
        exp_df = exp_df[exp_df['applicant_name'] != 'DANIEL']

    human_df = df[df['reviewer_type'] == 'Human']  # Use all human reviews

    human_scores = human_df['total_score'].dropna()
    llm_scores = exp_df[exp_df['reviewer_type'] == 'LLM']['total_score'].dropna()

    human_mean = human_scores.mean()
    llm_mean = llm_scores.mean()

    data = {
        'Reviewer Type': ['Human (n=12)', f'LLM (n={len(llm_scores)})'],
        'Mean ± SD': [
            f"{human_mean:.2f} ± {human_scores.std():.2f}",
            f"{llm_mean:.2f} ± {llm_scores.std():.2f}"
        ],
        'Diff from Human': ['—', f"{llm_mean - human_mean:+.2f}"]
    }
    df_table = pd.DataFrame(data)

    # Save CSV
    df_table.to_csv(OUTPUT_DIR / f"table{exp_num}_exp{exp_num-5}_overall.csv", index=False)

    # Save PNG
    save_table_as_png(df_table, f"table{exp_num}_exp{exp_num-5}_overall",
                      title=f"Table {exp_num}: Experiment {exp_num-5} ({exp_label}) - Overall Scores",
                      figsize=(10, None))

    return df_table


def table_experiment_criteria(df, exp_name, exp_num, exp_label):
    """Generate criterion-level table for a specific experiment.

    Experiments 2-4 exclude DANIEL (used as training example).
    """
    exp_df = df[df['prompt_experiment_name'] == exp_name]

    # Experiments 2-4 exclude DANIEL from LLM reviews (used in training examples)
    if exp_name in ['with_training_data_v1', 'multi_examples_v1', 'strict_scoring_v1']:
        exp_df = exp_df[exp_df['applicant_name'] != 'DANIEL']

    human_df = df[df['reviewer_type'] == 'Human']

    criteria = [
        ('innovation_impact', 'Innovation & Impact (30)'),
        ('methodological_approach', 'Methodology (30)'),
        ('research_team_strength', 'Team Strength (10)'),
        ('external_funding_potential', 'External Funding (10)'),
        ('budget_clarity', 'Budget Clarity (10)'),
        ('presentation_quality', 'Presentation (10)')
    ]

    results = []
    for col_name, display_name in criteria:
        human_vals = human_df[col_name].dropna()
        llm_vals = exp_df[exp_df['reviewer_type'] == 'LLM'][col_name].dropna()

        diff = llm_vals.mean() - human_vals.mean()

        results.append({
            'Criterion': display_name,
            'Human Mean': f"{human_vals.mean():.2f}",
            'LLM Mean': f"{llm_vals.mean():.2f}",
            'Difference': f"{diff:+.2f}"
        })

    df_table = pd.DataFrame(results)

    # Save CSV
    df_table.to_csv(OUTPUT_DIR / f"table{exp_num+1}_exp{exp_num-5}_criteria.csv", index=False)

    # Save PNG
    save_table_as_png(df_table, f"table{exp_num+1}_exp{exp_num-5}_criteria",
                      title=f"Table {exp_num+1}: Experiment {exp_num-5} ({exp_label}) - Criteria",
                      figsize=(11, None))

    return df_table


def table_experiment_vendors(df, exp_name, exp_num, exp_label):
    """Generate vendor performance table for a specific experiment.

    Experiments 2-4 exclude DANIEL (used as training example).
    """
    exp_df = df[df['prompt_experiment_name'] == exp_name]

    # Experiments 2-4 exclude DANIEL from LLM reviews (used in training examples)
    if exp_name in ['with_training_data_v1', 'multi_examples_v1', 'strict_scoring_v1']:
        exp_df = exp_df[exp_df['applicant_name'] != 'DANIEL']

    human_mean = df[df['reviewer_type'] == 'Human']['total_score'].mean()

    vendors = ['grok-4-fast-reasoning', 'gemini-2.5-flash', 'gpt-5-nano']
    vendor_display = {
        'grok-4-fast-reasoning': 'xAI (Grok)',
        'gemini-2.5-flash': 'Google (Gemini)',
        'gpt-5-nano': 'OpenAI (GPT)'
    }

    results = []
    for vendor in vendors:
        vendor_df = exp_df[(exp_df['reviewer_type'] == 'LLM') &
                          (exp_df['model'] == vendor)]
        scores = vendor_df['total_score'].dropna()

        results.append({
            'Vendor': vendor_display[vendor],
            'Mean ± SD': f"{scores.mean():.2f} ± {scores.std():.2f}",
            'Diff from Human': f"{scores.mean() - human_mean:+.2f}"
        })

    df_table = pd.DataFrame(results)

    # Save CSV
    df_table.to_csv(OUTPUT_DIR / f"table{exp_num+2}_exp{exp_num-5}_vendors.csv", index=False)

    # Save PNG
    save_table_as_png(df_table, f"table{exp_num+2}_exp{exp_num-5}_vendors",
                      title=f"Table {exp_num+2}: Experiment {exp_num-5} ({exp_label}) - Vendors",
                      figsize=(10, None))

    return df_table


# =====================================================================
# TABLE 15: Cross-Experiment Summary
# =====================================================================
def table_cross_experiment_summary(df):
    """Generate cross-experiment comparison table.

    Experiments 2-4 exclude DANIEL (used as training example).
    """
    experiments = [
        ('baseline_v1', 'Exp 1: Baseline'),
        ('with_training_data_v1', 'Exp 2: Single Example'),
        ('multi_examples_v1', 'Exp 3: Multiple Examples'),
        ('strict_scoring_v1', 'Exp 4: Strict Scoring')
    ]

    human_mean = df[df['reviewer_type'] == 'Human']['total_score'].mean()

    from scipy import stats

    results = []
    for exp_name, exp_label in experiments:
        exp_df = df[df['prompt_experiment_name'] == exp_name]

        # Experiments 2-4 exclude DANIEL from LLM reviews (used in training examples)
        if exp_name in ['with_training_data_v1', 'multi_examples_v1', 'strict_scoring_v1']:
            exp_df = exp_df[exp_df['applicant_name'] != 'DANIEL']

        llm_scores = exp_df[exp_df['reviewer_type'] == 'LLM']['total_score'].dropna()
        human_scores = df[df['reviewer_type'] == 'Human']['total_score'].dropna()

        t_stat, p_val = stats.ttest_ind(llm_scores, human_scores)

        results.append({
            'Experiment': exp_label,
            'LLM Mean': f"{llm_scores.mean():.2f}",
            'Diff from Human': f"{llm_scores.mean() - human_mean:+.2f}",
            'p-value': f"{p_val:.3f}" if p_val >= 0.001 else "<0.001"
        })

    df_table = pd.DataFrame(results)

    # Save CSV
    df_table.to_csv(OUTPUT_DIR / "table15_cross_experiment.csv", index=False)

    # Save PNG
    save_table_as_png(df_table, "table15_cross_experiment",
                      title="Table 15: Cross-Experiment Comparison",
                      figsize=(11, None))

    return df_table


# =====================================================================
# TABLE 16: Overall Vendor Performance
# =====================================================================
def table_vendor_overall(df):
    """Generate overall vendor performance across all experiments."""
    human_mean = df[df['reviewer_type'] == 'Human']['total_score'].mean()

    vendors = ['grok-4-fast-reasoning', 'gemini-2.5-flash', 'gpt-5-nano']
    vendor_display = {
        'grok-4-fast-reasoning': 'xAI (Grok)',
        'gemini-2.5-flash': 'Google (Gemini)',
        'gpt-5-nano': 'OpenAI (GPT)'
    }

    results = []
    for vendor in vendors:
        vendor_df = df[(df['reviewer_type'] == 'LLM') &
                      (df['model'] == vendor)]
        scores = vendor_df['total_score'].dropna()

        results.append({
            'Vendor': vendor_display[vendor],
            'Mean ± SD': f"{scores.mean():.2f} ± {scores.std():.2f}",
            'n': len(scores),
            'Diff from Human': f"{scores.mean() - human_mean:+.2f}"
        })

    df_table = pd.DataFrame(results)

    # Save CSV
    df_table.to_csv(OUTPUT_DIR / "table16_vendor_overall.csv", index=False)

    # Save PNG
    save_table_as_png(df_table, "table16_vendor_overall",
                      title="Table 16: Overall Vendor Performance (All Experiments)",
                      figsize=(11, None))

    return df_table


# =====================================================================
# TABLE 17: Criterion-Level Aggregated
# =====================================================================
def table_criteria_aggregated(df):
    """Generate aggregated criterion-level performance table."""
    human_df = df[df['reviewer_type'] == 'Human']
    llm_df = df[df['reviewer_type'] == 'LLM']

    from scipy import stats

    criteria = [
        ('innovation_impact', 'Innovation & Impact (30)', 30),
        ('methodological_approach', 'Methodology (30)', 30),
        ('research_team_strength', 'Team Strength (10)', 10),
        ('external_funding_potential', 'External Funding (10)', 10),
        ('budget_clarity', 'Budget Clarity (10)', 10),
        ('presentation_quality', 'Presentation (10)', 10)
    ]

    results = []
    for col_name, display_name, max_points in criteria:
        human_vals = human_df[col_name].dropna()
        llm_vals = llm_df[col_name].dropna()

        human_pct = (human_vals.mean() / max_points) * 100
        llm_pct = (llm_vals.mean() / max_points) * 100
        diff_pct = llm_pct - human_pct

        t_stat, p_val = stats.ttest_ind(llm_vals, human_vals)

        results.append({
            'Criterion (Max)': display_name,
            'Human %': f"{human_pct:.1f}%",
            'LLM %': f"{llm_pct:.1f}%",
            'Difference': f"{diff_pct:+.1f}%",
            'p-value': f"{p_val:.3f}"
        })

    df_table = pd.DataFrame(results)

    # Save CSV
    df_table.to_csv(OUTPUT_DIR / "table17_criteria_aggregated.csv", index=False)

    # Save PNG
    save_table_as_png(df_table, "table17_criteria_aggregated",
                      title="Table 17: Aggregated Criterion-Level Performance",
                      figsize=(12, None))

    return df_table


# =====================================================================
# MAIN EXECUTION
# =====================================================================
def main():
    """Generate all manuscript tables."""
    print("\n" + "="*70)
    print("GENERATING MANUSCRIPT TABLES")
    print("="*70 + "\n")

    # Load data
    print("Loading data from database...")
    df = load_data()
    print(f"✓ Loaded {len(df)} reviews\n")

    # Methods tables
    print("METHODS TABLES:")
    print("-" * 70)
    table_scoring_rubric()
    table_llm_vendors()
    print()

    # Results tables - Experiment 1
    print("RESULTS TABLES - EXPERIMENT 1:")
    print("-" * 70)
    table_exp1_overall(df)
    table_exp1_criteria(df)
    table_exp1_vendors(df)
    print()

    # Results tables - Experiments 2, 3, 4
    experiments = [
        ('with_training_data_v1', 6, 'Single Example'),
        ('multi_examples_v1', 9, 'Multiple Examples'),
        ('strict_scoring_v1', 12, 'Strict Scoring')
    ]

    for exp_name, exp_num, exp_label in experiments:
        print(f"RESULTS TABLES - {exp_label.upper()}:")
        print("-" * 70)
        table_experiment_overall(df, exp_name, exp_num, exp_label)
        table_experiment_criteria(df, exp_name, exp_num, exp_label)
        table_experiment_vendors(df, exp_name, exp_num, exp_label)
        print()

    # Cross-experiment and aggregated tables
    print("CROSS-EXPERIMENT AND AGGREGATED TABLES:")
    print("-" * 70)
    table_cross_experiment_summary(df)
    table_vendor_overall(df)
    table_criteria_aggregated(df)
    print()

    print("="*70)
    print(f"✓ All tables generated successfully!")
    print(f"✓ Output directory: {OUTPUT_DIR}")
    print(f"✓ Generated {len(list(OUTPUT_DIR.glob('*.csv')))} CSV files")
    print(f"✓ Generated {len(list(OUTPUT_DIR.glob('*.png')))} PNG images")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
