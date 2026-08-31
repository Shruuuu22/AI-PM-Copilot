import numpy as np
import pandas as pd


def normalize_series(s):
    mi = s.min()
    ma = s.max()
    if ma == mi:
        return pd.Series([50]*len(s), index=s.index)
    return 100 * (s - mi) / (ma - mi)


def compute_priority_scores(themes, df, weights=None):
    # build DataFrame
    rows = []
    for t in themes:
        mentions = t['mentions']
        unique_customers = t['unique_customers']
        enterprise_customers = t['enterprise_customers']
        # frequency = mentions (normalized later)
        rows.append({
            'cluster': t['cluster'],
            'label': t.get('label',''),
            'summary': t.get('summary',''),
            'mentions': mentions,
            'unique_customers': unique_customers,
            'enterprise_customers': enterprise_customers,
            'representative_examples': t['representative_examples'],
            'keywords': t['keywords']
        })
    df_t = pd.DataFrame(rows)
    # compute components
    df_t['frequency'] = df_t['mentions']
    # customer value: proxy using enterprise_customers + avg account_value
    avg_values = []
    for t in themes:
        idx = t['samples_idx']
        avg = df.iloc[idx]['account_value'].mean()
        avg_values.append(avg if not np.isnan(avg) else 0)
    df_t['customer_value'] = avg_values
    # urgency: count urgency keywords
    urgency_keywords = ['blocked','cannot','broken','critical','urgent','unusable']
    urgency_scores = []
    for t in themes:
        idx = t['samples_idx']
        texts = df.iloc[idx]['clean_text'].str.lower()
        score = sum(texts.str.contains('|'.join(urgency_keywords)).fillna(False))
        urgency_scores.append(score)
    df_t['urgency'] = urgency_scores
    # sentiment severity: proportion negative
    sent_scores = []
    for t in themes:
        idx = t['samples_idx']
        s = df.iloc[idx]['sentiment']
        neg = (s < 0).sum()
        sent_scores.append(neg)
    df_t['sentiment_severity'] = sent_scores
    # breadth: number of distinct sources and segments
    breadth = []
    for t in themes:
        idx = t['samples_idx']
        s = df.iloc[idx]
        breadth.append(len(set(s['source'].tolist() + s['customer_segment'].tolist())))
    df_t['breadth'] = breadth

    # normalize components to 0-100
    for c in ['frequency','customer_value','urgency','sentiment_severity','breadth']:
        df_t[c+'_n'] = normalize_series(df_t[c])

    # weights
    if weights is None:
        weights = dict(frequency=0.30, customer_value=0.25, urgency=0.20, sentiment_severity=0.15, breadth=0.10)
    df_t['priority_score'] = (
        weights['frequency']*df_t['frequency_n'] +
        weights['customer_value']*df_t['customer_value_n'] +
        weights['urgency']*df_t['urgency_n'] +
        weights['sentiment_severity']*df_t['sentiment_severity_n'] +
        weights['breadth']*df_t['breadth_n']
    )
    df_t = df_t.sort_values('priority_score', ascending=False).reset_index(drop=True)
    df_t['rank'] = df_t.index + 1
    return df_t
