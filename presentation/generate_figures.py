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
            f'Mean: {human_mean:.1f}\nSD: {human_std:.1f}',
            ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    ax.text(2, llm_mean + llm_std + 3,
            f'Mean: {llm_mean:.1f}\nSD: {llm_std:.1f}',
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
                f'{score:.1f})',
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

def simple_consistency_comparison(df):
    """Simple bar chart showing standard deviation: Human vs AI"""
    fig, ax = plt.subplots(figsize=(10, 7))

    # Calculate standard deviations
    human_std = df[df['reviewer_type'] == 'Human']['total_score'].std()
    llm_std = df[df['reviewer_type'] == 'LLM']['total_score'].std()

    # Create data
    categories = ['Human\nReviewers', 'AI\nReviewers']
    std_values = [human_std, llm_std]
    colors = ['#36A2EB', '#FF6384']

    # Create bars
    bars = ax.bar(categories, std_values, color=colors, alpha=0.85,
                  edgecolor='black', linewidth=2.5, width=0.5)

    # Add value labels
    for bar, val in zip(bars, std_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.4,
                f'{val:.1f}\npoints',
                ha='center', va='bottom', fontsize=16, fontweight='bold')

    # Calculate improvement
    pct_improvement = ((human_std - llm_std) / human_std) * 100

    # Add arrow showing improvement
    ax.annotate('', xy=(1, llm_std), xytext=(1, human_std),
                arrowprops=dict(arrowstyle='<->', color='green', lw=3))
    ax.text(1.25, (human_std + llm_std) / 2,
            f'{pct_improvement:.0f}%\nmore\nconsistent',
            fontsize=14, fontweight='bold', color='green', va='center')

    # Customize plot
    ax.set_ylabel('Variability (Standard Deviation)', fontsize=14, fontweight='bold')
    ax.set_title('AI Reviews Are More Consistent Than Human Reviews',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, max(std_values) * 1.35)
    ax.grid(axis='y', alpha=0.3)

    # Add explanatory text
    ax.text(0.5, 0.95, 'Lower is better = More consistent across reviewers',
            transform=ax.transAxes, ha='center', fontsize=12, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / 'simple_consistency_comparison.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated simple_consistency_comparison.png")

def llm_model_consistency_comparison(df):
    """Compare consistency across different LLM vendors"""
    fig, ax = plt.subplots(figsize=(12, 7))

    # Get unique vendors
    llm_df = df[df['reviewer_type'] == 'LLM']
    vendors = sorted(llm_df['vendor'].dropna().unique())

    # Calculate std for each vendor
    vendor_stds = {}
    for vendor in vendors:
        vendor_scores = llm_df[llm_df['vendor'] == vendor]['total_score'].dropna()
        if len(vendor_scores) > 1:
            vendor_stds[vendor] = vendor_scores.std()

    # Add human for comparison
    human_std = df[df['reviewer_type'] == 'Human']['total_score'].std()

    # Prepare data
    all_labels = ['Human'] + list(vendor_stds.keys())
    all_values = [human_std] + list(vendor_stds.values())

    # Color scheme: human is blue, best LLM is green, others are shades
    colors_map = {
        'Human': '#36A2EB',
        'OpenAI': '#FF6B6B',
        'Google': '#4ECDC4',
        'xAI': '#4CAF50',  # Green for best
        'Anthropic': '#A8DADC'
    }
    colors = [colors_map.get(label, '#CCCCCC') for label in all_labels]

    # Create bars
    bars = ax.bar(all_labels, all_values, color=colors, alpha=0.85,
                  edgecolor='black', linewidth=2, width=0.6)

    # Add value labels
    for bar, val in zip(bars, all_values):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                f'{val:.1f}',
                ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Highlight the best LLM
    best_llm = min(vendor_stds.items(), key=lambda x: x[1])
    best_idx = all_labels.index(best_llm[0])
    bars[best_idx].set_edgecolor('green')
    bars[best_idx].set_linewidth(4)

    # Add annotation for best
    ax.text(best_idx, best_llm[1] + 1.5, '★ Most Consistent',
            ha='center', fontsize=11, fontweight='bold', color='green')

    # Customize plot
    ax.set_ylabel('Variability (Standard Deviation)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Reviewer Type / AI Model', fontsize=13, fontweight='bold')
    ax.set_title('Consistency Comparison: Human vs. Different AI Models',
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_ylim(0, max(all_values) * 1.25)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / 'llm_model_consistency_comparison.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated llm_model_consistency_comparison.png")

def grok_alignment_superiority(df):
    """Show Grok's superior alignment with human reviewers"""
    fig, ax = plt.subplots(figsize=(12, 7))

    # Calculate mean scores
    human_mean = df[df['reviewer_type'] == 'Human']['total_score'].mean()

    # Get vendor means
    llm_df = df[df['reviewer_type'] == 'LLM']
    vendors = sorted(llm_df['vendor'].dropna().unique())

    vendor_means = {}
    vendor_diffs = {}
    for vendor in vendors:
        vendor_scores = llm_df[llm_df['vendor'] == vendor]['total_score'].dropna()
        if len(vendor_scores) > 0:
            vendor_mean = vendor_scores.mean()
            vendor_means[vendor] = vendor_mean
            vendor_diffs[vendor] = abs(vendor_mean - human_mean)

    # Sort by alignment (smallest difference first)
    sorted_vendors = sorted(vendor_diffs.items(), key=lambda x: x[1])

    # Prepare data
    labels = [v[0] for v in sorted_vendors]
    differences = [v[1] for v in sorted_vendors]

    # Color scheme: best is green, others fade
    colors = ['#4CAF50' if i == 0 else '#FF6B6B' for i in range(len(labels))]

    # Create horizontal bars
    bars = ax.barh(labels, differences, color=colors, alpha=0.85,
                   edgecolor='black', linewidth=2, height=0.6)

    # Highlight best with thicker border
    bars[0].set_edgecolor('green')
    bars[0].set_linewidth(4)

    # Add value labels
    for i, (bar, val) in enumerate(zip(bars, differences)):
        width = bar.get_width()
        ax.text(width + 0.15, bar.get_y() + bar.get_height()/2.,
                f'{val:.2f} pts',
                ha='left', va='center', fontsize=13, fontweight='bold')

    # Add "BEST" label
    # ax.text(differences[0] + 0.15, 0, '   ← BEST',
    #         va='center', fontsize=12, fontweight='bold', color='green')

    # Add reference line at 0
    ax.axvline(x=0, color='gray', linestyle='--', linewidth=1.5, alpha=0.5)

    # Customize plot
    ax.set_xlabel('Difference from Human Average Score (points)', fontsize=13, fontweight='bold')
    ax.set_ylabel('AI Model', fontsize=13, fontweight='bold')
    ax.set_title(f'Which AI Model Best Matches Human Reviewers?\n(Human Average: {human_mean:.1f} points)',
                 fontsize=15, fontweight='bold', pad=20)
    ax.set_xlim(0, max(differences) * 1.3)
    ax.grid(axis='x', alpha=0.3)
    ax.invert_yaxis()  # Best at top

    # Add explanatory note
    note_text = f'{labels[0]} is closest to human average (only {differences[0]:.2f} points away)'
    ax.text(0.98, 0.02, note_text,
            transform=ax.transAxes, ha='right', va='bottom',
            fontsize=11, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / 'grok_alignment_superiority.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated grok_alignment_superiority.png")

def slide_consistency_comparison(df):
    """Simple visualization showing consistency difference between human and AI"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Get human and LLM scores
    human_scores = df[df['reviewer_type'] == 'Human']['total_score'].dropna()
    llm_scores = df[df['reviewer_type'] == 'LLM']['total_score'].dropna()

    # Calculate standard deviations
    human_std = human_scores.std()
    llm_std = llm_scores.std()

    # Left plot: Violin plots showing distribution spread
    parts1 = axes[0].violinplot([human_scores], positions=[0], widths=0.7,
                                 showmeans=True, showmedians=True)
    parts2 = axes[0].violinplot([llm_scores], positions=[1], widths=0.7,
                                 showmeans=True, showmedians=True)

    # Color the violin plots
    for pc in parts1['bodies']:
        pc.set_facecolor('#36A2EB')
        pc.set_alpha(0.7)
    for pc in parts2['bodies']:
        pc.set_facecolor('#FF6384')
        pc.set_alpha(0.7)

    # Customize left plot
    axes[0].set_xticks([0, 1])
    axes[0].set_xticklabels(['Human\nReviewers', 'AI\nReviewers'], fontsize=12)
    axes[0].set_ylabel('Total Score (out of 100)', fontsize=12, fontweight='bold')
    axes[0].set_title('Score Distribution Comparison', fontsize=14, fontweight='bold')
    axes[0].set_ylim(50, 105)
    axes[0].grid(axis='y', alpha=0.3)

    # Add annotation showing spread
    axes[0].text(0, 105, f'Variation:\n±{human_std:.1f} pts',
                ha='center', va='top', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='#36A2EB', linewidth=2))
    axes[0].text(1, 105, f'Variation:\n±{llm_std:.1f} pts',
                ha='center', va='top', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', edgecolor='#FF6384', linewidth=2))

    # Right plot: Bar chart comparing variability
    categories = ['Human\nReviewers', 'AI\nReviewers']
    variability = [human_std, llm_std]
    colors = ['#36A2EB', '#FF6384']

    bars = axes[1].bar(categories, variability, color=colors, alpha=0.8,
                       edgecolor='black', linewidth=2, width=0.6)

    # Add value labels on bars
    for bar, val in zip(bars, variability):
        height = bar.get_height()
        axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.3,
                    f'{val:.1f}\npoints',
                    ha='center', va='bottom', fontsize=12, fontweight='bold')

    # Calculate percentage difference
    pct_improvement = ((human_std - llm_std) / human_std) * 100

    # Add improvement annotation
    axes[1].annotate('', xy=(1, llm_std), xytext=(1, human_std),
                    arrowprops=dict(arrowstyle='<->', color='green', lw=2))
    axes[1].text(1.15, (human_std + llm_std) / 2,
                f'{pct_improvement:.0f}%\nmore\nconsistent',
                fontsize=11, fontweight='bold', color='green',
                va='center')

    axes[1].set_ylabel('Variability (Standard Deviation)', fontsize=12, fontweight='bold')
    axes[1].set_title('AI Reviews are More Consistent', fontsize=14, fontweight='bold')
    axes[1].set_ylim(0, max(variability) * 1.3)
    axes[1].grid(axis='y', alpha=0.3)

    # Add summary text
    fig.text(0.5, 0.02,
            f'Lower variability = More consistent scores across different reviewers\n'
            f'Human reviewers varied by {human_std:.1f} points • AI reviewers varied by {llm_std:.1f} points',
            ha='center', fontsize=11, style='italic',
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.tight_layout(rect=[0, 0.08, 1, 1])
    plt.savefig(OUTPUT_PATH / 'slide_consistency_comparison.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated slide_consistency_comparison.png")

def slide9_recommendation_frequencies(df):
    """Bar chart showing recommendation frequency distributions"""
    fig, ax = plt.subplots(figsize=(12, 7))

    # Get recommendation counts
    human_recs = df[df['reviewer_type'] == 'Human']['overall_recommendation'].value_counts()
    llm_recs = df[df['reviewer_type'] == 'LLM']['overall_recommendation'].value_counts()

    # Define standard categories (ensure consistent ordering)
    categories = ['Fund', 'Do Not Fund', 'Fund with Revisions']

    # Get counts for each category (default to 0 if not present)
    human_counts = [human_recs.get(cat, 0) for cat in categories]
    llm_counts = [llm_recs.get(cat, 0) for cat in categories]

    # Calculate percentages
    human_total = sum(human_counts)
    llm_total = sum(llm_counts)
    human_pcts = [(count / human_total * 100) if human_total > 0 else 0 for count in human_counts]
    llm_pcts = [(count / llm_total * 100) if llm_total > 0 else 0 for count in llm_counts]

    # Set up bar positions
    x = np.arange(len(categories))
    width = 0.35

    # Create bars
    bars1 = ax.bar(x - width/2, human_counts, width, label='Human Reviewers',
                   color='#36A2EB', alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x + width/2, llm_counts, width, label='LLM Reviewers',
                   color='#FF6384', alpha=0.8, edgecolor='black', linewidth=1.5)

    # Add value labels on bars (count and percentage)
    for i, (bar, count, pct) in enumerate(zip(bars1, human_counts, human_pcts)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{count}\n({pct:.1f}%)',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    for i, (bar, count, pct) in enumerate(zip(bars2, llm_counts, llm_pcts)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{count}\n({pct:.1f}%)',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Customize plot
    ax.set_xlabel('Funding Recommendation', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency (Count)', fontsize=12, fontweight='bold')
    ax.set_title('Funding Recommendation Distribution:\nHuman vs. LLM Reviewers',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11)
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(axis='y', alpha=0.3)

    ## move legend outside the plot to the bottom
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=12)

    plt.tight_layout()

    # Add summary text box below the plot
    agreement_text = (f'Human (n={human_total}): '
                     f'{human_pcts[0]:.1f}% Fund, '
                     f'{human_pcts[1]:.1f}% Do Not Fund, '
                     f'{human_pcts[2]:.1f}% Revisions\n'
                     f'LLM (n={llm_total}): '
                     f'{llm_pcts[0]:.1f}% Fund, '
                     f'{llm_pcts[1]:.1f}% Do Not Fund, '
                     f'{llm_pcts[2]:.1f}% Revisions')

    fig.text(0.5, -0.05, agreement_text,
            ha='center', va='top', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    plt.savefig(OUTPUT_PATH / 'slide9_recommendation_frequencies.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated slide9_recommendation_frequencies.png")

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

    ## move legend outside the plot to the bottom
    axes[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=2, fontsize=11)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / 'slide9_agreement_analysis.png', bbox_inches='tight')
    plt.close()
    print("✓ Generated slide9_agreement_analysis.png")

def experiment_human_vs_llm_comparison(df, experiment_name, experiment_label, filename_prefix):
    """Box plot comparing human vs LLM for a specific experiment"""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Filter data for this experiment
    exp_df = filter_for_experiment(df, experiment_name)

    # Prepare data
    human_scores = exp_df[exp_df['reviewer_type'] == 'Human']['total_score'].dropna()
    llm_scores = exp_df[exp_df['reviewer_type'] == 'LLM']['total_score'].dropna()

    if len(llm_scores) == 0:
        print(f"⚠ No LLM data for {experiment_label}, skipping figure")
        return

    data_to_plot = [human_scores, llm_scores]
    labels = ['Human Reviewers', f'LLM Reviewers\n({experiment_label})']

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
    if len(llm_scores) > 1 and len(human_scores) > 1:
        t_stat, p_value = stats.ttest_ind(human_scores, llm_scores)
        ax.text(1.5, ax.get_ylim()[1] * 0.95,
                f't={t_stat:.2f}, p={p_value:.4f}\nΔ={llm_mean - human_mean:+.2f} pts',
                ha='center', fontsize=10, style='italic',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

    ax.set_ylabel('Total Score (out of 100)', fontsize=12, fontweight='bold')
    ax.set_title(f'{experiment_label}\nHuman vs. LLM Scores', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / f'{filename_prefix}_human_vs_llm.png', bbox_inches='tight')
    plt.close()
    print(f"✓ Generated {filename_prefix}_human_vs_llm.png")

def experiment_criteria_radar(df, experiment_name, experiment_label, filename_prefix):
    """Radar chart for a specific experiment"""
    exp_df = filter_for_experiment(df, experiment_name)

    criteria_cols = [
        'innovation_impact', 'methodological_approach', 'research_team_strength',
        'external_funding_potential', 'budget_clarity', 'presentation_quality'
    ]

    criteria_labels = [
        'Innovation &\nImpact', 'Methodology &\nFeasibility', 'Team\nStrength',
        'External\nFunding', 'Budget\nClarity', 'Presentation\nQuality'
    ]

    # Calculate means
    human_means = exp_df[exp_df['reviewer_type'] == 'Human'][criteria_cols].mean()
    llm_means = exp_df[exp_df['reviewer_type'] == 'LLM'][criteria_cols].mean()

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

    ax.set_title(f'{experiment_label}\nPerformance by Criteria (% of Max Score)',
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / f'{filename_prefix}_criteria_radar.png', bbox_inches='tight')
    plt.close()
    print(f"✓ Generated {filename_prefix}_criteria_radar.png")

def experiment_model_comparison(df, experiment_name, experiment_label, filename_prefix):
    """Bar chart comparing models within an experiment"""
    exp_df = filter_for_experiment(df, experiment_name)
    llm_df = exp_df[exp_df['reviewer_type'] == 'LLM']

    vendors = sorted(llm_df['vendor'].dropna().unique())

    if len(vendors) == 0:
        print(f"⚠ No vendor data for {experiment_label}, skipping figure")
        return

    human_mean = exp_df[exp_df['reviewer_type'] == 'Human']['total_score'].mean()

    fig, ax = plt.subplots(figsize=(10, 7))

    vendor_means = []
    vendor_stds = []
    vendor_ns = []

    for vendor in vendors:
        vendor_scores = llm_df[llm_df['vendor'] == vendor]['total_score'].dropna()
        if len(vendor_scores) > 0:
            vendor_means.append(vendor_scores.mean())
            vendor_stds.append(vendor_scores.std())
            vendor_ns.append(len(vendor_scores))

    colors_map = {'OpenAI': '#FF6B6B', 'Google': '#4ECDC4', 'xAI': '#FFE66D', 'Anthropic': '#A8DADC'}
    colors = [colors_map.get(v, '#CCCCCC') for v in vendors]

    bars = ax.bar(vendors, vendor_means, color=colors, alpha=0.8, edgecolor='black', linewidth=2)

    # Add error bars
    ax.errorbar(vendors, vendor_means, yerr=vendor_stds, fmt='none', ecolor='black', capsize=5, linewidth=1.5)

    # Add horizontal line for human mean
    ax.axhline(y=human_mean, color='green', linestyle='--', linewidth=2,
               label=f'Human Mean ({human_mean:.1f})')

    # Add value labels on bars
    for bar, mean, std, n in zip(bars, vendor_means, vendor_stds, vendor_ns):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + std + 1,
                f'{mean:.1f}\n(n={n})',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_ylabel('Average Total Score (out of 100)', fontsize=12, fontweight='bold')
    ax.set_xlabel('AI Model Vendor', fontsize=12, fontweight='bold')
    ax.set_title(f'{experiment_label}\nModel Performance Comparison', fontsize=14, fontweight='bold', pad=20)
    ax.set_ylim(0, 100)
    ax.legend(fontsize=11, loc='upper right')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / f'{filename_prefix}_model_comparison.png', bbox_inches='tight')
    plt.close()
    print(f"✓ Generated {filename_prefix}_model_comparison.png")

def experiment_recommendations(df, experiment_name, experiment_label, filename_prefix):
    """Stacked bar chart showing recommendation distributions for an experiment"""
    exp_df = filter_for_experiment(df, experiment_name)

    fig, ax = plt.subplots(figsize=(10, 7))

    # Get recommendation counts
    human_recs = exp_df[exp_df['reviewer_type'] == 'Human']['overall_recommendation'].value_counts()
    llm_recs = exp_df[exp_df['reviewer_type'] == 'LLM']['overall_recommendation'].value_counts()

    # Define categories
    categories = ['Fund', 'Do Not Fund', 'Fund with Revisions']

    # Get counts
    human_counts = [human_recs.get(cat, 0) for cat in categories]
    llm_counts = [llm_recs.get(cat, 0) for cat in categories]

    # Calculate percentages
    human_total = sum(human_counts)
    llm_total = sum(llm_counts)
    human_pcts = [(c / human_total * 100) if human_total > 0 else 0 for c in human_counts]
    llm_pcts = [(c / llm_total * 100) if llm_total > 0 else 0 for c in llm_counts]

    # Set up positions
    x = np.arange(len(categories))
    width = 0.35

    # Create bars
    bars1 = ax.bar(x - width/2, human_counts, width, label='Human Reviewers',
                   color='#36A2EB', alpha=0.8, edgecolor='black', linewidth=1.5)
    bars2 = ax.bar(x + width/2, llm_counts, width, label='LLM Reviewers',
                   color='#FF6384', alpha=0.8, edgecolor='black', linewidth=1.5)

    # Add value labels
    for bars, counts, pcts in [(bars1, human_counts, human_pcts), (bars2, llm_counts, llm_pcts)]:
        for bar, count, pct in zip(bars, counts, pcts):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.3,
                    f'{count}\n({pct:.1f}%)',
                    ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_xlabel('Funding Recommendation', fontsize=12, fontweight='bold')
    ax.set_ylabel('Frequency (Count)', fontsize=12, fontweight='bold')
    ax.set_title(f'{experiment_label}\nRecommendation Distribution', fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11)
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / f'{filename_prefix}_recommendations.png', bbox_inches='tight')
    plt.close()
    print(f"✓ Generated {filename_prefix}_recommendations.png")

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

    # Generate general figures
    print("\nGenerating general figures...")
    slide2_problem_statement()
    slide3_study_design()
    slide4_experiment_conditions()
    slide5_human_vs_llm_overall(df)
    slide6_criteria_comparison(df)
    slide7_experiment_comparison(df)
    slide8_model_comparison(df)
    slide9_recommendation_frequencies(df)
    slide9_agreement_analysis(df)
    slide_consistency_comparison(df)

    # Additional simple/supplementary figures
    simple_consistency_comparison(df)
    llm_model_consistency_comparison(df)
    grok_alignment_superiority(df)

    # Generate per-experiment figures
    print("\n" + "=" * 60)
    print("Generating per-experiment figures...")
    print("=" * 60)

    experiments = [
        ('baseline_v1', 'Experiment 1: Baseline', 'exp1_baseline'),
        ('with_training_data_v1', 'Experiment 2: Single Example', 'exp2_single'),
        ('multi_examples_v1', 'Experiment 3: Multiple Examples', 'exp3_multi'),
        ('strict_scoring_v1', 'Experiment 4: Strict Scoring', 'exp4_strict')
    ]

    for exp_name, exp_label, exp_prefix in experiments:
        print(f"\nGenerating figures for {exp_label}...")
        experiment_human_vs_llm_comparison(df, exp_name, exp_label, exp_prefix)
        experiment_criteria_radar(df, exp_name, exp_label, exp_prefix)
        experiment_model_comparison(df, exp_name, exp_label, exp_prefix)
        experiment_recommendations(df, exp_name, exp_label, exp_prefix)

    print("\n" + "=" * 60)
    print("✓ All figures generated successfully!")
    print(f"Output location: {OUTPUT_PATH}")
    print("\nGenerated figures:")
    print("  General figures:")
    for i in range(2, 10):
        print(f"    - slide{i}_*.png")
    print(f"    - slide9_recommendation_frequencies.png")
    print(f"    - slide_consistency_comparison.png")
    print(f"\n  Supplementary/Simple figures:")
    print(f"    - simple_consistency_comparison.png")
    print(f"    - llm_model_consistency_comparison.png")
    print(f"    - grok_alignment_superiority.png")
    print(f"\n  Per-experiment figures:")
    for _, exp_label, exp_prefix in experiments:
        print(f"    - {exp_prefix}_*.png (4 figures per experiment)")

if __name__ == "__main__":
    main()
