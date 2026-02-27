#!/usr/bin/env python3
"""
Generate statistical analyses for presentation

This script calculates key findings and statistics from the grant review database.
Results are printed in a format suitable for copying into the presentation.
"""

import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from scipy.stats import pearsonr, spearmanr
import json

# Define paths
BASE_PATH = Path(__file__).parent.parent
DB_PATH = BASE_PATH / "data" / "results.db"
OUTPUT_PATH = Path(__file__).parent / "analysis_results.json"

# Experiments that exclude Daniel
EXPERIMENTS_EXCLUDING_DANIEL = ['with_training_data_v1', 'multi_examples_v1', 'strict_scoring_v1']

def load_data():
    """Load data from database"""
    conn = sqlite3.connect(DB_PATH)

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

    filtered = df[(df['prompt_experiment_name'] == experiment_name) | (df['reviewer_type'] == 'Human')]

    if experiment_name in EXPERIMENTS_EXCLUDING_DANIEL:
        filtered = filtered[~((filtered['applicant_name'] == 'DANIEL') & (filtered['reviewer_type'] == 'LLM'))]

    return filtered

def analyze_overall_performance(df):
    """Analyze overall human vs LLM performance"""
    print("\n" + "="*80)
    print("ANALYSIS 1: OVERALL HUMAN VS. LLM PERFORMANCE")
    print("="*80)

    human = df[df['reviewer_type'] == 'Human']['total_score'].dropna()
    llm = df[df['reviewer_type'] == 'LLM']['total_score'].dropna()

    # Descriptive statistics
    human_mean = human.mean()
    human_std = human.std()
    human_median = human.median()
    human_iqr = human.quantile(0.75) - human.quantile(0.25)

    llm_mean = llm.mean()
    llm_std = llm.std()
    llm_median = llm.median()
    llm_iqr = llm.quantile(0.75) - llm.quantile(0.25)

    print(f"\nHuman Reviewers (n={len(human)}):")
    print(f"  Mean ± SD: {human_mean:.2f} ± {human_std:.2f}")
    print(f"  Median (IQR): {human_median:.2f} ({human_iqr:.2f})")
    print(f"  Range: {human.min():.0f} - {human.max():.0f}")

    print(f"\nLLM Reviewers (n={len(llm)}):")
    print(f"  Mean ± SD: {llm_mean:.2f} ± {llm_std:.2f}")
    print(f"  Median (IQR): {llm_median:.2f} ({llm_iqr:.2f})")
    print(f"  Range: {llm.min():.0f} - {llm.max():.0f}")

    # Statistical test
    t_stat, p_value = stats.ttest_ind(human, llm)
    cohens_d = (llm_mean - human_mean) / np.sqrt((human_std**2 + llm_std**2) / 2)

    print(f"\nStatistical Comparison:")
    print(f"  Difference: {llm_mean - human_mean:+.2f} points")
    print(f"  Two-sample t-test: t={t_stat:.3f}, p={p_value:.4f}")
    print(f"  Cohen's d: {cohens_d:.3f} ({'small' if abs(cohens_d) < 0.5 else 'medium' if abs(cohens_d) < 0.8 else 'large'} effect)")

    interpretation = "LLMs score significantly higher" if p_value < 0.05 and llm_mean > human_mean else \
                     "LLMs score significantly lower" if p_value < 0.05 and llm_mean < human_mean else \
                     "No significant difference"
    print(f"  Interpretation: {interpretation}")

    return {
        'human_mean': human_mean,
        'human_std': human_std,
        'human_n': len(human),
        'llm_mean': llm_mean,
        'llm_std': llm_std,
        'llm_n': len(llm),
        'difference': llm_mean - human_mean,
        'p_value': p_value,
        'cohens_d': cohens_d,
        'interpretation': interpretation
    }

def analyze_criteria_performance(df):
    """Analyze performance by evaluation criteria"""
    print("\n" + "="*80)
    print("ANALYSIS 2: PERFORMANCE BY CRITERIA")
    print("="*80)

    criteria_cols = [
        'innovation_impact', 'methodological_approach', 'research_team_strength',
        'external_funding_potential', 'budget_clarity', 'presentation_quality'
    ]

    criteria_labels = [
        'Innovation & Impact (max 30)',
        'Methodology & Feasibility (max 30)',
        'Team Strength (max 10)',
        'External Funding (max 10)',
        'Budget Clarity (max 10)',
        'Presentation Quality (max 10)'
    ]

    max_scores = [30, 30, 10, 10, 10, 10]

    results = {}

    for i, (col, label, max_score) in enumerate(zip(criteria_cols, criteria_labels, max_scores)):
        human_scores = df[df['reviewer_type'] == 'Human'][col].dropna()
        llm_scores = df[df['reviewer_type'] == 'LLM'][col].dropna()

        human_pct = (human_scores.mean() / max_score) * 100
        llm_pct = (llm_scores.mean() / max_score) * 100

        t_stat, p_value = stats.ttest_ind(human_scores, llm_scores)

        print(f"\n{label}:")
        print(f"  Human: {human_scores.mean():.2f}/{max_score} ({human_pct:.1f}%)")
        print(f"  LLM:   {llm_scores.mean():.2f}/{max_score} ({llm_pct:.1f}%)")
        print(f"  Difference: {llm_scores.mean() - human_scores.mean():+.2f} points")
        print(f"  p-value: {p_value:.4f} {'***' if p_value < 0.001 else '**' if p_value < 0.01 else '*' if p_value < 0.05 else 'ns'}")

        results[col] = {
            'human_mean': human_scores.mean(),
            'llm_mean': llm_scores.mean(),
            'human_pct': human_pct,
            'llm_pct': llm_pct,
            'difference': llm_scores.mean() - human_scores.mean(),
            'p_value': p_value
        }

    # Identify biggest differences
    sorted_diffs = sorted(results.items(), key=lambda x: abs(x[1]['difference']), reverse=True)
    print(f"\nBiggest Differences:")
    for i, (criterion, data) in enumerate(sorted_diffs[:3], 1):
        label = criteria_labels[criteria_cols.index(criterion)]
        print(f"  {i}. {label}: {data['difference']:+.2f} points")

    return results

def analyze_experiment_impact(df):
    """Analyze impact of different prompt engineering approaches"""
    print("\n" + "="*80)
    print("ANALYSIS 3: PROMPT ENGINEERING IMPACT")
    print("="*80)

    experiment_order = ['baseline_v1', 'with_training_data_v1', 'multi_examples_v1', 'strict_scoring_v1']
    experiment_names = {
        'baseline_v1': 'Baseline (no examples)',
        'with_training_data_v1': 'Single Example',
        'multi_examples_v1': 'Multiple Examples (4)',
        'strict_scoring_v1': 'Strict Instructions'
    }

    human_mean = df[df['reviewer_type'] == 'Human']['total_score'].mean()

    results = {}

    for exp in experiment_order:
        exp_df = filter_for_experiment(df, exp)
        exp_llm = exp_df[exp_df['reviewer_type'] == 'LLM']['total_score'].dropna()

        if len(exp_llm) > 0:
            exp_mean = exp_llm.mean()
            exp_std = exp_llm.std()
            diff_from_human = exp_mean - human_mean

            print(f"\n{experiment_names[exp]}:")
            print(f"  Mean ± SD: {exp_mean:.2f} ± {exp_std:.2f} (n={len(exp_llm)})")
            print(f"  Difference from human mean: {diff_from_human:+.2f} points")
            print(f"  Distance from human: {abs(diff_from_human):.2f} points")

            results[exp] = {
                'mean': exp_mean,
                'std': exp_std,
                'n': len(exp_llm),
                'diff_from_human': diff_from_human,
                'abs_diff_from_human': abs(diff_from_human)
            }

    # Find best alignment with humans
    best_exp = min(results.items(), key=lambda x: x[1]['abs_diff_from_human'])
    worst_exp = max(results.items(), key=lambda x: x[1]['abs_diff_from_human'])

    print(f"\nBest alignment with humans: {experiment_names[best_exp[0]]} ({best_exp[1]['abs_diff_from_human']:.2f} points difference)")
    print(f"Worst alignment with humans: {experiment_names[worst_exp[0]]} ({worst_exp[1]['abs_diff_from_human']:.2f} points difference)")

    # ANOVA to test if experiments differ significantly
    exp_groups = [filter_for_experiment(df, exp)[filter_for_experiment(df, exp)['reviewer_type'] == 'LLM']['total_score'].dropna()
                  for exp in experiment_order]
    f_stat, p_value = stats.f_oneway(*exp_groups)

    print(f"\nOne-way ANOVA: F={f_stat:.3f}, p={p_value:.4f}")
    print(f"Interpretation: {'Experiments differ significantly' if p_value < 0.05 else 'No significant difference between experiments'}")

    return results, best_exp, worst_exp

def analyze_model_performance(df):
    """Analyze performance by LLM vendor"""
    print("\n" + "="*80)
    print("ANALYSIS 4: MODEL-SPECIFIC PERFORMANCE")
    print("="*80)

    llm_df = df[df['reviewer_type'] == 'LLM']
    human_mean = df[df['reviewer_type'] == 'Human']['total_score'].mean()

    vendors = llm_df['vendor'].dropna().unique()

    results = {}

    for vendor in sorted(vendors):
        vendor_scores = llm_df[llm_df['vendor'] == vendor]['total_score'].dropna()

        if len(vendor_scores) > 0:
            vendor_mean = vendor_scores.mean()
            vendor_std = vendor_scores.std()
            diff_from_human = vendor_mean - human_mean

            print(f"\n{vendor} (n={len(vendor_scores)}):")
            print(f"  Mean ± SD: {vendor_mean:.2f} ± {vendor_std:.2f}")
            print(f"  Difference from human: {diff_from_human:+.2f} points")

            results[vendor] = {
                'mean': vendor_mean,
                'std': vendor_std,
                'n': len(vendor_scores),
                'diff_from_human': diff_from_human
            }

    # Rank vendors by alignment with humans
    ranked = sorted(results.items(), key=lambda x: abs(x[1]['diff_from_human']))

    print(f"\nRanking by alignment with humans:")
    for i, (vendor, data) in enumerate(ranked, 1):
        print(f"  {i}. {vendor}: {abs(data['diff_from_human']):.2f} points difference")

    return results, ranked

def analyze_inter_rater_reliability(df):
    """Analyze inter-rater reliability and agreement"""
    print("\n" + "="*80)
    print("ANALYSIS 5: INTER-RATER RELIABILITY & AGREEMENT")
    print("="*80)

    # Calculate variance by applicant for humans and LLMs
    applicants = df['applicant_name'].unique()

    print("\nVariability by Applicant:")
    print(f"{'Applicant':<15} {'Human SD':<12} {'LLM SD':<12} {'Ratio (LLM/Human)'}")
    print("-" * 55)

    human_vars = []
    llm_vars = []

    for applicant in sorted(applicants):
        human_scores = df[(df['applicant_name'] == applicant) & (df['reviewer_type'] == 'Human')]['total_score']
        llm_scores = df[(df['applicant_name'] == applicant) & (df['reviewer_type'] == 'LLM')]['total_score']

        if len(human_scores) > 1 and len(llm_scores) > 1:
            human_std = human_scores.std()
            llm_std = llm_scores.std()
            ratio = llm_std / human_std if human_std > 0 else np.nan

            print(f"{applicant:<15} {human_std:>10.2f}  {llm_std:>10.2f}  {ratio:>10.2f}")

            human_vars.append(human_std)
            llm_vars.append(llm_std)

    avg_human_std = np.mean(human_vars)
    avg_llm_std = np.mean(llm_vars)

    print(f"\nAverage across applicants:")
    print(f"  Human SD: {avg_human_std:.2f}")
    print(f"  LLM SD: {avg_llm_std:.2f}")
    print(f"  Interpretation: {'LLMs are more consistent' if avg_llm_std < avg_human_std else 'Humans are more consistent'}")

    # Calculate correlation between human and LLM average scores by applicant
    human_by_app = df[df['reviewer_type'] == 'Human'].groupby('applicant_name')['total_score'].mean()
    llm_by_app = df[df['reviewer_type'] == 'LLM'].groupby('applicant_name')['total_score'].mean()

    common_apps = list(set(human_by_app.index) & set(llm_by_app.index))
    human_matched = [human_by_app[app] for app in common_apps]
    llm_matched = [llm_by_app[app] for app in common_apps]

    if len(human_matched) > 2:
        pearson_r, pearson_p = pearsonr(human_matched, llm_matched)
        spearman_r, spearman_p = spearmanr(human_matched, llm_matched)

        print(f"\nHuman-LLM Agreement (by applicant):")
        print(f"  Pearson correlation: r = {pearson_r:.3f}, p = {pearson_p:.4f}")
        print(f"  Spearman correlation: ρ = {spearman_r:.3f}, p = {spearman_p:.4f}")
        print(f"  Interpretation: {'Strong agreement' if abs(pearson_r) > 0.7 else 'Moderate agreement' if abs(pearson_r) > 0.4 else 'Weak agreement'}")

    return {
        'avg_human_std': avg_human_std,
        'avg_llm_std': avg_llm_std,
        'pearson_r': pearson_r if len(human_matched) > 2 else None,
        'spearman_r': spearman_r if len(human_matched) > 2 else None
    }

def analyze_recommendation_agreement(df):
    """Analyze agreement in funding recommendations"""
    print("\n" + "="*80)
    print("ANALYSIS 6: RECOMMENDATION AGREEMENT")
    print("="*80)

    # Get recommendation distribution
    human_recs = df[df['reviewer_type'] == 'Human']['overall_recommendation'].value_counts()
    llm_recs = df[df['reviewer_type'] == 'LLM']['overall_recommendation'].value_counts()

    print("\nRecommendation Distribution:")
    print("\nHuman Reviewers:")
    for rec, count in human_recs.items():
        pct = (count / len(df[df['reviewer_type'] == 'Human'])) * 100
        print(f"  {rec}: {count} ({pct:.1f}%)")

    print("\nLLM Reviewers:")
    for rec, count in llm_recs.items():
        pct = (count / len(df[df['reviewer_type'] == 'LLM'])) * 100
        print(f"  {rec}: {count} ({pct:.1f}%)")

    # Analyze by applicant
    applicants = df['applicant_name'].unique()

    print("\nRecommendation Agreement by Applicant:")
    print(f"{'Applicant':<15} {'Human Majority':<20} {'LLM Majority':<20} {'Agreement'}")
    print("-" * 75)

    agreements = []

    for applicant in sorted(applicants):
        human_app = df[(df['applicant_name'] == applicant) & (df['reviewer_type'] == 'Human')]
        llm_app = df[(df['applicant_name'] == applicant) & (df['reviewer_type'] == 'LLM')]

        if len(human_app) > 0 and len(llm_app) > 0:
            human_majority = human_app['overall_recommendation'].mode()[0] if len(human_app['overall_recommendation'].mode()) > 0 else 'N/A'
            llm_majority = llm_app['overall_recommendation'].mode()[0] if len(llm_app['overall_recommendation'].mode()) > 0 else 'N/A'

            agreement = '✓' if human_majority == llm_majority else '✗'
            agreements.append(human_majority == llm_majority)

            print(f"{applicant:<15} {human_majority:<20} {llm_majority:<20} {agreement}")

    agreement_rate = sum(agreements) / len(agreements) * 100 if agreements else 0
    print(f"\nOverall Agreement Rate: {agreement_rate:.1f}%")

    return {
        'human_recs': human_recs.to_dict(),
        'llm_recs': llm_recs.to_dict(),
        'agreement_rate': agreement_rate
    }

def analyze_experiment_detailed(df, experiment_name, experiment_label):
    """Detailed analysis for a specific experiment"""
    print("\n" + "="*80)
    print(f"DETAILED ANALYSIS: {experiment_label}")
    print("="*80)

    # Filter data for this experiment
    exp_df = filter_for_experiment(df, experiment_name)

    # Overall performance
    human_scores = exp_df[exp_df['reviewer_type'] == 'Human']['total_score'].dropna()
    llm_scores = exp_df[exp_df['reviewer_type'] == 'LLM']['total_score'].dropna()

    print(f"\n{'='*80}")
    print(f"OVERALL SCORES - {experiment_label}")
    print(f"{'='*80}")

    if len(llm_scores) > 0:
        human_mean = human_scores.mean()
        human_std = human_scores.std()
        llm_mean = llm_scores.mean()
        llm_std = llm_scores.std()

        print(f"\nHuman Reviewers (n={len(human_scores)}):")
        print(f"  Mean ± SD: {human_mean:.2f} ± {human_std:.2f}")
        print(f"\nLLM Reviewers (n={len(llm_scores)}):")
        print(f"  Mean ± SD: {llm_mean:.2f} ± {llm_std:.2f}")
        print(f"  Difference from Human: {llm_mean - human_mean:+.2f} points")

        if len(llm_scores) > 1 and len(human_scores) > 1:
            t_stat, p_value = stats.ttest_ind(human_scores, llm_scores)
            cohens_d = (llm_mean - human_mean) / np.sqrt((human_std**2 + llm_std**2) / 2)
            print(f"  t-test: t={t_stat:.3f}, p={p_value:.4f}")
            print(f"  Cohen's d: {cohens_d:.3f}")

    # Criteria breakdown
    print(f"\n{'='*80}")
    print(f"CRITERIA BREAKDOWN - {experiment_label}")
    print(f"{'='*80}")

    criteria_cols = [
        'innovation_impact', 'methodological_approach', 'research_team_strength',
        'external_funding_potential', 'budget_clarity', 'presentation_quality'
    ]

    criteria_labels = [
        'Innovation & Impact',
        'Methodology',
        'Team Strength',
        'External Funding',
        'Budget Clarity',
        'Presentation Quality'
    ]

    max_scores = [30, 30, 10, 10, 10, 10]

    criteria_results = {}

    for col, label, max_score in zip(criteria_cols, criteria_labels, max_scores):
        human_criterion = exp_df[exp_df['reviewer_type'] == 'Human'][col].dropna()
        llm_criterion = exp_df[exp_df['reviewer_type'] == 'LLM'][col].dropna()

        if len(llm_criterion) > 0 and len(human_criterion) > 0:
            human_mean = human_criterion.mean()
            llm_mean = llm_criterion.mean()
            diff = llm_mean - human_mean

            print(f"\n{label} (max {max_score}):")
            print(f"  Human: {human_mean:.2f} ({(human_mean/max_score)*100:.1f}%)")
            print(f"  LLM:   {llm_mean:.2f} ({(llm_mean/max_score)*100:.1f}%)")
            print(f"  Difference: {diff:+.2f} points")

            criteria_results[col] = {
                'human_mean': human_mean,
                'llm_mean': llm_mean,
                'difference': diff
            }

    # Model comparison within experiment
    print(f"\n{'='*80}")
    print(f"MODEL PERFORMANCE - {experiment_label}")
    print(f"{'='*80}")

    llm_exp_df = exp_df[exp_df['reviewer_type'] == 'LLM']
    vendors = llm_exp_df['vendor'].dropna().unique()

    model_results = {}

    for vendor in sorted(vendors):
        vendor_scores = llm_exp_df[llm_exp_df['vendor'] == vendor]['total_score'].dropna()
        if len(vendor_scores) > 0:
            vendor_mean = vendor_scores.mean()
            vendor_std = vendor_scores.std()
            print(f"\n{vendor} (n={len(vendor_scores)}):")
            print(f"  Mean ± SD: {vendor_mean:.2f} ± {vendor_std:.2f}")
            model_results[vendor] = {
                'mean': vendor_mean,
                'std': vendor_std,
                'n': len(vendor_scores)
            }

    # Recommendation distribution
    print(f"\n{'='*80}")
    print(f"RECOMMENDATION DISTRIBUTION - {experiment_label}")
    print(f"{'='*80}")

    human_recs = exp_df[exp_df['reviewer_type'] == 'Human']['overall_recommendation'].value_counts()
    llm_recs = exp_df[exp_df['reviewer_type'] == 'LLM']['overall_recommendation'].value_counts()

    print("\nHuman Reviewers:")
    for rec, count in human_recs.items():
        pct = (count / len(exp_df[exp_df['reviewer_type'] == 'Human'])) * 100
        print(f"  {rec}: {count} ({pct:.1f}%)")

    print("\nLLM Reviewers:")
    for rec, count in llm_recs.items():
        pct = (count / len(exp_df[exp_df['reviewer_type'] == 'LLM'])) * 100
        print(f"  {rec}: {count} ({pct:.1f}%)")

    return {
        'overall': {
            'human_mean': human_mean if len(human_scores) > 0 else None,
            'llm_mean': llm_mean if len(llm_scores) > 0 else None,
            'difference': llm_mean - human_mean if len(llm_scores) > 0 and len(human_scores) > 0 else None
        },
        'criteria': criteria_results,
        'models': model_results,
        'recommendations': {
            'human': human_recs.to_dict(),
            'llm': llm_recs.to_dict()
        }
    }

def generate_key_findings_summary(all_results):
    """Generate a summary of key findings for the presentation"""
    print("\n" + "="*80)
    print("KEY FINDINGS SUMMARY FOR PRESENTATION")
    print("="*80)

    print("\n1. OVERALL PERFORMANCE:")
    print(f"   - LLMs scored {all_results['overall']['interpretation'].lower()}")
    print(f"   - Average difference: {all_results['overall']['difference']:+.2f} points")
    print(f"   - Effect size: {all_results['overall']['cohens_d']:.2f} (Cohen's d)")

    print("\n2. BY CRITERIA:")
    # Find criteria with biggest differences
    criteria_names = {
        'innovation_impact': 'Innovation & Impact',
        'methodological_approach': 'Methodology',
        'research_team_strength': 'Team Strength',
        'external_funding_potential': 'External Funding',
        'budget_clarity': 'Budget',
        'presentation_quality': 'Presentation'
    }
    sorted_criteria = sorted(all_results['criteria'].items(),
                            key=lambda x: abs(x[1]['difference']), reverse=True)

    for i, (criterion, data) in enumerate(sorted_criteria[:3], 1):
        direction = "higher" if data['difference'] > 0 else "lower"
        print(f"   {i}. {criteria_names[criterion]}: LLMs {abs(data['difference']):.2f} pts {direction}")

    print("\n3. PROMPT ENGINEERING:")
    best_exp_name = all_results['experiments']['best'][0].replace('_', ' ').title()
    best_diff = all_results['experiments']['best'][1]['abs_diff_from_human']
    print(f"   - Best alignment: {best_exp_name} ({best_diff:.2f} pts from human mean)")
    print(f"   - Training examples {'improved' if 'with_training' in all_results['experiments']['best'][0] else 'did not clearly improve'} alignment")

    print("\n4. MODEL COMPARISON:")
    best_model = all_results['models']['ranked'][0]
    print(f"   - Best model: {best_model[0]} ({abs(best_model[1]['diff_from_human']):.2f} pts from human)")

    print("\n5. INTER-RATER RELIABILITY:")
    consistency = "more" if all_results['reliability']['avg_llm_std'] < all_results['reliability']['avg_human_std'] else "less"
    print(f"   - LLMs are {consistency} consistent than humans")
    print(f"   - Human-LLM correlation: r = {all_results['reliability']['pearson_r']:.2f}")

    print("\n6. RECOMMENDATION AGREEMENT:")
    print(f"   - Agreement rate: {all_results['recommendations']['agreement_rate']:.1f}%")

def main():
    """Run all analyses"""
    print("\nLOADING DATA...")
    df = load_data()
    print(f"Loaded {len(df)} reviews")
    print(f"  - Human: {len(df[df['reviewer_type'] == 'Human'])}")
    print(f"  - LLM: {len(df[df['reviewer_type'] == 'LLM'])}")

    # Run all analyses
    all_results = {}

    all_results['overall'] = analyze_overall_performance(df)
    all_results['criteria'] = analyze_criteria_performance(df)
    exp_results, best_exp, worst_exp = analyze_experiment_impact(df)
    all_results['experiments'] = {
        'results': exp_results,
        'best': best_exp,
        'worst': worst_exp
    }
    model_results, model_ranking = analyze_model_performance(df)
    all_results['models'] = {
        'results': model_results,
        'ranked': model_ranking
    }
    all_results['reliability'] = analyze_inter_rater_reliability(df)
    all_results['recommendations'] = analyze_recommendation_agreement(df)

    # Generate summary
    generate_key_findings_summary(all_results)

    # Run detailed per-experiment analyses
    print("\n" + "="*80)
    print("RUNNING PER-EXPERIMENT DETAILED ANALYSES")
    print("="*80)

    experiment_definitions = {
        'baseline_v1': 'Experiment 1: Baseline (No Examples)',
        'with_training_data_v1': 'Experiment 2: Single Training Example',
        'multi_examples_v1': 'Experiment 3: Multiple Examples (4)',
        'strict_scoring_v1': 'Experiment 4: Strict Scoring Instructions'
    }

    experiment_detailed_results = {}

    for exp_name, exp_label in experiment_definitions.items():
        exp_detailed = analyze_experiment_detailed(df, exp_name, exp_label)
        experiment_detailed_results[exp_name] = exp_detailed

    all_results['experiment_detailed'] = experiment_detailed_results

    # Save results to JSON
    # Convert to serializable format
    serializable_results = {}
    for key, value in all_results.items():
        if key == 'experiments':
            serializable_results[key] = {
                'results': value['results'],
                'best_experiment': value['best'][0],
                'best_value': value['best'][1]
            }
        elif key == 'models':
            serializable_results[key] = {
                'results': value['results'],
                'ranked': [(name, data) for name, data in value['ranked']]
            }
        elif key == 'experiment_detailed':
            # Already in serializable format
            serializable_results[key] = value
        else:
            serializable_results[key] = value

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(serializable_results, f, indent=2)

    print(f"\n{'='*80}")
    print(f"✓ Analysis complete! Results saved to {OUTPUT_PATH}")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
