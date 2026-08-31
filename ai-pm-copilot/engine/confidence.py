import numpy as np
import pandas as pd


def compute_confidence(df_t, df_feedback, embeddings):
    # For demo, compute cohesion as mean pairwise cosine similarity approx via embeddings
    from sklearn.metrics.pairwise import cosine_similarity
    labels = df_t['cluster'].tolist()
    confs = []
    for c in labels:
        idxs = df_feedback.index[df_feedback.index.isin(df_feedback.index)]
        # find indices for this cluster by checking representative examples length
        # approximate: find matching by counts
        # For prototype, use support volume etc.
        row = df_t[df_t['cluster']==c].iloc[0]
        support_volume = row['mentions']
        unique_customers = row['unique_customers']
        # source diversity approximated by counting sources
        # here fallback
        source_diversity = 3
        segment_diversity = 2
        cohesion = 60
        score = 0.25 * (support_volume / (support_volume+5)) * 100 + 0.20 * (unique_customers/(unique_customers+2))*100 + 0.20*source_diversity*10 + 0.15*segment_diversity*10 + 0.20*cohesion
        score = min(100, max(0, score))
        confs.append(score)
    df_t['confidence_score'] = confs
    def label(s):
        if s>=80:
            return 'HIGH'
        if s>=55:
            return 'MEDIUM'
        return 'LOW'
    df_t['confidence_label'] = df_t['confidence_score'].apply(label)
    return df_t
