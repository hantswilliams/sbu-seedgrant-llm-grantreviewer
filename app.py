#!/usr/bin/env python3
"""
Flask application to display combined grant reviews and analytics.
"""

from flask import Flask, render_template, jsonify, request
import pandas as pd
import sqlite3
import json
from pathlib import Path

app = Flask(__name__)

# Experiments that use Daniel as training data and should exclude him from analysis
EXPERIMENTS_EXCLUDING_DANIEL = [
    'with_training_data_v1',
    'multi_examples_v1',
    'strict_scoring_v1'
]

def should_exclude_daniel(experiment_name):
    """Check if an experiment should exclude Daniel from LLM analysis."""
    return experiment_name in EXPERIMENTS_EXCLUDING_DANIEL

def get_combined_reviews(experiment_filter=None, exclude_daniel=False):
    """Load combined reviews from database with optional experiment filter.

    Args:
        experiment_filter: Optional experiment name to filter by
        exclude_daniel: If True, excludes Daniel from LLM reviews (used for experiments with training data)
    """
    db_path = Path("data/results.db")
    conn = sqlite3.connect(db_path)

    if experiment_filter:
        query = """
        SELECT * FROM combined_reviews
        WHERE prompt_experiment_name = ? OR reviewer_type = 'Human'
        ORDER BY applicant_name, reviewer_type, reviewer_id
        """
        df = pd.read_sql_query(query, conn, params=(experiment_filter,))
    else:
        query = """
        SELECT * FROM combined_reviews
        ORDER BY applicant_name, reviewer_type, reviewer_id
        """
        df = pd.read_sql_query(query, conn)

    # Exclude Daniel from LLM reviews if requested (for experiments using Daniel as training data)
    if exclude_daniel:
        df = df[~((df['applicant_name'] == 'DANIEL') & (df['reviewer_type'] == 'LLM'))]

    conn.close()
    return df

def get_grant_reviews(experiment_filter=None):
    """Load grant reviews from database with optional experiment filter."""
    db_path = Path("data/results.db")
    conn = sqlite3.connect(db_path)

    if experiment_filter:
        query = """
        SELECT * FROM grant_reviews
        WHERE prompt_experiment_name = ?
        ORDER BY applicant_name, iteration
        """
        df = pd.read_sql_query(query, conn, params=(experiment_filter,))
    else:
        query = """
        SELECT * FROM grant_reviews
        ORDER BY applicant_name, iteration
        """
        df = pd.read_sql_query(query, conn)

    conn.close()
    return df

def get_available_experiments():
    """Get list of unique experiments from database in specified order with descriptions."""
    db_path = Path("data/results.db")
    conn = sqlite3.connect(db_path)

    query = """
    SELECT DISTINCT prompt_experiment_name, prompt_version
    FROM grant_reviews
    WHERE prompt_experiment_name IS NOT NULL
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Define experiment order and descriptions
    experiment_info = {
        'baseline_v1': {
            'order': 1,
            'description': 'Original prompt without training examples - baseline for comparison'
        },
        'with_training_data_v1': {
            'order': 2,
            'description': 'Prompt with 1 training example (Daniel\'s data). Excludes Daniel from LLM analysis to prevent data leakage.'
        },
        'multi_examples_v1': {
            'order': 3,
            'description': 'Prompt with all 4 human reviews of Daniel as training examples. Excludes Daniel from LLM analysis.'
        },
        'strict_scoring_v1': {
            'order': 4,
            'description': 'Prompt with 1 training example (Daniel\'s data) and strict wording emphasizing critical evaluation and conservative scoring. Excludes Daniel from LLM analysis.'
        }
    }

    # Add order and descriptions to experiments
    experiments = []
    for _, row in df.iterrows():
        exp_name = row['prompt_experiment_name']
        exp_dict = {
            'prompt_experiment_name': exp_name,
            'prompt_version': row['prompt_version'],
            'order': experiment_info.get(exp_name, {}).get('order', 999),
            'description': experiment_info.get(exp_name, {}).get('description', '')
        }
        experiments.append(exp_dict)

    # Sort by order
    experiments.sort(key=lambda x: x['order'])

    return experiments

def get_summary_stats(df):
    """Generate summary statistics for the dashboard."""
    stats = {
        'total_reviews': len(df),
        'human_reviews': len(df[df['reviewer_type'] == 'Human']),
        'llm_reviews': len(df[df['reviewer_type'] == 'LLM']),
        'unique_applicants': df['applicant_name'].nunique(),
        'unique_reviewers': df['reviewer_id'].nunique()
    }

    # Calculate detailed descriptive statistics for each criterion
    score_columns = [
        'innovation_impact', 'methodological_approach', 'research_team_strength',
        'external_funding_potential', 'budget_clarity', 'presentation_quality', 'total_score'
    ]

    criterion_stats = {}
    for reviewer_type in ['Human', 'LLM']:
        subset = df[df['reviewer_type'] == reviewer_type]
        if len(subset) > 0:
            criterion_stats[reviewer_type] = {}
            for col in score_columns:
                if col in subset.columns and subset[col].notna().any():
                    criterion_stats[reviewer_type][col] = {
                        'mean': round(subset[col].mean(), 2),
                        'median': round(subset[col].median(), 2),
                        'std': round(subset[col].std(), 2),
                        'min': round(subset[col].min(), 2),
                        'max': round(subset[col].max(), 2),
                        'q1': round(subset[col].quantile(0.25), 2),
                        'q3': round(subset[col].quantile(0.75), 2),
                        'count': int(subset[col].count())
                    }

    stats['criterion_stats'] = criterion_stats
    
    # Applicant coverage
    applicant_coverage = []
    for applicant in df['applicant_name'].unique():
        applicant_data = df[df['applicant_name'] == applicant]
        human_count = len(applicant_data[applicant_data['reviewer_type'] == 'Human'])
        llm_count = len(applicant_data[applicant_data['reviewer_type'] == 'LLM'])
        
        applicant_coverage.append({
            'name': applicant,
            'total': len(applicant_data),
            'human': human_count,
            'llm': llm_count
        })
    
    stats['applicant_coverage'] = applicant_coverage
    
    # Score statistics
    score_stats = {}
    for reviewer_type in ['Human', 'LLM']:
        subset = df[df['reviewer_type'] == reviewer_type]
        if len(subset) > 0:
            score_stats[reviewer_type] = {
                'mean_total': round(subset['total_score'].mean(), 1) if subset['total_score'].notna().any() else 0,
                'min_total': subset['total_score'].min() if subset['total_score'].notna().any() else 0,
                'max_total': subset['total_score'].max() if subset['total_score'].notna().any() else 0,
                'count': len(subset)
            }
    
    stats['score_stats'] = score_stats
    
    # Recommendation distribution
    rec_dist = df['overall_recommendation'].value_counts().to_dict()
    stats['recommendation_distribution'] = rec_dist
    
    return stats

@app.route('/')
def dashboard():
    """Main dashboard page."""
    experiment_filter = request.args.get('experiment', None)
    exclude_daniel = should_exclude_daniel(experiment_filter) if experiment_filter else False
    df = get_combined_reviews(experiment_filter=experiment_filter, exclude_daniel=exclude_daniel)
    stats = get_summary_stats(df)
    experiments = get_available_experiments()
    return render_template('dashboard.html', stats=stats, experiments=experiments, selected_experiment=experiment_filter)

@app.route('/reviews')
def reviews():
    """Detailed reviews table page."""
    experiment_filter = request.args.get('experiment', None)
    exclude_daniel = should_exclude_daniel(experiment_filter) if experiment_filter else False
    df = get_combined_reviews(experiment_filter=experiment_filter, exclude_daniel=exclude_daniel)

    # Convert DataFrame to list of dictionaries for template
    reviews_data = df.to_dict('records')
    experiments = get_available_experiments()

    return render_template('reviews.html', reviews=reviews_data, experiments=experiments, selected_experiment=experiment_filter)

@app.route('/applicant/<applicant_name>')
def applicant_detail(applicant_name):
    """Detailed view for a specific applicant."""
    experiment_filter = request.args.get('experiment', None)
    exclude_daniel = should_exclude_daniel(experiment_filter) if experiment_filter else False
    df = get_combined_reviews(experiment_filter=experiment_filter, exclude_daniel=exclude_daniel)
    applicant_data = df[df['applicant_name'] == applicant_name.upper()]

    if len(applicant_data) == 0:
        return "Applicant not found", 404

    # Separate human and LLM reviews
    human_reviews = applicant_data[applicant_data['reviewer_type'] == 'Human']
    llm_reviews = applicant_data[applicant_data['reviewer_type'] == 'LLM']

    # Get available experiments for this applicant
    experiments_for_applicant = llm_reviews['prompt_experiment_name'].dropna().unique().tolist() if len(llm_reviews) > 0 else []

    # Group LLM reviews by vendor
    llm_by_vendor = {}
    for vendor in llm_reviews['vendor'].dropna().unique():
        if vendor.strip():
            vendor_reviews = llm_reviews[llm_reviews['vendor'] == vendor]
            llm_by_vendor[vendor] = vendor_reviews.to_dict('records')

    # Calculate average scores by criterion
    score_columns = [
        'innovation_impact', 'methodological_approach', 'research_team_strength',
        'external_funding_potential', 'budget_clarity', 'presentation_quality'
    ]

    criterion_names = [
        'Innovation & Impact', 'Methodological Approach', 'Research Team Strength',
        'External Funding Potential', 'Budget Clarity', 'Presentation Quality'
    ]

    human_avg = []
    vendor_averages = {}

    for col in score_columns:
        if len(human_reviews) > 0:
            human_avg.append(round(human_reviews[col].mean(), 1) if human_reviews[col].notna().any() else 0)
        else:
            human_avg.append(0)

        # Calculate averages for each vendor
        for vendor in llm_by_vendor.keys():
            vendor_data = llm_reviews[llm_reviews['vendor'] == vendor]
            if vendor not in vendor_averages:
                vendor_averages[vendor] = []
            if len(vendor_data) > 0:
                vendor_averages[vendor].append(round(vendor_data[col].mean(), 1) if vendor_data[col].notna().any() else 0)
            else:
                vendor_averages[vendor].append(0)

    # Also keep overall LLM average for backwards compatibility
    llm_avg = []
    for col in score_columns:
        if len(llm_reviews) > 0:
            llm_avg.append(round(llm_reviews[col].mean(), 1) if llm_reviews[col].notna().any() else 0)
        else:
            llm_avg.append(0)

    comparison_data = {
        'criteria': criterion_names,
        'human_avg': human_avg,
        'llm_avg': llm_avg,
        'vendor_averages': vendor_averages,
        'available_vendors': list(llm_by_vendor.keys())
    }

    # Get experiment comparison data if multiple experiments exist
    experiment_comparison = {}
    if len(experiments_for_applicant) > 1:
        for experiment in experiments_for_applicant:
            exp_reviews = llm_reviews[llm_reviews['prompt_experiment_name'] == experiment]
            exp_avg = []
            for col in score_columns:
                if len(exp_reviews) > 0:
                    exp_avg.append(round(exp_reviews[col].mean(), 1) if exp_reviews[col].notna().any() else 0)
                else:
                    exp_avg.append(0)
            experiment_comparison[experiment] = exp_avg

    # Calculate detailed descriptive statistics for this applicant
    applicant_criterion_stats = {}
    for reviewer_type in ['Human', 'LLM']:
        subset = applicant_data[applicant_data['reviewer_type'] == reviewer_type]
        if len(subset) > 0:
            applicant_criterion_stats[reviewer_type] = {}
            all_score_columns = score_columns + ['total_score']
            for col in all_score_columns:
                if col in subset.columns and subset[col].notna().any():
                    applicant_criterion_stats[reviewer_type][col] = {
                        'mean': round(subset[col].mean(), 2),
                        'median': round(subset[col].median(), 2),
                        'std': round(subset[col].std(), 2),
                        'min': round(subset[col].min(), 2),
                        'max': round(subset[col].max(), 2),
                        'q1': round(subset[col].quantile(0.25), 2),
                        'q3': round(subset[col].quantile(0.75), 2),
                        'count': int(subset[col].count())
                    }

    return render_template('applicant_detail.html',
                         applicant=applicant_name.upper(),
                         human_reviews=human_reviews.to_dict('records'),
                         llm_reviews=llm_reviews.to_dict('records'),
                         llm_by_vendor=llm_by_vendor,
                         comparison=comparison_data,
                         experiments_available=experiments_for_applicant,
                         experiment_comparison=experiment_comparison,
                         selected_experiment=experiment_filter,
                         applicant_stats=applicant_criterion_stats)

@app.route('/api/chart_data')
def chart_data():
    """API endpoint for chart data."""
    experiment_filter = request.args.get('experiment', None)
    exclude_daniel = should_exclude_daniel(experiment_filter) if experiment_filter else False
    df = get_combined_reviews(experiment_filter=experiment_filter, exclude_daniel=exclude_daniel)
    chart_type = request.args.get('type', 'scores')

    if chart_type == 'scores':
        # Score comparison by reviewer type
        human_scores = df[df['reviewer_type'] == 'Human']['total_score'].dropna().tolist()
        llm_scores = df[df['reviewer_type'] == 'LLM']['total_score'].dropna().tolist()

        return jsonify({
            'human_scores': human_scores,
            'llm_scores': llm_scores,
            'excludes_daniel': exclude_daniel
        })

    elif chart_type == 'recommendations':
        # Recommendation distribution
        rec_dist = df['overall_recommendation'].value_counts().to_dict()
        return jsonify(rec_dist)

    elif chart_type == 'applicant_scores':
        # Average scores by applicant
        applicant_scores = {}
        for applicant in df['applicant_name'].unique():
            applicant_data = df[df['applicant_name'] == applicant]
            human_avg = applicant_data[applicant_data['reviewer_type'] == 'Human']['total_score'].mean()
            llm_avg = applicant_data[applicant_data['reviewer_type'] == 'LLM']['total_score'].mean()

            applicant_scores[applicant] = {
                'human': round(human_avg, 1) if pd.notna(human_avg) else None,
                'llm': round(llm_avg, 1) if pd.notna(llm_avg) else None
            }

        return jsonify(applicant_scores)

    return jsonify({'error': 'Invalid chart type'})

@app.route('/api/criteria_comparison')
def criteria_comparison():
    """API endpoint for criteria comparison data."""
    experiment_filter = request.args.get('experiment', None)
    exclude_daniel = should_exclude_daniel(experiment_filter) if experiment_filter else False
    df = get_combined_reviews(experiment_filter=experiment_filter, exclude_daniel=exclude_daniel)

    score_columns = [
        'innovation_impact', 'methodological_approach', 'research_team_strength',
        'external_funding_potential', 'budget_clarity', 'presentation_quality'
    ]

    criterion_names = [
        'Innovation & Impact', 'Methodological Approach', 'Research Team Strength',
        'External Funding Potential', 'Budget Clarity', 'Presentation Quality'
    ]

    human_data = df[df['reviewer_type'] == 'Human']
    llm_data = df[df['reviewer_type'] == 'LLM']

    human_means = [round(human_data[col].mean(), 1) if human_data[col].notna().any() else 0 for col in score_columns]
    llm_means = [round(llm_data[col].mean(), 1) if llm_data[col].notna().any() else 0 for col in score_columns]

    return jsonify({
        'criteria': criterion_names,
        'human_means': human_means,
        'llm_means': llm_means,
        'excludes_daniel': exclude_daniel
    })

@app.route('/api/experiments')
def get_experiments_api():
    """API endpoint for available experiments."""
    experiments = get_available_experiments()
    return jsonify(experiments)

@app.route('/experiments')
def experiments_page():
    """Experiment comparison page."""
    experiments = get_available_experiments()

    # Calculate detailed stats for each experiment
    db_path = Path("data/results.db")
    conn = sqlite3.connect(db_path)

    # Use ordered dict to maintain experiment order
    from collections import OrderedDict
    experiment_detailed_stats = OrderedDict()

    for exp in experiments:
        exp_name = exp['prompt_experiment_name']

        # Determine if we should exclude Daniel for this experiment
        exclude_daniel = should_exclude_daniel(exp_name)

        # Get all reviews for this experiment
        if exclude_daniel:
            # Exclude Daniel from LLM reviews for experiments using him as training data
            query = """
            SELECT
                innovation_impact, methodological_approach, research_team_strength,
                external_funding_potential, budget_clarity, presentation_quality, total_score
            FROM combined_reviews
            WHERE prompt_experiment_name = ? AND reviewer_type = 'LLM'
                AND applicant_name != 'DANIEL'
            """
        else:
            query = """
            SELECT
                innovation_impact, methodological_approach, research_team_strength,
                external_funding_potential, budget_clarity, presentation_quality, total_score
            FROM combined_reviews
            WHERE prompt_experiment_name = ? AND reviewer_type = 'LLM'
            """
        df = pd.read_sql_query(query, conn, params=(exp_name,))

        if len(df) > 0:
            stats = {}
            for col in df.columns:
                if df[col].notna().any():
                    stats[col] = {
                        'mean': round(df[col].mean(), 2),
                        'median': round(df[col].median(), 2),
                        'std': round(df[col].std(), 2),
                        'min': round(df[col].min(), 2),
                        'max': round(df[col].max(), 2),
                        'q1': round(df[col].quantile(0.25), 2),
                        'q3': round(df[col].quantile(0.75), 2),
                        'count': int(df[col].count())
                    }
            experiment_detailed_stats[exp_name] = stats

    conn.close()

    return render_template('experiments.html',
                          experiments=experiments,
                          experiment_detailed_stats=experiment_detailed_stats)

@app.route('/api/experiment_comparison')
def experiment_comparison():
    """API endpoint for comparing different prompt experiments."""
    db_path = Path("data/results.db")
    conn = sqlite3.connect(db_path)

    # Get all unique experiments first
    experiments_query = """
    SELECT DISTINCT prompt_experiment_name
    FROM grant_reviews
    WHERE prompt_experiment_name IS NOT NULL
    """
    experiments_df = pd.read_sql_query(experiments_query, conn)

    # Prepare data for chart
    experiments_data = {}
    for exp_name in experiments_df['prompt_experiment_name']:
        exclude_daniel = should_exclude_daniel(exp_name)

        # Build query based on whether to exclude Daniel
        if exclude_daniel:
            query = """
            SELECT
                gr.prompt_experiment_name,
                grc.criterion_name,
                AVG(grc.score) as avg_score
            FROM grant_reviews gr
            JOIN grant_review_criteria grc ON gr.id = grc.grant_review_id
            WHERE gr.prompt_experiment_name = ?
                AND gr.applicant_name != 'Daniel'
            GROUP BY gr.prompt_experiment_name, grc.criterion_name
            ORDER BY grc.criterion_name
            """
        else:
            query = """
            SELECT
                gr.prompt_experiment_name,
                grc.criterion_name,
                AVG(grc.score) as avg_score
            FROM grant_reviews gr
            JOIN grant_review_criteria grc ON gr.id = grc.grant_review_id
            WHERE gr.prompt_experiment_name = ?
            GROUP BY gr.prompt_experiment_name, grc.criterion_name
            ORDER BY grc.criterion_name
            """

        exp_data = pd.read_sql_query(query, conn, params=(exp_name,))
        if len(exp_data) > 0:
            experiments_data[exp_name] = {
                'criteria': exp_data['criterion_name'].tolist(),
                'scores': exp_data['avg_score'].tolist(),
                'excludes_daniel': exclude_daniel
            }

    conn.close()
    return jsonify(experiments_data)

@app.route('/api/experiment_stats')
def experiment_stats():
    """API endpoint for experiment statistics comparison."""
    db_path = Path("data/results.db")
    conn = sqlite3.connect(db_path)

    # Get all unique experiments first
    experiments_query = """
    SELECT DISTINCT prompt_experiment_name, prompt_version
    FROM combined_reviews
    WHERE reviewer_type = 'LLM' AND prompt_experiment_name IS NOT NULL
    """
    experiments_df = pd.read_sql_query(experiments_query, conn)

    result = {}
    for _, exp_row in experiments_df.iterrows():
        exp_name = exp_row['prompt_experiment_name']
        exclude_daniel = should_exclude_daniel(exp_name)

        # Build query based on whether to exclude Daniel
        if exclude_daniel:
            query = """
            SELECT
                cr.prompt_experiment_name,
                cr.prompt_version,
                AVG(cr.total_score) as avg_total_score,
                MIN(cr.total_score) as min_total_score,
                MAX(cr.total_score) as max_total_score,
                COUNT(*) as review_count,
                cr.overall_recommendation,
                COUNT(*) as recommendation_count
            FROM combined_reviews cr
            WHERE cr.reviewer_type = 'LLM'
                AND cr.prompt_experiment_name = ?
                AND cr.applicant_name != 'DANIEL'
            GROUP BY cr.prompt_experiment_name, cr.prompt_version, cr.overall_recommendation
            ORDER BY cr.overall_recommendation
            """
        else:
            query = """
            SELECT
                cr.prompt_experiment_name,
                cr.prompt_version,
                AVG(cr.total_score) as avg_total_score,
                MIN(cr.total_score) as min_total_score,
                MAX(cr.total_score) as max_total_score,
                COUNT(*) as review_count,
                cr.overall_recommendation,
                COUNT(*) as recommendation_count
            FROM combined_reviews cr
            WHERE cr.reviewer_type = 'LLM'
                AND cr.prompt_experiment_name = ?
            GROUP BY cr.prompt_experiment_name, cr.prompt_version, cr.overall_recommendation
            ORDER BY cr.overall_recommendation
            """

        exp_data = pd.read_sql_query(query, conn, params=(exp_name,))

        if len(exp_data) > 0:
            result[exp_name] = {
                'version': exp_data['prompt_version'].iloc[0],
                'avg_score': float(exp_data['avg_total_score'].mean()),
                'min_score': float(exp_data['min_total_score'].min()),
                'max_score': float(exp_data['max_total_score'].max()),
                'total_reviews': int(exp_data['review_count'].sum()),
                'recommendations': exp_data.set_index('overall_recommendation')['recommendation_count'].to_dict(),
                'excludes_daniel': exclude_daniel
            }

    conn.close()
    return jsonify(result)

@app.route('/api/model_comparison')
def model_comparison():
    """API endpoint for model-specific criteria comparison data."""
    experiment_filter = request.args.get('experiment', None)

    # Determine if we should exclude Daniel
    exclude_daniel = should_exclude_daniel(experiment_filter) if experiment_filter else False

    # Use get_combined_reviews with appropriate exclusion
    df = get_combined_reviews(experiment_filter=experiment_filter, exclude_daniel=exclude_daniel)

    score_columns = [
        'innovation_impact', 'methodological_approach', 'research_team_strength',
        'external_funding_potential', 'budget_clarity', 'presentation_quality'
    ]

    criterion_names = [
        'Innovation & Impact', 'Methodological Approach', 'Research Team Strength',
        'External Funding Potential', 'Budget Clarity', 'Presentation Quality'
    ]

    # Get data for each reviewer category
    human_data = df[df['reviewer_type'] == 'Human']

    # Dynamically detect available LLM models by vendor
    llm_data = df[df['reviewer_type'] == 'LLM']

    # Get unique vendor-model combinations
    model_groups = {}
    datasets = []
    counts = {'human': len(human_data)}

    # Add human data
    human_means = [round(human_data[col].mean(), 1) if human_data[col].notna().any() else 0 for col in score_columns]

    # Group LLM data by vendor
    for vendor in llm_data['vendor'].dropna().unique():
        if vendor.strip():  # Skip empty vendor names
            vendor_data = llm_data[llm_data['vendor'] == vendor]
            vendor_key = vendor.lower().replace(' ', '_')

            if len(vendor_data) > 0:
                vendor_means = [round(vendor_data[col].mean(), 1) if vendor_data[col].notna().any() else 0 for col in score_columns]
                model_groups[vendor_key] = {
                    'name': vendor,
                    'means': vendor_means,
                    'count': len(vendor_data)
                }
                counts[vendor_key] = len(vendor_data)

    # Also check for specific models if needed
    openai_data = llm_data[llm_data['vendor'].str.contains('openai', case=False, na=False)]
    google_data = llm_data[llm_data['vendor'].str.contains('google', case=False, na=False)]
    xai_data = llm_data[llm_data['vendor'].str.contains('xai', case=False, na=False)]
    anthropic_data = llm_data[llm_data['vendor'].str.contains('anthropic', case=False, na=False)]

    # Build response with available models
    response_data = {
        'criteria': criterion_names,
        'human_means': human_means,
        'counts': counts
    }

    # Add vendor-specific data
    for vendor_key, vendor_info in model_groups.items():
        response_data[f'{vendor_key}_means'] = vendor_info['means']

    # Maintain backwards compatibility with existing chart code
    if 'openai' in model_groups:
        response_data['openai_means'] = model_groups['openai']['means']
    if 'google' in model_groups:
        response_data['google_means'] = model_groups['google']['means']
    if 'xai' in model_groups:
        response_data['xai_means'] = model_groups['xai']['means']
    if 'anthropic' in model_groups:
        response_data['anthropic_means'] = model_groups['anthropic']['means']

    response_data['available_vendors'] = list(model_groups.keys())

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5004, host='0.0.0.0')