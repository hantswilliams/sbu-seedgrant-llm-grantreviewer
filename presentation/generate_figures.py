#!/usr/bin/env python3
"""
Generate presentation figures from grant review database

This script creates static visualizations for the presentation slides.
All figures are saved to the ./presentation/ directory.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from scipy import stats

# Set style
sns.set_style("whitegrid")
sns.set_palette("colorblind")
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10

# Define paths
BASE_PATH = Path(__file__).parent.parent
DB_PATH = BASE_PATH / "data" / "results.db"
OUTPUT_PATH = Path(__file__).parent

# Experiments that exclude Daniel
EXPERIMENTS_EXCLUDING_DANIEL = ['with_training_data_v1', 'multi_examples_v1', 'strict_scoring_v1']

def load_data():
    """Load data from database"""
    conn = sqlite3.connect(DB_PATH)

    # Load combined reviews
    query = """
    SELECT * FROM combined_reviews
    ORDER BY applicant_name, reviewer_type, reviewer_id
    """
    df = pd.read_sql_query(query, conn)

    conn.close()
    return df

def filter_for_experiment(df, experiment_name):
    """Filter data for specific experiment, excluding Daniel if needed"""
    if experiment_name is None:
        return df

    # Filter by experiment
    filtered = df[(df['prompt_experiment_name'] == experiment_name) | (df['reviewer_type'] == 'Human')]

    # Exclude Daniel from LLM if needed
    if experiment_name in EXPERIMENTS_EXCLUDING_DANIEL:
        filtered = filtered[~((filtered['applicant_name'] == 'DANIEL') & (filtered['reviewer_type'] == 'LLM'))]

    return filtered

def slide2_problem_statement():
    """Create infographic for problem statement (placeholder)"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Simple text-based infographic
    ax.text(0.5, 0.8, 'Grant Review Challenges',
            ha='center', va='center', fontsize=20, fontweight='bold')

    challenges = [
        '⏱️  Time-intensive process (hours per review)',
        '👥  Limited reviewer availability',
        '📊  Variable inter-rater reliability',
        '💰  High cost of expert reviewers',
        '🔄  Growing application volumes'
    ]

    y_pos = 0.6
    for challenge in challenges:
        ax.text(0.5, y_pos, challenge, ha='center', va='center', fontsize=14)
        y_pos -= 0.12

    ax.axis('off')
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / 'slide2_problem_statement.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated slide2_problem_statement.png")

def slide3_study_design():
    """Create study design flowchart"""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Create simple flowchart using text and arrows
    ax.text(0.5, 0.95, 'Study Design Overview',
            ha='center', va='center', fontsize=18, fontweight='bold')

    # Data collection
    ax.text(0.5, 0.85, '4 Grant Applications',
            ha='center', va='center', fontsize=14,
            bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))

    # Reviewers
    ax.text(0.2, 0.7, 'Human Reviewers\n(n=4 per application)',
            ha='center', va='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

    ax.text(0.8, 0.7, 'LLM Reviewers\n(4 vendors, 4 experiments)',
            ha='center', va='center', fontsize=12,
            bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))

    # Criteria
    ax.text(0.5, 0.5, '6 Evaluation Criteria (100 points)',
            ha='center', va='center', fontsize=14, fontweight='bold')

    criteria = [
        'Innovation & Impact (30 pts)',
        'Methodology & Feasibility (30 pts)',
        'Team Strength (10 pts)',
        'External Funding (10 pts)',
        'Budget Clarity (10 pts)',
        'Presentation (10 pts)'
    ]

    y_pos = 0.38
    for criterion in criteria:
        ax.text(0.5, y_pos, criterion, ha='center', va='center', fontsize=10)
        y_pos -= 0.06

    # Analysis
    ax.text(0.5, 0.05, 'Statistical Analysis & Comparison',
            ha='center', va='center', fontsize=14,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.7))

    # Draw arrows
    ax.annotate('', xy=(0.5, 0.82), xytext=(0.2, 0.75),
                arrowprops=dict(arrowstyle='->', lw=2, color='gray'))
    ax.annotate('', xy=(0.5, 0.82), xytext=(0.8, 0.75),
                arrowprops=dict(arrowstyle='->', lw=2, color='gray'))
    ax.annotate('', xy=(0.5, 0.53), xytext=(0.5, 0.67),
                arrowprops=dict(arrowstyle='->', lw=2, color='gray'))
    ax.annotate('', xy=(0.5, 0.08), xytext=(0.5, 0.42),
                arrowprops=dict(arrowstyle='->', lw=2, color='gray'))

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / 'slide3_study_design.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated slide3_study_design.png")

def slide4_experiment_conditions():
    """Create table of experiment conditions"""
    experiments = {
        'Experiment': ['baseline_v1', 'with_training_data_v1', 'multi_examples_v1', 'strict_scoring_v1'],
        'Training Examples': ['None', '1 review', '4 reviews', '1 review'],
        'Special Instructions': ['Standard', 'None', 'Show score variance', 'Strict/conservative'],
        'Training Applicant Excluded': ['No', 'Yes', 'Yes', 'Yes']
    }

    df = pd.DataFrame(experiments)

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.axis('tight')
    ax.axis('off')

    table = ax.table(cellText=df.values, colLabels=df.columns,
                     cellLoc='left', loc='center',
                     colWidths=[0.28, 0.20, 0.28, 0.24])

    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2)

    # Style header
    for i in range(len(df.columns)):
        table[(0, i)].set_facecolor('#4472C4')
        table[(0, i)].set_text_props(weight='bold', color='white')

    # Alternate row colors
    for i in range(1, len(df) + 1):
        for j in range(len(df.columns)):
            if i % 2 == 0:
                table[(i, j)].set_facecolor('#E7E6E6')

    plt.savefig(OUTPUT_PATH / 'slide4_experiment_conditions.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated slide4_experiment_conditions.png")

def slide5_human_vs_llm_overall(df):
    """Box plots comparing human vs. LLM total scores"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Prepare data
    human_scores = df[df['reviewer_type'] == 'Human']['total_score'].dropna()
    llm_scores = df[df['reviewer_type'] == 'LLM']['total_score'].dropna()

    data_to_plot = [human_scores, llm_scores]
    labels = ['Human Reviewers', 'LLM Reviewers']

    bp = ax.boxplot(data_to_plot, labels=labels, patch_artist=True,
                    widths=0.6, showmeans=True, meanline=True)

    # Color boxes
    colors = ['#36A2EB', '#FF6384']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    # Add statistical annotations
    human_mean = human_scores.mean()
    llm_mean = llm_scores.mean()
    human_std = human_scores.std()
    llm_std = llm_scores.std()

    ax.text(1, human_mean + human_std + 3,
            f'Mean: {human_mean:.1f}\nSD: {human_std:.1f}\nn={len(human_scores)}',
            ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.text(2, llm_mean + llm_std + 3,
            f'Mean: {llm_mean:.1f}\nSD: {llm_std:.1f}\nn={len(llm_scores)}',
            ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    # Perform t-test
    t_stat, p_value = stats.ttest_ind(human_scores, llm_scores)
    ax.text(1.5, ax.get_ylim()[1] * 0.95,
            f'Two-sample t-test: t={t_stat:.2f}, p={p_value:.4f}',
            ha='center', fontsize=10, style='italic')

    ax.set_ylabel('Total Score (out of 100)', fontsize=12, fontweight='bold')
    ax.set_title('Human vs. LLM Overall Review Scores', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / 'slide5_human_vs_llm_overall.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated slide5_human_vs_llm_overall.png")

def slide6_criteria_comparison(df):
    """Radar chart comparing human vs. LLM by criteria"""
    criteria_cols = [
        'innovation_impact', 'methodological_approach', 'research_team_strength',
        'external_funding_potential', 'budget_clarity', 'presentation_quality'
    ]

    criteria_labels = [
        'Innovation &\nImpact', 'Methodology &\nFeasibility', 'Team\nStrength',
        'External\nFunding', 'Budget\nClarity', 'Presentation\nQuality'
    ]

    # Calculate means
    human_means = df[df['reviewer_type'] == 'Human'][criteria_cols].mean()
    llm_means = df[df['reviewer_type'] == 'LLM'][criteria_cols].mean()

    # Normalize to percentage of max possible score
    max_scores = [30, 30, 10, 10, 10, 10]
    human_pct = [(human_means[i] / max_scores[i]) * 100 for i in range(len(criteria_cols))]
    llm_pct = [(llm_means[i] / max_scores[i]) * 100 for i in range(len(criteria_cols))]

    # Create radar chart
    angles = np.linspace(0, 2 * np.pi, len(criteria_labels), endpoint=False).tolist()
    human_pct += human_pct[:1]  # Complete the circle
    llm_pct += llm_pct[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))

    ax.plot(angles, human_pct, 'o-', linewidth=2, label='Human Reviewers', color='#36A2EB')
    ax.fill(angles, human_pct, alpha=0.25, color='#36A2EB')

    ax.plot(angles, llm_pct, 's-', linewidth=2, label='LLM Reviewers', color='#FF6384')
    ax.fill(angles, llm_pct, alpha=0.25, color='#FF6384')

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(criteria_labels, size=11)
    ax.set_ylim(0, 100)
    ax.set_yticks([20, 40, 60, 80, 100])
    ax.set_yticklabels(['20%', '40%', '60%', '80%', '100%'])
    ax.grid(True)

    ax.set_title('Performance by Evaluation Criteria\n(% of Maximum Possible Score)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / 'slide6_criteria_comparison.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated slide6_criteria_comparison.png")

def slide7_experiment_comparison(df):
    """Bar chart comparing experiments"""
    experiment_order = ['baseline_v1', 'with_training_data_v1', 'multi_examples_v1', 'strict_scoring_v1']

    # Calculate average scores per experiment (excluding Daniel where needed)
    experiment_scores = []
    experiment_labels = []
    experiment_ns = []

    for exp in experiment_order:
        exp_df = filter_for_experiment(df, exp)
        exp_llm = exp_df[exp_df['reviewer_type'] == 'LLM']
        if len(exp_llm) > 0:
            experiment_scores.append(exp_llm['total_score'].mean())
            experiment_labels.append(exp.replace('_', '\n'))
            experiment_ns.append(len(exp_llm))

    # Get human baseline for comparison
    human_mean = df[df['reviewer_type'] == 'Human']['total_score'].mean()

    fig, ax = plt.subplots(figsize=(12, 7))

    colors = ['#36A2EB', '#FF6384', '#FFCE56', '#4BC0C0']
    bars = ax.bar(experiment_labels, experiment_scores, color=colors, alpha=0.8, edgecolor='black')

    # Add horizontal line for human mean
    ax.axhline(y=human_mean, color='green', linestyle='--', linewidth=2,
               label=f'Human Mean ({human_mean:.1f})')

    # Add value labels on bars
    for i, (bar, score, n) in enumerate(zip(bars, experiment_scores, experiment_ns)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{score:.1f}\n(n={n})',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.set_ylabel('Average Total Score (out of 100)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Experiment Condition', fontsize=12, fontweight='bold')
    ax.set_title('Impact of Prompt Engineering on LLM Performance', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / 'slide7_experiment_comparison.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated slide7_experiment_comparison.png")

def slide8_model_comparison(df):
    """Grouped bar chart comparing vendors"""
    criteria_cols = [
        'innovation_impact', 'methodological_approach', 'research_team_strength',
        'external_funding_potential', 'budget_clarity', 'presentation_quality'
    ]

    criteria_labels = [
        'Innovation', 'Methodology', 'Team', 'Funding', 'Budget', 'Presentation'
    ]

    # Get unique vendors
    vendors = df[df['reviewer_type'] == 'LLM']['vendor'].dropna().unique()

    # Calculate means per vendor
    vendor_data = {}
    for vendor in vendors:
        vendor_df = df[(df['reviewer_type'] == 'LLM') & (df['vendor'] == vendor)]
        if len(vendor_df) > 0:
            vendor_data[vendor] = vendor_df[criteria_cols].mean().values

    # Also add human data
    human_df = df[df['reviewer_type'] == 'Human']
    vendor_data['Human'] = human_df[criteria_cols].mean().values

    # Create grouped bar chart
    fig, ax = plt.subplots(figsize=(14, 7))

    x = np.arange(len(criteria_labels))
    width = 0.15
    multiplier = 0

    colors_map = {'Human': '#2E7D32', 'OpenAI': '#FF6B6B', 'Google': '#4ECDC4',
                  'xAI': '#FFE66D', 'Anthropic': '#A8DADC'}

    for vendor, scores in vendor_data.items():
        offset = width * multiplier
        color = colors_map.get(vendor, f'C{multiplier}')
        bars = ax.bar(x + offset, scores, width, label=vendor, color=color, alpha=0.8)
        multiplier += 1

    ax.set_ylabel('Average Score', fontsize=12, fontweight='bold')
    ax.set_xlabel('Evaluation Criteria', fontsize=12, fontweight='bold')
    ax.set_title('Model Performance Comparison Across Criteria', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x + width * 2)
    ax.set_xticklabels(criteria_labels, rotation=0)
    ax.legend(loc='upper right', ncol=len(vendor_data), fontsize=10)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / 'slide8_model_comparison.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated slide8_model_comparison.png")

def slide9_agreement_analysis(df):
    """Correlation and agreement plots"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Left plot: Human vs LLM correlation
    human_by_applicant = df[df['reviewer_type'] == 'Human'].groupby('applicant_name')['total_score'].mean()
    llm_by_applicant = df[df['reviewer_type'] == 'LLM'].groupby('applicant_name')['total_score'].mean()

    # Match applicants
    common_applicants = sorted(list(set(human_by_applicant.index) & set(llm_by_applicant.index)))
    human_scores_matched = [human_by_applicant[app] for app in common_applicants]
    llm_scores_matched = [llm_by_applicant[app] for app in common_applicants]

    # Create anonymized labels (S1, S2, S3, S4)
    applicant_labels = {app: f'S{i+1}' for i, app in enumerate(common_applicants)}

    axes[0].scatter(human_scores_matched, llm_scores_matched, s=150, alpha=0.7,
                    color='#FF6384', edgecolors='black', linewidth=1.5)

    # Add anonymized labels for each point
    for i, app in enumerate(common_applicants):
        axes[0].annotate(applicant_labels[app], (human_scores_matched[i], llm_scores_matched[i]),
                        xytext=(5, 5), textcoords='offset points', fontsize=10, fontweight='bold')

    # Add diagonal line
    min_val = min(min(human_scores_matched), min(llm_scores_matched))
    max_val = max(max(human_scores_matched), max(llm_scores_matched))
    axes[0].plot([min_val, max_val], [min_val, max_val], 'k--', alpha=0.5, linewidth=1)

    # Calculate correlation
    if len(human_scores_matched) > 2:
        corr, p_val = stats.pearsonr(human_scores_matched, llm_scores_matched)
        axes[0].text(0.05, 0.95, f'r = {corr:.3f}\np = {p_val:.4f}',
                    transform=axes[0].transAxes, fontsize=11,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    axes[0].set_xlabel('Human Mean Score', fontsize=12, fontweight='bold')
    axes[0].set_ylabel('LLM Mean Score', fontsize=12, fontweight='bold')
    axes[0].set_title('Human-LLM Score Correlation\n(by Applicant)', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3)

    # Right plot: Variance comparison
    human_std_by_applicant = df[df['reviewer_type'] == 'Human'].groupby('applicant_name')['total_score'].std()
    llm_std_by_applicant = df[df['reviewer_type'] == 'LLM'].groupby('applicant_name')['total_score'].std()

    applicants = sorted(list(set(human_std_by_applicant.index) & set(llm_std_by_applicant.index)))
    x_pos = np.arange(len(applicants))
    width = 0.35

    # Create anonymized labels (S1, S2, S3, S4) - must match left plot
    applicant_labels_right = {app: f'S{i+1}' for i, app in enumerate(applicants)}
    anonymous_labels = [applicant_labels_right[app] for app in applicants]

    human_stds = [human_std_by_applicant.get(app, 0) for app in applicants]
    llm_stds = [llm_std_by_applicant.get(app, 0) for app in applicants]

    axes[1].bar(x_pos - width/2, human_stds, width, label='Human',
                color='#36A2EB', alpha=0.8)
    axes[1].bar(x_pos + width/2, llm_stds, width, label='LLM',
                color='#FF6384', alpha=0.8)

    axes[1].set_xlabel('Applicant', fontsize=12, fontweight='bold')
    axes[1].set_ylabel('Standard Deviation', fontsize=12, fontweight='bold')
    axes[1].set_title('Inter-Rater Variability\n(by Applicant)', fontsize=12, fontweight='bold')
    axes[1].set_xticks(x_pos)
    axes[1].set_xticklabels(anonymous_labels, rotation=0)  # Changed to horizontal
    axes[1].legend(fontsize=11)
    axes[1].grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / 'slide9_agreement_analysis.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated slide9_agreement_analysis.png")

def main():
    """Generate all presentation figures"""
    print("\nGenerating presentation figures...")
    print("=" * 60)

    # Load data
    print("\nLoading data from database...")
    df = load_data()
    print(f"Loaded {len(df)} reviews")
    print(f"  - Human reviews: {len(df[df['reviewer_type'] == 'Human'])}")
    print(f"  - LLM reviews: {len(df[df['reviewer_type'] == 'LLM'])}")

    # Generate figures
    print("\nGenerating figures...")
    slide2_problem_statement()
    slide3_study_design()
    slide4_experiment_conditions()
    slide5_human_vs_llm_overall(df)
    slide6_criteria_comparison(df)
    slide7_experiment_comparison(df)
    slide8_model_comparison(df)
    slide9_agreement_analysis(df)

    print("\n" + "=" * 60)
    print("✓ All figures generated successfully!")
    print(f"Output location: {OUTPUT_PATH}")
    print("\nGenerated figures:")
    for i in range(2, 10):
        print(f"  - slide{i}_*.png")

if __name__ == "__main__":
    main()
