#!/usr/bin/env python3
"""
Script to combine human reviews from CSV with LLM reviews from SQLite database.
Creates a combined CSV output and a new database table with merged results.
"""

import pandas as pd
import sqlite3
import json
from datetime import datetime
from pathlib import Path

def load_human_reviews(csv_path):
    """Load and process human reviews from CSV file."""
    print(f"Loading human reviews from {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Rename columns for consistency
    column_mapping = {
        'Innovation and Impact (Why & What): Score between 0 to 30': 'Innovation and Impact',
        'Methodological Approach and Feasibility (How & When): Score between 0 to 30': 'Methodological Approach and Feasibility',
        'Strength of the Research Team (Who): Score between 0 to 10': 'Strength of Research Team',
        'Potential to Attract External Funding: Score between 0 to 10': 'Potential to Attract External Funding',
        'Clarity and Efficiency of Budget: Score between 0 to 10': 'Clarity and Efficiency of Budget',
        'Overall Presentation (Writing, Clarity, Flow): Score between 0 to 10': 'Overall Presentation (Writing, Clarity, Flow)',
        'Overall Recommendation': 'Overall Recommendation'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Calculate total score for human reviews
    score_columns = [
        'Innovation and Impact',
        'Methodological Approach and Feasibility', 
        'Strength of Research Team',
        'Potential to Attract External Funding',
        'Clarity and Efficiency of Budget',
        'Overall Presentation (Writing, Clarity, Flow)'
    ]
    
    df['Total Score'] = df[score_columns].sum(axis=1)
    
    print(f"Loaded {len(df)} human review records")
    return df

def load_llm_reviews(db_path):
    """Load and process LLM reviews from SQLite database."""
    print(f"Loading LLM reviews from {db_path}")
    
    conn = sqlite3.connect(db_path)
    
    # Get main review data including experiment information
    reviews_query = """
    SELECT
        id,
        applicant_name,
        vendor,
        model,
        model_version,
        iteration,
        timestamp,
        overall_recommendation,
        processing_time,
        prompt_experiment_name,
        prompt_version
    FROM grant_reviews
    ORDER BY applicant_name, iteration
    """
    
    reviews_df = pd.read_sql_query(reviews_query, conn)
    
    # Get criteria scores
    criteria_query = """
    SELECT 
        grant_review_id,
        applicant_name,
        criterion_name,
        score,
        rationale
    FROM grant_review_criteria
    ORDER BY grant_review_id, criterion_name
    """
    
    criteria_df = pd.read_sql_query(criteria_query, conn)
    conn.close()
    
    # Pivot criteria scores to create columns for each criterion
    criteria_pivot = criteria_df.pivot_table(
        index=['grant_review_id', 'applicant_name'],
        columns='criterion_name',
        values='score',
        aggfunc='first'
    ).reset_index()
    
    # Merge reviews with criteria scores
    llm_df = reviews_df.merge(
        criteria_pivot, 
        left_on=['id', 'applicant_name'], 
        right_on=['grant_review_id', 'applicant_name'],
        how='left'
    )
    
    # Calculate total score for LLM reviews
    score_columns = [
        'Innovation and Impact',
        'Methodological Approach and Feasibility',
        'Strength of Research Team', 
        'Potential to Attract External Funding',
        'Clarity and Efficiency of Budget',
        'Overall Presentation (Writing, Clarity, Flow)'
    ]
    
    available_score_columns = [col for col in score_columns if col in llm_df.columns]
    if available_score_columns:
        llm_df['Total Score'] = llm_df[available_score_columns].sum(axis=1)
    
    print(f"Loaded {len(llm_df)} LLM review records")
    return llm_df, criteria_df

def combine_reviews(human_df, llm_df):
    """Combine human and LLM reviews into a unified dataset."""
    print("Combining human and LLM reviews")
    
    # Prepare human reviews for combination
    human_combined = []
    for _, row in human_df.iterrows():
        record = {
            'applicant_name': row['Applicant'].upper(),
            'reviewer_id': row['Reviewer'],
            'reviewer_type': 'Human',
            'vendor': None,
            'model': None,
            'model_version': None,
            'iteration': None,
            'timestamp': None,
            'innovation_impact': row['Innovation and Impact'],
            'methodological_approach': row['Methodological Approach and Feasibility'],
            'research_team_strength': row['Strength of Research Team'],
            'external_funding_potential': row['Potential to Attract External Funding'],
            'budget_clarity': row['Clarity and Efficiency of Budget'],
            'presentation_quality': row['Overall Presentation (Writing, Clarity, Flow)'],
            'total_score': row['Total Score'],
            'overall_recommendation': row['Overall Recommendation'],
            'processing_time': None,
            'prompt_experiment_name': None,
            'prompt_version': None
        }
        human_combined.append(record)
    
    # Prepare LLM reviews for combination
    llm_combined = []
    for _, row in llm_df.iterrows():
        record = {
            'applicant_name': row['applicant_name'].upper(),
            'reviewer_id': f"{row['vendor']}_{row['model']}_{row['iteration']}",
            'reviewer_type': 'LLM',
            'vendor': row['vendor'],
            'model': row['model'],
            'model_version': row['model_version'],
            'iteration': row['iteration'],
            'timestamp': row['timestamp'],
            'innovation_impact': row.get('Innovation and Impact'),
            'methodological_approach': row.get('Methodological Approach and Feasibility'),
            'research_team_strength': row.get('Strength of Research Team'),
            'external_funding_potential': row.get('Potential to Attract External Funding'),
            'budget_clarity': row.get('Clarity and Efficiency of Budget'),
            'presentation_quality': row.get('Overall Presentation (Writing, Clarity, Flow)'),
            'total_score': row.get('Total Score'),
            'overall_recommendation': row['overall_recommendation'],
            'processing_time': row['processing_time'],
            'prompt_experiment_name': row.get('prompt_experiment_name'),
            'prompt_version': row.get('prompt_version')
        }
        llm_combined.append(record)
    
    # Combine all reviews
    all_reviews = human_combined + llm_combined
    combined_df = pd.DataFrame(all_reviews)
    
    print(f"Combined dataset contains {len(combined_df)} total reviews")
    print(f"- Human reviews: {len(human_combined)}")
    print(f"- LLM reviews: {len(llm_combined)}")
    
    return combined_df

def save_to_csv(df, output_path):
    """Save combined reviews to CSV file."""
    print(f"Saving combined reviews to {output_path}")
    df.to_csv(output_path, index=False)
    print(f"CSV file saved with {len(df)} records")

def save_to_database(df, db_path):
    """Save combined reviews to a new database table."""
    print(f"Saving combined reviews to database {db_path}")
    
    conn = sqlite3.connect(db_path)
    
    # Create the combined reviews table with experiment tracking
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS combined_reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        applicant_name TEXT NOT NULL,
        reviewer_id TEXT NOT NULL,
        reviewer_type TEXT NOT NULL,
        vendor TEXT,
        model TEXT,
        model_version TEXT,
        iteration INTEGER,
        timestamp TEXT,
        innovation_impact REAL,
        methodological_approach REAL,
        research_team_strength REAL,
        external_funding_potential REAL,
        budget_clarity REAL,
        presentation_quality REAL,
        total_score REAL,
        overall_recommendation TEXT,
        processing_time REAL,
        prompt_experiment_name TEXT,
        prompt_version TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    conn.execute(create_table_sql)
    
    # Insert the combined data
    df.to_sql('combined_reviews', conn, if_exists='replace', index=False)
    
    conn.commit()
    conn.close()
    
    print(f"Database table 'combined_reviews' created/updated with {len(df)} records")

def generate_summary_stats(df):
    """Generate summary statistics for the combined reviews."""
    print("\n=== SUMMARY STATISTICS ===")
    
    # Overall counts
    print(f"Total reviews: {len(df)}")
    print(f"Human reviews: {len(df[df['reviewer_type'] == 'Human'])}")
    print(f"LLM reviews: {len(df[df['reviewer_type'] == 'LLM'])}")
    print(f"Unique applicants: {df['applicant_name'].nunique()}")
    
    # Reviews per applicant
    print("\nReviews per applicant:")
    applicant_counts = df['applicant_name'].value_counts()
    for applicant, count in applicant_counts.items():
        human_count = len(df[(df['applicant_name'] == applicant) & (df['reviewer_type'] == 'Human')])
        llm_count = len(df[(df['applicant_name'] == applicant) & (df['reviewer_type'] == 'LLM')])
        print(f"  {applicant}: {count} total ({human_count} human, {llm_count} LLM)")
    
    # Score statistics by reviewer type
    print("\nScore statistics by reviewer type:")
    for reviewer_type in ['Human', 'LLM']:
        subset = df[df['reviewer_type'] == reviewer_type]
        if len(subset) > 0 and 'total_score' in subset.columns:
            print(f"  {reviewer_type} reviews:")
            print(f"    Mean total score: {subset['total_score'].mean():.1f}")
            print(f"    Score range: {subset['total_score'].min():.0f} - {subset['total_score'].max():.0f}")
    
    # Recommendation distribution
    print("\nOverall recommendation distribution:")
    rec_counts = df['overall_recommendation'].value_counts()
    for rec, count in rec_counts.items():
        print(f"  {rec}: {count}")

def main():
    """Main function to combine human and LLM reviews."""
    # File paths
    csv_path = Path("inputs/human_scores.csv")
    db_path = Path("data/results.db")
    output_csv = Path("data/combined_reviews.csv")
    
    # Check if input files exist
    if not csv_path.exists():
        print(f"Error: Human scores CSV file not found at {csv_path}")
        return
    
    if not db_path.exists():
        print(f"Error: Results database not found at {db_path}")
        return
    
    # Load data
    human_df = load_human_reviews(csv_path)
    llm_df, criteria_df = load_llm_reviews(db_path)
    
    # Combine reviews
    combined_df = combine_reviews(human_df, llm_df)
    
    # Save outputs
    save_to_csv(combined_df, output_csv)
    save_to_database(combined_df, db_path)
    
    # Generate summary
    generate_summary_stats(combined_df)
    
    print(f"\n=== COMPLETED SUCCESSFULLY ===")
    print(f"Combined reviews saved to:")
    print(f"- CSV: {output_csv}")
    print(f"- Database table: 'combined_reviews' in {db_path}")

if __name__ == "__main__":
    main()