#!/usr/bin/env python3
"""
Generate statistical analyses for manuscript - Version 2 (3 Experiments)

This script performs comprehensive statistical analyses for the 3 experiments,
properly handling the different human and LLM review inclusion/exclusion criteria.

Experiment Details:
- Experiment 1 (baseline_v1): 12 human reviews + 27 AI reviews (no exclusions)
- Experiment 3 (multi_examples_v1): 8 human reviews + 18 AI reviews (DANIEL completely excluded - used as training)
- Experiment 4 (strict_scoring_v1): 8 human reviews + 18 AI reviews (DANIEL completely excluded - used as training)

Note: Experiment 2 (with_training_data_v1) has been removed from this analysis.
"""

import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set style for plots
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 10

# Define paths
BASE_PATH = Path(__file__).parent.parent.parent
DB_PATH = BASE_PATH / "data" / "results.db"
OUTPUT_PATH = Path(__file__).parent / "output_v2"
OUTPUT_PATH.mkdir(exist_ok=True)

# Experiment definitions (3 experiments only)
EXPERIMENTS = {
    'baseline_v1': {
        'name': 'Experiment 1: Zero Shot',
        'short_name': 'Exp1_ZeroShot',
        'description': 'Baseline performance with no training examples',
        'exclude_daniel_complete': False
    },
    'multi_examples_v1': {
        'name': 'Experiment 3: Few Shot',
        'short_name': 'Exp3_FewShot',
        'description': 'Multiple training examples using DANIEL data (DANIEL excluded from analysis)',
        'exclude_daniel_complete': True
    },
    'strict_scoring_v1': {
        'name': 'Experiment 4: Stricter Prompt',
        'short_name': 'Exp4_Stricter',
        'description': 'Stricter prompt with DANIEL training data (DANIEL excluded from analysis)',
        'exclude_daniel_complete': True
    }
}

CRITERIA_DEFINITIONS = {
    'innovation_impact': {'label': 'Innovation & Impact', 'max': 30},
    'methodological_approach': {'label': 'Methodology & Feasibility', 'max': 30},
    'research_team_strength': {'label': 'Team Strength', 'max': 10},
    'external_funding_potential': {'label': 'External Funding Potential', 'max': 10},
    'budget_clarity': {'label': 'Budget Clarity', 'max': 10},
    'presentation_quality': {'label': 'Presentation Quality', 'max': 10}
}

def load_data():
    """Load data from database"""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM combined_reviews ORDER BY applicant_name, reviewer_type, reviewer_id"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def filter_for_experiment(df, experiment_key):
    """
    Filter data for specific experiment with proper human and LLM review exclusions

    Args:
        df: Full dataframe
        experiment_key: Key from EXPERIMENTS dict

    Returns:
        Filtered dataframe with appropriate human and LLM reviews
    """
    exp_config = EXPERIMENTS[experiment_key]

    # Start with LLM reviews for this experiment
    llm_reviews = df[(df['reviewer_type'] == 'LLM') &
                     (df['prompt_experiment_name'] == experiment_key)].copy()

    # Get human reviews
    human_reviews = df[df['reviewer_type'] == 'Human'].copy()

    # Apply exclusions based on experiment
    if exp_config['exclude_daniel_complete']:
        # Exclude all reviews of DANIEL (both human and LLM) - Exp 3 & 4
        human_reviews = human_reviews[human_reviews['applicant_name'] != 'DANIEL']
        llm_reviews = llm_reviews[llm_reviews['applicant_name'] != 'DANIEL']

    # Combine and return
    result = pd.concat([human_reviews, llm_reviews], ignore_index=True)
    return result

def analyze_experiment_overall(df_exp, experiment_key):
    """Analyze overall performance for an experiment"""
    results = {}

    human = df_exp[df_exp['reviewer_type'] == 'Human']['total_score'].dropna()
    llm = df_exp[df_exp['reviewer_type'] == 'LLM']['total_score'].dropna()

    results['human'] = {
        'n': len(human),
        'mean': human.mean(),
        'std': human.std(),
        'median': human.median(),
        'min': human.min(),
        'max': human.max(),
        'q25': human.quantile(0.25),
        'q75': human.quantile(0.75)
    }

    results['llm'] = {
        'n': len(llm),
        'mean': llm.mean(),
        'std': llm.std(),
        'median': llm.median(),
        'min': llm.min(),
        'max': llm.max(),
        'q25': llm.quantile(0.25),
        'q75': llm.quantile(0.75)
    }

    # Statistical tests
    if len(human) > 1 and len(llm) > 1:
        t_stat, p_value = stats.ttest_ind(human, llm)
        cohens_d = (llm.mean() - human.mean()) / np.sqrt((human.std()**2 + llm.std()**2) / 2)

        results['statistics'] = {
            'difference': llm.mean() - human.mean(),
            't_statistic': t_stat,
            'p_value': p_value,
            'cohens_d': cohens_d,
            'significant': p_value < 0.05
        }

    return results

def analyze_experiment_criteria(df_exp, experiment_key):
    """Analyze performance by criteria for an experiment"""
    results = {}

    for criterion, definition in CRITERIA_DEFINITIONS.items():
        human_scores = df_exp[df_exp['reviewer_type'] == 'Human'][criterion].dropna()
        llm_scores = df_exp[df_exp['reviewer_type'] == 'LLM'][criterion].dropna()

        if len(human_scores) > 0 and len(llm_scores) > 0:
            human_mean = human_scores.mean()
            llm_mean = llm_scores.mean()
            max_score = definition['max']

            results[criterion] = {
                'label': definition['label'],
                'max_score': max_score,
                'human_mean': human_mean,
                'human_pct': (human_mean / max_score) * 100,
                'llm_mean': llm_mean,
                'llm_pct': (llm_mean / max_score) * 100,
                'difference': llm_mean - human_mean,
                'difference_pct': ((llm_mean - human_mean) / max_score) * 100
            }

            if len(human_scores) > 1 and len(llm_scores) > 1:
                t_stat, p_value = stats.ttest_ind(human_scores, llm_scores)
                results[criterion]['t_statistic'] = t_stat
                results[criterion]['p_value'] = p_value
                results[criterion]['significant'] = p_value < 0.05

    return results

def analyze_experiment_models(df_exp, experiment_key):
    """Analyze performance by LLM model/vendor"""
    results = {}

    llm_df = df_exp[df_exp['reviewer_type'] == 'LLM']
    human_mean = df_exp[df_exp['reviewer_type'] == 'Human']['total_score'].mean()

    vendors = llm_df['vendor'].dropna().unique()

    for vendor in sorted(vendors):
        vendor_scores = llm_df[llm_df['vendor'] == vendor]['total_score'].dropna()

        if len(vendor_scores) > 0:
            results[vendor] = {
                'n': len(vendor_scores),
                'mean': vendor_scores.mean(),
                'std': vendor_scores.std(),
                'median': vendor_scores.median(),
                'diff_from_human': vendor_scores.mean() - human_mean,
                'abs_diff_from_human': abs(vendor_scores.mean() - human_mean)
            }

    return results

def analyze_experiment_recommendations(df_exp, experiment_key):
    """Analyze recommendation distributions"""
    results = {}

    human_recs = df_exp[df_exp['reviewer_type'] == 'Human']['overall_recommendation'].value_counts()
    llm_recs = df_exp[df_exp['reviewer_type'] == 'LLM']['overall_recommendation'].value_counts()

    total_human = len(df_exp[df_exp['reviewer_type'] == 'Human'])
    total_llm = len(df_exp[df_exp['reviewer_type'] == 'LLM'])

    results['human'] = {
        rec: {'count': int(count), 'percentage': (count / total_human) * 100}
        for rec, count in human_recs.items()
    }

    results['llm'] = {
        rec: {'count': int(count), 'percentage': (count / total_llm) * 100}
        for rec, count in llm_recs.items()
    }

    # Agreement by applicant - Exact match
    applicants = df_exp['applicant_name'].unique()
    agreements_exact = []
    agreements_broad = []

    # Helper function to categorize recommendations
    def categorize_recommendation(rec):
        """Categorize recommendation as Positive or Negative"""
        if rec in ['Fund', 'Fund with Revisions']:
            return 'Positive'
        else:  # 'Do Not Fund'
            return 'Negative'

    for applicant in applicants:
        human_app = df_exp[(df_exp['applicant_name'] == applicant) &
                          (df_exp['reviewer_type'] == 'Human')]['overall_recommendation']
        llm_app = df_exp[(df_exp['applicant_name'] == applicant) &
                        (df_exp['reviewer_type'] == 'LLM')]['overall_recommendation']

        if len(human_app) > 0 and len(llm_app) > 0:
            # Exact agreement
            human_mode = human_app.mode()[0] if len(human_app.mode()) > 0 else None
            llm_mode = llm_app.mode()[0] if len(llm_app.mode()) > 0 else None

            if human_mode and llm_mode:
                agreements_exact.append(human_mode == llm_mode)

            # Broad agreement (Positive vs Negative)
            human_categories = human_app.apply(categorize_recommendation)
            llm_categories = llm_app.apply(categorize_recommendation)

            human_broad_mode = human_categories.mode()[0] if len(human_categories.mode()) > 0 else None
            llm_broad_mode = llm_categories.mode()[0] if len(llm_categories.mode()) > 0 else None

            if human_broad_mode and llm_broad_mode:
                agreements_broad.append(human_broad_mode == llm_broad_mode)

    results['agreement_rate_exact'] = (sum(agreements_exact) / len(agreements_exact) * 100) if agreements_exact else 0
    results['agreement_rate_broad'] = (sum(agreements_broad) / len(agreements_broad) * 100) if agreements_broad else 0
    results['agreement_rate'] = results['agreement_rate_broad']  # Use broad for default

    return results

def analyze_experiment_consistency(df_exp, experiment_key):
    """Analyze inter-rater consistency"""
    results = {}

    applicants = df_exp['applicant_name'].unique()

    human_stds = []
    llm_stds = []

    for applicant in applicants:
        human_scores = df_exp[(df_exp['applicant_name'] == applicant) &
                             (df_exp['reviewer_type'] == 'Human')]['total_score']
        llm_scores = df_exp[(df_exp['applicant_name'] == applicant) &
                           (df_exp['reviewer_type'] == 'LLM')]['total_score']

        if len(human_scores) > 1:
            human_stds.append(human_scores.std())
        if len(llm_scores) > 1:
            llm_stds.append(llm_scores.std())

    results['human_avg_std'] = np.mean(human_stds) if human_stds else np.nan
    results['llm_avg_std'] = np.mean(llm_stds) if llm_stds else np.nan

    # Correlation between human and LLM average scores by applicant
    human_by_app = df_exp[df_exp['reviewer_type'] == 'Human'].groupby('applicant_name')['total_score'].mean()
    llm_by_app = df_exp[df_exp['reviewer_type'] == 'LLM'].groupby('applicant_name')['total_score'].mean()

    common_apps = list(set(human_by_app.index) & set(llm_by_app.index))

    if len(common_apps) >= 2:
        human_matched = [human_by_app[app] for app in common_apps]
        llm_matched = [llm_by_app[app] for app in common_apps]

        pearson_r, pearson_p = pearsonr(human_matched, llm_matched)
        spearman_r, spearman_p = spearmanr(human_matched, llm_matched)

        results['pearson_r'] = pearson_r
        results['pearson_p'] = pearson_p
        results['spearman_r'] = spearman_r
        results['spearman_p'] = spearman_p

    return results

def generate_plots_for_experiment(df_exp, experiment_key, exp_config):
    """Generate all plots for an experiment"""
    short_name = exp_config['short_name']

    # 1. Overall Score Comparison (Box Plot)
    fig, ax = plt.subplots(figsize=(8, 6))

    plot_data = []
    labels = []

    human_scores = df_exp[df_exp['reviewer_type'] == 'Human']['total_score'].dropna()
    llm_scores = df_exp[df_exp['reviewer_type'] == 'LLM']['total_score'].dropna()

    if len(human_scores) > 0:
        plot_data.append(human_scores)
        labels.append('Human')
    if len(llm_scores) > 0:
        plot_data.append(llm_scores)
        labels.append('LLM')

    bp = ax.boxplot(plot_data, labels=labels, patch_artist=True, widths=0.6)

    # Color boxes
    colors = ['#3498db', '#e74c3c']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.6)

    ax.set_ylabel('Total Score (out of 100)')
    ax.set_title(f'{exp_config["name"]}\nOverall Score Comparison')
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / f'{short_name}_overall_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Criteria Comparison (Grouped Bar Chart)
    fig, ax = plt.subplots(figsize=(12, 6))

    criteria_names = []
    human_means = []
    llm_means = []

    for criterion, definition in CRITERIA_DEFINITIONS.items():
        human_crit = df_exp[df_exp['reviewer_type'] == 'Human'][criterion].dropna()
        llm_crit = df_exp[df_exp['reviewer_type'] == 'LLM'][criterion].dropna()

        if len(human_crit) > 0 and len(llm_crit) > 0:
            criteria_names.append(definition['label'])
            human_means.append((human_crit.mean() / definition['max']) * 100)
            llm_means.append((llm_crit.mean() / definition['max']) * 100)

    x = np.arange(len(criteria_names))
    width = 0.35

    ax.bar(x - width/2, human_means, width, label='Human', color='#3498db', alpha=0.8)
    ax.bar(x + width/2, llm_means, width, label='LLM', color='#e74c3c', alpha=0.8)

    ax.set_xlabel('Evaluation Criteria')
    ax.set_ylabel('Average Score (% of maximum)')
    ax.set_title(f'{exp_config["name"]}\nPerformance by Criteria')
    ax.set_xticks(x)
    ax.set_xticklabels(criteria_names, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    ax.set_ylim(0, 100)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / f'{short_name}_criteria_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Model Comparison (Bar Chart)
    fig, ax = plt.subplots(figsize=(10, 6))

    llm_df = df_exp[df_exp['reviewer_type'] == 'LLM']
    vendors = sorted(llm_df['vendor'].dropna().unique())

    vendor_means = []
    vendor_stds = []

    for vendor in vendors:
        vendor_scores = llm_df[llm_df['vendor'] == vendor]['total_score'].dropna()
        vendor_means.append(vendor_scores.mean())
        vendor_stds.append(vendor_scores.std())

    human_mean = df_exp[df_exp['reviewer_type'] == 'Human']['total_score'].mean()

    x = np.arange(len(vendors))
    bars = ax.bar(x, vendor_means, yerr=vendor_stds, capsize=5, alpha=0.8, color=['#e67e22', '#9b59b6', '#1abc9c'])
    ax.axhline(y=human_mean, color='#3498db', linestyle='--', linewidth=2, label='Human Mean')

    ax.set_xlabel('LLM Vendor')
    ax.set_ylabel('Mean Total Score (out of 100)')
    ax.set_title(f'{exp_config["name"]}\nModel Performance Comparison')
    ax.set_xticks(x)
    ax.set_xticklabels(vendors)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / f'{short_name}_model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 4. Recommendation Distribution (Stacked Bar)
    fig, ax = plt.subplots(figsize=(10, 6))

    human_recs = df_exp[df_exp['reviewer_type'] == 'Human']['overall_recommendation'].value_counts()
    llm_recs = df_exp[df_exp['reviewer_type'] == 'LLM']['overall_recommendation'].value_counts()

    # Get all possible recommendations
    all_recs = sorted(set(list(human_recs.index) + list(llm_recs.index)))

    human_counts = [human_recs.get(rec, 0) for rec in all_recs]
    llm_counts = [llm_recs.get(rec, 0) for rec in all_recs]

    x = np.arange(2)
    width = 0.6

    # Create stacked bars
    bottom_human = 0
    bottom_llm = 0
    colors = plt.cm.Set3(np.linspace(0, 1, len(all_recs)))

    for i, rec in enumerate(all_recs):
        ax.bar(0, human_counts[i], width, bottom=bottom_human, label=rec if i == 0 else "", color=colors[i])
        ax.bar(1, llm_counts[i], width, bottom=bottom_llm, color=colors[i])
        bottom_human += human_counts[i]
        bottom_llm += llm_counts[i]

    # Add legend with all recommendations
    handles = [plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(len(all_recs))]
    ax.legend(handles, all_recs, title='Recommendation', bbox_to_anchor=(1.05, 1), loc='upper left')

    ax.set_ylabel('Count')
    ax.set_title(f'{exp_config["name"]}\nRecommendation Distribution')
    ax.set_xticks(x)
    ax.set_xticklabels(['Human', 'LLM'])
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / f'{short_name}_recommendations.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_markdown_report_for_experiment(df_exp, experiment_key, exp_config, analyses):
    """Generate markdown report for an experiment"""
    short_name = exp_config['short_name']

    md = []
    md.append(f"# {exp_config['name']}\n")
    md.append(f"**Description:** {exp_config['description']}\n")
    md.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    md.append("\n---\n")

    # Sample sizes
    md.append("\n## Sample Sizes\n")
    md.append(f"- Human reviews: {analyses['overall']['human']['n']}\n")
    md.append(f"- LLM reviews: {analyses['overall']['llm']['n']}\n")

    if exp_config['exclude_daniel_complete']:
        md.append(f"- *Note: All reviews of DANIEL excluded (used as training data)*\n")

    # Overall Performance
    md.append("\n## Overall Performance\n")
    md.append("\n### Human Reviewers\n")
    md.append(f"- Mean ± SD: {analyses['overall']['human']['mean']:.2f} ± {analyses['overall']['human']['std']:.2f}\n")
    md.append(f"- Median (IQR): {analyses['overall']['human']['median']:.2f} ({analyses['overall']['human']['q25']:.2f} - {analyses['overall']['human']['q75']:.2f})\n")
    md.append(f"- Range: {analyses['overall']['human']['min']:.1f} - {analyses['overall']['human']['max']:.1f}\n")

    md.append("\n### LLM Reviewers\n")
    md.append(f"- Mean ± SD: {analyses['overall']['llm']['mean']:.2f} ± {analyses['overall']['llm']['std']:.2f}\n")
    md.append(f"- Median (IQR): {analyses['overall']['llm']['median']:.2f} ({analyses['overall']['llm']['q25']:.2f} - {analyses['overall']['llm']['q75']:.2f})\n")
    md.append(f"- Range: {analyses['overall']['llm']['min']:.1f} - {analyses['overall']['llm']['max']:.1f}\n")

    if 'statistics' in analyses['overall']:
        stats = analyses['overall']['statistics']
        md.append("\n### Statistical Comparison\n")
        md.append(f"- Difference (LLM - Human): {stats['difference']:+.2f} points\n")
        md.append(f"- t-statistic: {stats['t_statistic']:.3f}\n")
        md.append(f"- p-value: {stats['p_value']:.4f} {'(significant)' if stats['significant'] else '(not significant)'}\n")
        md.append(f"- Cohen's d: {stats['cohens_d']:.3f}\n")

    md.append(f"\n![Overall Comparison]({short_name}_overall_comparison.png)\n")

    # Criteria Performance
    md.append("\n## Performance by Criteria\n")
    md.append("\n| Criterion | Human Mean (%) | LLM Mean (%) | Difference | p-value |\n")
    md.append("|-----------|----------------|--------------|------------|----------|\n")

    for criterion, data in analyses['criteria'].items():
        sig_marker = "*" if data.get('significant', False) else ""
        p_val = f"{data['p_value']:.4f}{sig_marker}" if 'p_value' in data else "N/A"
        md.append(f"| {data['label']} | {data['human_pct']:.1f}% | {data['llm_pct']:.1f}% | {data['difference']:+.2f} | {p_val} |\n")

    md.append(f"\n![Criteria Comparison]({short_name}_criteria_comparison.png)\n")

    # Model Performance
    md.append("\n## Model-Specific Performance\n")
    md.append("\n| Model | n | Mean ± SD | Difference from Human |\n")
    md.append("|-------|---|-----------|----------------------|\n")

    for vendor, data in sorted(analyses['models'].items(), key=lambda x: x[1]['abs_diff_from_human']):
        md.append(f"| {vendor} | {data['n']} | {data['mean']:.2f} ± {data['std']:.2f} | {data['diff_from_human']:+.2f} |\n")

    md.append(f"\n![Model Comparison]({short_name}_model_comparison.png)\n")

    # Recommendations
    md.append("\n## Recommendation Analysis\n")
    md.append(f"\n**Broad Agreement Rate (Positive vs Negative):** {analyses['recommendations']['agreement_rate_broad']:.1f}%\n")
    md.append(f"**Exact Agreement Rate:** {analyses['recommendations']['agreement_rate_exact']:.1f}%\n")
    md.append("\n*Note: Broad agreement groups 'Fund' and 'Fund with Revisions' as 'Positive' vs 'Do Not Fund' as 'Negative'*\n")

    md.append("\n### Human Recommendations\n")
    for rec, data in sorted(analyses['recommendations']['human'].items()):
        md.append(f"- {rec}: {data['count']} ({data['percentage']:.1f}%)\n")

    md.append("\n### LLM Recommendations\n")
    for rec, data in sorted(analyses['recommendations']['llm'].items()):
        md.append(f"- {rec}: {data['count']} ({data['percentage']:.1f}%)\n")

    md.append(f"\n![Recommendations]({short_name}_recommendations.png)\n")

    # Consistency
    md.append("\n## Inter-Rater Consistency\n")
    if not np.isnan(analyses['consistency']['human_avg_std']):
        md.append(f"- Human average SD: {analyses['consistency']['human_avg_std']:.2f}\n")
    if not np.isnan(analyses['consistency']['llm_avg_std']):
        md.append(f"- LLM average SD: {analyses['consistency']['llm_avg_std']:.2f}\n")

    if 'pearson_r' in analyses['consistency']:
        md.append(f"- Pearson correlation: r = {analyses['consistency']['pearson_r']:.3f} (p = {analyses['consistency']['pearson_p']:.4f})\n")
        md.append(f"- Spearman correlation: ρ = {analyses['consistency']['spearman_r']:.3f} (p = {analyses['consistency']['spearman_p']:.4f})\n")

    # Write to file
    with open(OUTPUT_PATH / f'{short_name}_report.md', 'w') as f:
        f.write(''.join(md))

def generate_summary_table(all_analyses):
    """Generate comparative summary table across all experiments"""

    # Get all unique vendors across all experiments
    all_vendors = set()
    for exp_analyses in all_analyses.values():
        all_vendors.update(exp_analyses['models'].keys())
    all_vendors = sorted(all_vendors)

    # Create summary dataframe
    summary_data = []

    for exp_key, analyses in all_analyses.items():
        exp_config = EXPERIMENTS[exp_key]

        row = {
            'Experiment': exp_config['short_name'],
            'Description': exp_config['description'],
            'Human n': analyses['overall']['human']['n'],
            'LLM n': analyses['overall']['llm']['n'],
            'Human Mean': analyses['overall']['human']['mean'],
            'Human SD': analyses['overall']['human']['std'],
            'LLM Mean': analyses['overall']['llm']['mean'],
            'LLM SD': analyses['overall']['llm']['std'],
            'Difference': analyses['overall']['statistics']['difference'] if 'statistics' in analyses['overall'] else np.nan,
            'p-value': analyses['overall']['statistics']['p_value'] if 'statistics' in analyses['overall'] else np.nan,
            "Cohen's d": analyses['overall']['statistics']['cohens_d'] if 'statistics' in analyses['overall'] else np.nan,
            'Broad Agreement Rate': analyses['recommendations']['agreement_rate_broad'],
            'Exact Agreement Rate': analyses['recommendations']['agreement_rate_exact']
        }

        # Add model-specific performance
        for vendor in all_vendors:
            if vendor in analyses['models']:
                row[f'{vendor} Mean'] = analyses['models'][vendor]['mean']
            else:
                row[f'{vendor} Mean'] = np.nan

        summary_data.append(row)

    summary_df = pd.DataFrame(summary_data)

    # Save as CSV
    summary_df.to_csv(OUTPUT_PATH / 'summary_table.csv', index=False)

    # Generate markdown table
    md = ["# Summary Comparison Across All Experiments\n\n"]
    md.append(summary_df.to_markdown(index=False))

    with open(OUTPUT_PATH / 'summary_comparison.md', 'w') as f:
        f.write(''.join(md))

    return summary_df

def generate_sample_size_summary(df):
    """Generate detailed sample size summary showing which reviews are included in each experiment"""

    summary_rows = []

    for exp_key in ['baseline_v1', 'multi_examples_v1', 'strict_scoring_v1']:
        exp_config = EXPERIMENTS[exp_key]
        df_exp = filter_for_experiment(df, exp_key)

        # Get human and LLM reviews
        human_reviews = df_exp[df_exp['reviewer_type'] == 'Human']
        llm_reviews = df_exp[df_exp['reviewer_type'] == 'LLM']

        # Count by applicant
        for applicant in ['CHRISTINA', 'KELLY', 'DANIEL']:
            human_app = human_reviews[human_reviews['applicant_name'] == applicant]
            llm_app = llm_reviews[llm_reviews['applicant_name'] == applicant]

            # Get reviewer IDs
            reviewer_ids = sorted(human_app['reviewer_id'].unique()) if len(human_app) > 0 else []
            reviewer_list = ', '.join(reviewer_ids) if reviewer_ids else 'None'

            # Get LLM vendors
            vendors = llm_app['vendor'].value_counts().to_dict() if len(llm_app) > 0 else {}

            summary_rows.append({
                'Experiment': exp_config['short_name'],
                'Experiment Name': exp_key,
                'Applicant': applicant,
                'Human Count': len(human_app),
                'Human Reviewers': reviewer_list,
                'LLM Count': len(llm_app),
                'LLM Breakdown': f"Google={vendors.get('Google', 0)}, OpenAI={vendors.get('OpenAI', 0)}, xAI={vendors.get('xAI', 0)}"
            })

    summary_df = pd.DataFrame(summary_rows)

    # Save as CSV
    summary_df.to_csv(OUTPUT_PATH / 'sample_size_detail.csv', index=False)

    # Generate markdown version
    md = ["# Detailed Sample Size Summary by Experiment\n\n"]

    for exp_key in ['baseline_v1', 'multi_examples_v1', 'strict_scoring_v1']:
        exp_config = EXPERIMENTS[exp_key]
        exp_data = summary_df[summary_df['Experiment Name'] == exp_key]

        md.append(f"\n## {exp_config['name']}\n")
        md.append(f"**{exp_config['description']}**\n\n")

        # Add note about exclusions
        if exp_config['exclude_daniel_complete']:
            md.append("*Exclusion Rule: All reviews of DANIEL excluded (used as training data)*\n\n")
        else:
            md.append("*Exclusion Rule: None - all reviews included*\n\n")

        md.append("| Applicant | Human Count | Human Reviewers | LLM Count | LLM Breakdown |\n")
        md.append("|-----------|-------------|-----------------|-----------|---------------|\n")

        for _, row in exp_data.iterrows():
            md.append(f"| {row['Applicant']} | {row['Human Count']} | {row['Human Reviewers']} | {row['LLM Count']} | {row['LLM Breakdown']} |\n")

        # Add totals
        total_human = exp_data['Human Count'].sum()
        total_llm = exp_data['LLM Count'].sum()
        md.append(f"| **TOTAL** | **{total_human}** | - | **{total_llm}** | - |\n")

    with open(OUTPUT_PATH / 'sample_size_detail.md', 'w') as f:
        f.write(''.join(md))

    # Also create a pivot table summary
    pivot_data = []
    for exp_key in ['baseline_v1', 'multi_examples_v1', 'strict_scoring_v1']:
        exp_config = EXPERIMENTS[exp_key]
        df_exp = filter_for_experiment(df, exp_key)

        row = {
            'Experiment': exp_config['short_name'],
            'Total Reviews': len(df_exp),
            'Human Reviews': len(df_exp[df_exp['reviewer_type'] == 'Human']),
            'LLM Reviews': len(df_exp[df_exp['reviewer_type'] == 'LLM']),
            'CHRISTINA (Human)': len(df_exp[(df_exp['reviewer_type'] == 'Human') & (df_exp['applicant_name'] == 'CHRISTINA')]),
            'KELLY (Human)': len(df_exp[(df_exp['reviewer_type'] == 'Human') & (df_exp['applicant_name'] == 'KELLY')]),
            'DANIEL (Human)': len(df_exp[(df_exp['reviewer_type'] == 'Human') & (df_exp['applicant_name'] == 'DANIEL')]),
            'CHRISTINA (LLM)': len(df_exp[(df_exp['reviewer_type'] == 'LLM') & (df_exp['applicant_name'] == 'CHRISTINA')]),
            'KELLY (LLM)': len(df_exp[(df_exp['reviewer_type'] == 'LLM') & (df_exp['applicant_name'] == 'KELLY')]),
            'DANIEL (LLM)': len(df_exp[(df_exp['reviewer_type'] == 'LLM') & (df_exp['applicant_name'] == 'DANIEL')])
        }
        pivot_data.append(row)

    pivot_df = pd.DataFrame(pivot_data)
    pivot_df.to_csv(OUTPUT_PATH / 'sample_size_pivot.csv', index=False)

    # Markdown version of pivot
    md_pivot = ["# Sample Size Pivot Table\n\n"]
    md_pivot.append(pivot_df.to_markdown(index=False))
    md_pivot.append("\n\n## Notes:\n")
    md_pivot.append("- Exp1 (baseline_v1): All reviews included (12 human + 27 LLM)\n")
    md_pivot.append("- Exp3 (multi_examples_v1): DANIEL completely excluded - used as training (8 human + 18 LLM)\n")
    md_pivot.append("- Exp4 (strict_scoring_v1): DANIEL completely excluded - used as training (8 human + 18 LLM)\n")

    with open(OUTPUT_PATH / 'sample_size_pivot.md', 'w') as f:
        f.write(''.join(md_pivot))

    return summary_df, pivot_df

def generate_comparative_plots(all_analyses):
    """Generate plots comparing across experiments"""

    # 1. Mean scores across experiments
    fig, ax = plt.subplots(figsize=(12, 6))

    experiments = []
    human_means = []
    llm_means = []

    for exp_key in ['baseline_v1', 'multi_examples_v1', 'strict_scoring_v1']:
        exp_config = EXPERIMENTS[exp_key]
        analyses = all_analyses[exp_key]

        experiments.append(exp_config['short_name'])
        human_means.append(analyses['overall']['human']['mean'])
        llm_means.append(analyses['overall']['llm']['mean'])

    x = np.arange(len(experiments))
    width = 0.35

    ax.bar(x - width/2, human_means, width, label='Human', color='#3498db', alpha=0.8)
    ax.bar(x + width/2, llm_means, width, label='LLM', color='#e74c3c', alpha=0.8)

    ax.set_xlabel('Experiment')
    ax.set_ylabel('Mean Total Score (out of 100)')
    ax.set_title('Mean Scores Across All Experiments')
    ax.set_xticks(x)
    ax.set_xticklabels(experiments, rotation=45, ha='right')
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / 'comparative_mean_scores.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Agreement rates across experiments (Exact vs Broad)
    fig, ax = plt.subplots(figsize=(12, 6))

    agreement_rates_exact = [all_analyses[exp_key]['recommendations']['agreement_rate_exact']
                            for exp_key in ['baseline_v1', 'multi_examples_v1', 'strict_scoring_v1']]
    agreement_rates_broad = [all_analyses[exp_key]['recommendations']['agreement_rate_broad']
                            for exp_key in ['baseline_v1', 'multi_examples_v1', 'strict_scoring_v1']]

    x = np.arange(len(experiments))
    width = 0.35

    bars1 = ax.bar(x - width/2, agreement_rates_exact, width, label='Exact Agreement', color='#e74c3c', alpha=0.8)
    bars2 = ax.bar(x + width/2, agreement_rates_broad, width, label='Broad Agreement\n(Positive vs Negative)', color='#2ecc71', alpha=0.8)

    ax.set_xlabel('Experiment')
    ax.set_ylabel('Agreement Rate (%)')
    ax.set_title('Human-LLM Recommendation Agreement Across Experiments')
    ax.set_xticks(x)
    ax.set_xticklabels(experiments, rotation=45, ha='right')
    ax.set_ylim(0, 100)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.0f}%', ha='center', va='bottom', fontsize=9)

    plt.tight_layout()
    plt.savefig(OUTPUT_PATH / 'comparative_agreement_rates.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Consistency comparison
    fig, ax = plt.subplots(figsize=(10, 6))

    human_stds = []
    llm_stds = []
    valid_experiments = []

    for exp_key in ['baseline_v1', 'multi_examples_v1', 'strict_scoring_v1']:
        exp_config = EXPERIMENTS[exp_key]
        analyses = all_analyses[exp_key]

        if not np.isnan(analyses['consistency']['human_avg_std']) and not np.isnan(analyses['consistency']['llm_avg_std']):
            valid_experiments.append(exp_config['short_name'])
            human_stds.append(analyses['consistency']['human_avg_std'])
            llm_stds.append(analyses['consistency']['llm_avg_std'])

    if valid_experiments:
        x = np.arange(len(valid_experiments))
        width = 0.35

        ax.bar(x - width/2, human_stds, width, label='Human', color='#3498db', alpha=0.8)
        ax.bar(x + width/2, llm_stds, width, label='LLM', color='#e74c3c', alpha=0.8)

        ax.set_xlabel('Experiment')
        ax.set_ylabel('Average Standard Deviation')
        ax.set_title('Inter-Rater Consistency Across Experiments\n(Lower = More Consistent)')
        ax.set_xticks(x)
        ax.set_xticklabels(valid_experiments, rotation=45, ha='right')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)

        plt.tight_layout()
        plt.savefig(OUTPUT_PATH / 'comparative_consistency.png', dpi=300, bbox_inches='tight')
        plt.close()

def main():
    """Main analysis function"""
    print("="*80)
    print("MANUSCRIPT STATISTICAL ANALYSIS - VERSION 2")
    print("3 Experiments with Updated Exclusion Criteria")
    print("="*80)

    # Load data
    print("\nLoading data...")
    df = load_data()
    print(f"✓ Loaded {len(df)} total reviews")
    print(f"  - Human reviews: {len(df[df['reviewer_type'] == 'Human'])}")
    print(f"  - LLM reviews: {len(df[df['reviewer_type'] == 'LLM'])}")

    # Generate sample size summaries
    print(f"\n{'='*80}")
    print("Generating sample size summaries...")
    print(f"{'='*80}")
    sample_detail_df, sample_pivot_df = generate_sample_size_summary(df)
    print("✓ Sample size detail table generated")
    print("✓ Sample size pivot table generated")
    print("\nSample Size Pivot:")
    print(sample_pivot_df.to_string(index=False))

    # Analyze each experiment
    all_analyses = {}

    for exp_key, exp_config in EXPERIMENTS.items():
        print(f"\n{'='*80}")
        print(f"Processing: {exp_config['name']}")
        print(f"{'='*80}")

        # Filter data
        df_exp = filter_for_experiment(df, exp_key)

        print(f"Filtered data:")
        print(f"  - Human reviews: {len(df_exp[df_exp['reviewer_type'] == 'Human'])}")
        print(f"  - LLM reviews: {len(df_exp[df_exp['reviewer_type'] == 'LLM'])}")

        # Run analyses
        print("Running analyses...")
        analyses = {
            'overall': analyze_experiment_overall(df_exp, exp_key),
            'criteria': analyze_experiment_criteria(df_exp, exp_key),
            'models': analyze_experiment_models(df_exp, exp_key),
            'recommendations': analyze_experiment_recommendations(df_exp, exp_key),
            'consistency': analyze_experiment_consistency(df_exp, exp_key)
        }

        all_analyses[exp_key] = analyses

        # Generate plots
        print("Generating plots...")
        generate_plots_for_experiment(df_exp, exp_key, exp_config)

        # Generate markdown report
        print("Generating report...")
        generate_markdown_report_for_experiment(df_exp, exp_key, exp_config, analyses)

        print(f"✓ Completed {exp_config['short_name']}")

    # Generate comparative analyses
    print(f"\n{'='*80}")
    print("Generating comparative analyses...")
    print(f"{'='*80}")

    summary_df = generate_summary_table(all_analyses)
    print("✓ Summary table generated")

    generate_comparative_plots(all_analyses)
    print("✓ Comparative plots generated")

    # Save all analyses to JSON
    # Convert to serializable format
    def convert_to_serializable(obj):
        """Recursively convert numpy types to Python types"""
        if pd.isna(obj):
            return None
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {key: convert_to_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [convert_to_serializable(item) for item in obj]
        elif isinstance(obj, (bool, int, float, str, type(None))):
            return obj
        else:
            # Try to convert to string as fallback
            return str(obj)

    serializable_analyses = convert_to_serializable(all_analyses)

    with open(OUTPUT_PATH / 'all_analyses.json', 'w') as f:
        json.dump(serializable_analyses, f, indent=2)

    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*80}")
    print(f"\nAll outputs saved to: {OUTPUT_PATH}")
    print("\nGenerated files:")
    print("  Sample Size Tables:")
    print("    - sample_size_detail.md (detailed breakdown by applicant)")
    print("    - sample_size_detail.csv")
    print("    - sample_size_pivot.md (summary pivot table)")
    print("    - sample_size_pivot.csv")
    print("  Reports:")
    for exp_key, exp_config in EXPERIMENTS.items():
        print(f"    - {exp_config['short_name']}_report.md")
    print("  Summary:")
    print("    - summary_comparison.md")
    print("    - summary_table.csv")
    print("    - all_analyses.json")
    print("  Plots:")
    print("    - Individual experiment plots (4 per experiment)")
    print("    - Comparative plots (3 cross-experiment)")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    main()
