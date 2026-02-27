import pandas as pd
from sklearn.metrics import cohen_kappa_score
import numpy as np

# Load data
llm_df = pd.read_csv('data/combined_reviews.csv')
human_df = pd.read_csv('inputs/human_scores.csv')

# Clean up human data
human_df['Applicant'] = human_df['Applicant'].str.strip()
human_df['Overall Recommendation'] = human_df['Overall Recommendation'].str.strip()

# Map recommendations to broad categories
def get_broad_rec(rec):
    if pd.isna(rec): return None
    rec = str(rec).lower()
    if 'do not fund' in rec: return 'negative'
    return 'positive'

human_df['broad_rec'] = human_df['Overall Recommendation'].apply(get_broad_rec)
llm_df['broad_rec'] = llm_df['overall_recommendation'].apply(get_broad_rec)

# Calculate kappa for each experiment
for exp in ['baseline_v1', 'multi_examples_v1', 'strict_scoring_v1']:
    print(f"\nExperiment: {exp}")
    exp_df = llm_df[llm_df['prompt_experiment_name'] == exp]
    
    # For each LLM review, we need to compare it to the human reviews for the same applicant
    # Since there are multiple human reviews, we can calculate the average kappa or compare to the majority vote
    
    # Let's just calculate the agreement between each LLM review and a randomly selected human review, or all pairs
    pairs_exact = []
    pairs_broad = []
    
    for _, llm_row in exp_df.iterrows():
        app = llm_row['applicant_name']
        llm_rec = str(llm_row['overall_recommendation']).strip().lower()
        llm_broad = llm_row['broad_rec']
        
        # Get human reviews for this applicant
        h_reviews = human_df[human_df['Applicant'] == app]
        
        for _, h_row in h_reviews.iterrows():
            h_rec = str(h_row['Overall Recommendation']).strip().lower()
            h_broad = h_row['broad_rec']
            
            pairs_exact.append((llm_rec, h_rec))
            pairs_broad.append((llm_broad, h_broad))
            
    if pairs_exact:
        y1_exact, y2_exact = zip(*pairs_exact)
        kappa_exact = cohen_kappa_score(y1_exact, y2_exact)
        print(f"Exact Kappa: {kappa_exact:.3f}")
        
        y1_broad, y2_broad = zip(*pairs_broad)
        kappa_broad = cohen_kappa_score(y1_broad, y2_broad)
        print(f"Broad Kappa: {kappa_broad:.3f}")

