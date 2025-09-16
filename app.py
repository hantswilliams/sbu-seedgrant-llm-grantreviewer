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

def get_combined_reviews():
    """Load combined reviews from database."""
    db_path = Path("data/results.db")
    conn = sqlite3.connect(db_path)
    
    query = """
    SELECT * FROM combined_reviews
    ORDER BY applicant_name, reviewer_type, reviewer_id
    """
    
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def get_summary_stats(df):
    """Generate summary statistics for the dashboard."""
    stats = {
        'total_reviews': len(df),
        'human_reviews': len(df[df['reviewer_type'] == 'Human']),
        'llm_reviews': len(df[df['reviewer_type'] == 'LLM']),
        'unique_applicants': df['applicant_name'].nunique(),
        'unique_reviewers': df['reviewer_id'].nunique()
    }
    
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
    df = get_combined_reviews()
    stats = get_summary_stats(df)
    return render_template('dashboard.html', stats=stats)

@app.route('/reviews')
def reviews():
    """Detailed reviews table page."""
    df = get_combined_reviews()
    
    # Convert DataFrame to list of dictionaries for template
    reviews_data = df.to_dict('records')
    
    return render_template('reviews.html', reviews=reviews_data)

@app.route('/applicant/<applicant_name>')
def applicant_detail(applicant_name):
    """Detailed view for a specific applicant."""
    df = get_combined_reviews()
    applicant_data = df[df['applicant_name'] == applicant_name.upper()]
    
    if len(applicant_data) == 0:
        return "Applicant not found", 404
    
    # Separate human and LLM reviews
    human_reviews = applicant_data[applicant_data['reviewer_type'] == 'Human']
    llm_reviews = applicant_data[applicant_data['reviewer_type'] == 'LLM']
    
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
    llm_avg = []
    
    for col in score_columns:
        if len(human_reviews) > 0:
            human_avg.append(round(human_reviews[col].mean(), 1) if human_reviews[col].notna().any() else 0)
        else:
            human_avg.append(0)
            
        if len(llm_reviews) > 0:
            llm_avg.append(round(llm_reviews[col].mean(), 1) if llm_reviews[col].notna().any() else 0)
        else:
            llm_avg.append(0)
    
    comparison_data = {
        'criteria': criterion_names,
        'human_avg': human_avg,
        'llm_avg': llm_avg
    }
    
    return render_template('applicant_detail.html', 
                         applicant=applicant_name.upper(),
                         human_reviews=human_reviews.to_dict('records'),
                         llm_reviews=llm_reviews.to_dict('records'),
                         comparison=comparison_data)

@app.route('/api/chart_data')
def chart_data():
    """API endpoint for chart data."""
    df = get_combined_reviews()
    chart_type = request.args.get('type', 'scores')
    
    if chart_type == 'scores':
        # Score comparison by reviewer type
        human_scores = df[df['reviewer_type'] == 'Human']['total_score'].dropna().tolist()
        llm_scores = df[df['reviewer_type'] == 'LLM']['total_score'].dropna().tolist()
        
        return jsonify({
            'human_scores': human_scores,
            'llm_scores': llm_scores
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
    df = get_combined_reviews()
    
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
        'llm_means': llm_means
    })

@app.route('/api/model_comparison')
def model_comparison():
    """API endpoint for model-specific criteria comparison data."""
    df = get_combined_reviews()
    
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
    gpt4_data = df[(df['reviewer_type'] == 'LLM') & (df['model'].str.contains('gpt-4', case=False, na=False))]
    gpt5_data = df[(df['reviewer_type'] == 'LLM') & (df['model'].str.contains('gpt-5', case=False, na=False))]
    
    # Calculate means for each group
    human_means = [round(human_data[col].mean(), 1) if human_data[col].notna().any() else 0 for col in score_columns]
    gpt4_means = [round(gpt4_data[col].mean(), 1) if gpt4_data[col].notna().any() else 0 for col in score_columns]
    gpt5_means = [round(gpt5_data[col].mean(), 1) if gpt5_data[col].notna().any() else 0 for col in score_columns]
    
    return jsonify({
        'criteria': criterion_names,
        'human_means': human_means,
        'gpt4_means': gpt4_means,
        'gpt5_means': gpt5_means,
        'counts': {
            'human': len(human_data),
            'gpt4': len(gpt4_data),
            'gpt5': len(gpt5_data)
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5003)