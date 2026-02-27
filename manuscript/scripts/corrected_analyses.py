#!/usr/bin/env python3
"""
Corrected analyses addressing peer review major concerns.

Computes:
1. Cell-mean aggregated statistics (addressing pseudoreplication, Major 4.1/4.2)
2. Glass's delta using human SD (addressing Moderate 5.1)
3. Cohen's kappa for recommendation agreement (addressing Moderate 5.2)
4. Holm-corrected p-values for criterion-level tests (addressing Major 4.5)
5. Application-level descriptive statistics
"""

import sqlite3
import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats
from sklearn.metrics import cohen_kappa_score
import json

BASE_PATH = Path(__file__).parent.parent.parent
DB_PATH = BASE_PATH / "data" / "results.db"

EXPERIMENTS = {
    'baseline_v1': {
        'name': 'Experiment 1: Zero-Shot',
        'exclude_daniel': False
    },
    'multi_examples_v1': {
        'name': 'Experiment 2: Few-Shot',
        'exclude_daniel': True
    },
    'strict_scoring_v1': {
        'name': 'Experiment 3: Few-Shot + Strict',
        'exclude_daniel': True
    }
}

CRITERIA = {
    'innovation_impact': 'Innovation & Impact',
    'methodological_approach': 'Methodology & Feasibility',
    'research_team_strength': 'Team Strength',
    'external_funding_potential': 'External Funding Potential',
    'budget_clarity': 'Budget Clarity',
    'presentation_quality': 'Presentation Quality'
}

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM combined_reviews", conn)
    conn.close()
    return df

def holm_correction(p_values):
    """Apply Holm-Bonferroni correction to a list of p-values."""
    n = len(p_values)
    sorted_indices = np.argsort(p_values)
    sorted_p = np.array(p_values)[sorted_indices]
    corrected = np.zeros(n)
    for i, p in enumerate(sorted_p):
        corrected[i] = min(p * (n - i), 1.0)
    # Enforce monotonicity
    for i in range(1, n):
        corrected[i] = max(corrected[i], corrected[i-1])
    # Map back to original order
    result = np.zeros(n)
    for i, idx in enumerate(sorted_indices):
        result[idx] = corrected[i]
    return result

def filter_experiment(df, exp_key):
    config = EXPERIMENTS[exp_key]
    llm = df[(df['reviewer_type'] == 'LLM') & (df['prompt_experiment_name'] == exp_key)].copy()
    human = df[df['reviewer_type'] == 'Human'].copy()
    if config['exclude_daniel']:
        llm = llm[llm['applicant_name'] != 'DANIEL']
        human = human[human['applicant_name'] != 'DANIEL']
    return pd.concat([human, llm], ignore_index=True)

def compute_aggregated_analysis(df_exp):
    """
    Aggregate LLM iterations within vendor-application cells,
    then compare cell means to human scores.
    """
    human = df_exp[df_exp['reviewer_type'] == 'Human']
    llm = df_exp[df_exp['reviewer_type'] == 'LLM']

    # Aggregate: mean of 3 iterations per vendor-application cell
    llm_cell_means = llm.groupby(['vendor', 'applicant_name'])['total_score'].mean().reset_index()

    human_scores = human['total_score'].values
    llm_agg_scores = llm_cell_means['total_score'].values

    h_mean = human_scores.mean()
    h_std = human_scores.std(ddof=1)
    l_mean = llm_agg_scores.mean()
    l_std = llm_agg_scores.std(ddof=1)

    diff = l_mean - h_mean

    # t-test on aggregated data
    t_stat, p_value = stats.ttest_ind(human_scores, llm_agg_scores)

    # Glass's delta (human SD as reference)
    glass_d = diff / h_std if h_std > 0 else np.nan

    # Also compute pooled Cohen's d for comparison
    pooled_sd = np.sqrt(((len(human_scores)-1)*h_std**2 + (len(llm_agg_scores)-1)*l_std**2) /
                        (len(human_scores) + len(llm_agg_scores) - 2))
    cohens_d = diff / pooled_sd if pooled_sd > 0 else np.nan

    return {
        'human_n': len(human_scores),
        'llm_n_raw': len(llm),
        'llm_n_aggregated': len(llm_agg_scores),
        'human_mean': h_mean,
        'human_std': h_std,
        'llm_mean_aggregated': l_mean,
        'llm_std_aggregated': l_std,
        'llm_mean_raw': llm['total_score'].mean(),
        'llm_std_raw': llm['total_score'].std(ddof=1),
        'difference': diff,
        't_stat': t_stat,
        'p_value': p_value,
        'glass_delta': glass_d,
        'cohens_d_pooled': cohens_d,
        'llm_cell_means': llm_cell_means
    }

def compute_application_level_stats(df_exp):
    """Compute application-level summary statistics."""
    human = df_exp[df_exp['reviewer_type'] == 'Human']
    llm = df_exp[df_exp['reviewer_type'] == 'LLM']

    apps = sorted(df_exp['applicant_name'].unique())
    results = {}

    for app in apps:
        h_scores = human[human['applicant_name'] == app]['total_score']
        l_scores = llm[llm['applicant_name'] == app]['total_score']

        results[app] = {
            'human_mean': h_scores.mean(),
            'human_std': h_scores.std(ddof=1),
            'human_n': len(h_scores),
            'llm_mean': l_scores.mean(),
            'llm_std': l_scores.std(ddof=1),
            'llm_n': len(l_scores),
            'diff': l_scores.mean() - h_scores.mean()
        }

    return results

def compute_criterion_with_holm(df_exp):
    """Compute criterion-level analyses with Holm correction."""
    human = df_exp[df_exp['reviewer_type'] == 'Human']
    llm = df_exp[df_exp['reviewer_type'] == 'LLM']

    results = {}
    p_values = []
    criterion_keys = []

    for criterion, label in CRITERIA.items():
        h_scores = human[criterion].dropna()
        l_scores = llm[criterion].dropna()

        if len(h_scores) > 1 and len(l_scores) > 1:
            # Aggregate LLM iterations within vendor-application cells
            llm_cell = llm.groupby(['vendor', 'applicant_name'])[criterion].mean()

            diff = l_scores.mean() - h_scores.mean()
            t_stat, p_val = stats.ttest_ind(h_scores, llm_cell.values)

            results[criterion] = {
                'label': label,
                'human_mean': h_scores.mean(),
                'llm_mean': l_scores.mean(),
                'difference': diff,
                't_stat': t_stat,
                'p_value_uncorrected': p_val,
            }
            p_values.append(p_val)
            criterion_keys.append(criterion)

    # Apply Holm correction
    if p_values:
        corrected = holm_correction(p_values)
        for i, key in enumerate(criterion_keys):
            results[key]['p_value_holm'] = corrected[i]
            results[key]['significant_uncorrected'] = p_values[i] < 0.05
            results[key]['significant_holm'] = corrected[i] < 0.05

    return results

def compute_cohens_kappa(df_exp):
    """Compute Cohen's kappa for recommendation agreement."""
    human = df_exp[df_exp['reviewer_type'] == 'Human']
    llm = df_exp[df_exp['reviewer_type'] == 'LLM']

    def broad_category(rec):
        if pd.isna(rec):
            return None
        rec = str(rec).lower().strip()
        if 'do not fund' in rec:
            return 'negative'
        return 'positive'

    # Create all human-LLM pairs for each application
    pairs_exact = []
    pairs_broad = []

    apps = df_exp['applicant_name'].unique()
    for app in apps:
        h_recs = human[human['applicant_name'] == app]['overall_recommendation'].dropna()
        l_recs = llm[llm['applicant_name'] == app]['overall_recommendation'].dropna()

        for h_rec in h_recs:
            for l_rec in l_recs:
                h_str = str(h_rec).strip().lower()
                l_str = str(l_rec).strip().lower()
                pairs_exact.append((h_str, l_str))
                pairs_broad.append((broad_category(h_rec), broad_category(l_rec)))

    result = {}
    if pairs_exact:
        y1_exact, y2_exact = zip(*pairs_exact)
        result['kappa_exact'] = cohen_kappa_score(y1_exact, y2_exact)
        result['n_pairs_exact'] = len(pairs_exact)

        y1_broad, y2_broad = zip(*pairs_broad)
        result['kappa_broad'] = cohen_kappa_score(y1_broad, y2_broad)
        result['n_pairs_broad'] = len(pairs_broad)

    return result

def compute_aggregated_anova(all_agg):
    """Compute ANOVA on aggregated cell means across experiments."""
    groups = []
    for exp_key in ['baseline_v1', 'multi_examples_v1', 'strict_scoring_v1']:
        cell_means = all_agg[exp_key]['llm_cell_means']['total_score'].values
        groups.append(cell_means)

    f_stat, p_val = stats.f_oneway(*groups)
    total_n = sum(len(g) for g in groups)
    k = len(groups)

    return {
        'f_stat': f_stat,
        'p_value': p_val,
        'df_between': k - 1,
        'df_within': total_n - k,
        'group_sizes': [len(g) for g in groups]
    }

def main():
    print("=" * 70)
    print("CORRECTED ANALYSES - Addressing Peer Review Concerns")
    print("=" * 70)

    df = load_data()

    all_results = {}
    all_agg = {}

    for exp_key, config in EXPERIMENTS.items():
        print(f"\n{'='*50}")
        print(f"{config['name']}")
        print(f"{'='*50}")

        df_exp = filter_experiment(df, exp_key)

        # 1. Aggregated analysis
        agg = compute_aggregated_analysis(df_exp)
        all_agg[exp_key] = agg

        print(f"\n--- AGGREGATED ANALYSIS (cell means) ---")
        print(f"Human: n={agg['human_n']}, mean={agg['human_mean']:.2f} ± {agg['human_std']:.2f}")
        print(f"LLM (raw): n={agg['llm_n_raw']}, mean={agg['llm_mean_raw']:.2f} ± {agg['llm_std_raw']:.2f}")
        print(f"LLM (aggregated cells): n={agg['llm_n_aggregated']}, mean={agg['llm_mean_aggregated']:.2f} ± {agg['llm_std_aggregated']:.2f}")
        print(f"Difference: {agg['difference']:+.2f}")
        print(f"t-test (aggregated): t={agg['t_stat']:.3f}, p={agg['p_value']:.4f}")
        print(f"Glass's delta: {agg['glass_delta']:.3f}")
        print(f"Cohen's d (pooled): {agg['cohens_d_pooled']:.3f}")

        # 2. Application-level stats
        app_stats = compute_application_level_stats(df_exp)
        print(f"\n--- APPLICATION-LEVEL STATS ---")
        for app, s in app_stats.items():
            print(f"  {app}: Human={s['human_mean']:.1f}±{s['human_std']:.1f}, LLM={s['llm_mean']:.1f}±{s['llm_std']:.1f}, diff={s['diff']:+.1f}")

        # 3. Criterion-level with Holm correction
        criteria = compute_criterion_with_holm(df_exp)
        print(f"\n--- CRITERION-LEVEL (with Holm correction) ---")
        for crit, data in criteria.items():
            sig_raw = "*" if data['significant_uncorrected'] else ""
            sig_holm = "**" if data['significant_holm'] else ""
            print(f"  {data['label']}: diff={data['difference']:+.2f}, p_uncorr={data['p_value_uncorrected']:.4f}{sig_raw}, p_holm={data['p_value_holm']:.4f}{sig_holm}")

        # 4. Cohen's kappa
        kappa = compute_cohens_kappa(df_exp)
        print(f"\n--- COHEN'S KAPPA ---")
        if kappa:
            print(f"  Exact kappa: {kappa['kappa_exact']:.3f} (n_pairs={kappa['n_pairs_exact']})")
            print(f"  Broad kappa: {kappa['kappa_broad']:.3f} (n_pairs={kappa['n_pairs_broad']})")

        all_results[exp_key] = {
            'aggregated': {k: v for k, v in agg.items() if k != 'llm_cell_means'},
            'application_level': app_stats,
            'criteria_holm': {k: v for k, v in criteria.items()},
            'kappa': kappa
        }

    # 5. ANOVA on aggregated data
    print(f"\n{'='*50}")
    print("CROSS-EXPERIMENT ANOVA (aggregated cell means)")
    print(f"{'='*50}")
    anova = compute_aggregated_anova(all_agg)
    print(f"F({anova['df_between']},{anova['df_within']}) = {anova['f_stat']:.2f}, p = {anova['p_value']:.4f}")
    print(f"Group sizes: {anova['group_sizes']}")
    all_results['anova_aggregated'] = anova

    # 6. LLM rank order vs human rank order
    print(f"\n{'='*50}")
    print("APPLICATION RANK ORDER COMPARISON")
    print(f"{'='*50}")
    for exp_key, config in EXPERIMENTS.items():
        df_exp = filter_experiment(df, exp_key)
        human = df_exp[df_exp['reviewer_type'] == 'Human']
        llm = df_exp[df_exp['reviewer_type'] == 'LLM']

        h_by_app = human.groupby('applicant_name')['total_score'].mean().sort_values(ascending=False)
        l_by_app = llm.groupby('applicant_name')['total_score'].mean().sort_values(ascending=False)

        h_rank = list(h_by_app.index)
        l_rank = list(l_by_app.index)
        match = h_rank == l_rank

        print(f"\n{config['name']}:")
        print(f"  Human rank: {h_rank} (scores: {[f'{v:.1f}' for v in h_by_app.values]})")
        print(f"  LLM rank:   {l_rank} (scores: {[f'{v:.1f}' for v in l_by_app.values]})")
        print(f"  Rank match: {match}")

    # Save all results
    def make_serializable(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        elif isinstance(obj, (np.floating,)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [make_serializable(i) for i in obj]
        elif pd.isna(obj):
            return None
        return obj

    output_path = Path(__file__).parent / "output_corrected"
    output_path.mkdir(exist_ok=True)

    with open(output_path / 'corrected_analyses.json', 'w') as f:
        json.dump(make_serializable(all_results), f, indent=2)

    print(f"\nResults saved to {output_path / 'corrected_analyses.json'}")

if __name__ == "__main__":
    main()
