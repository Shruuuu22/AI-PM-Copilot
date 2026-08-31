from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


def top_keywords(texts, k=5):
    tf = TfidfVectorizer(stop_words='english', ngram_range=(1,2), max_features=2000)
    X = tf.fit_transform(texts)
    sums = X.sum(axis=0)
    terms = tf.get_feature_names_out()
    data = [(terms[i], sums[0,i]) for i in range(len(terms))]
    data = sorted(data, key=lambda x: x[1], reverse=True)
    return [t for t,_ in data[:k]]


def build_theme_evidence(df, embeddings, cluster_info):
    labels = cluster_info['labels']
    n = len(set(labels))
    themes = []
    for c in range(n):
        idx = [i for i,l in enumerate(labels) if l==c]
        samples = df.iloc[idx]
        texts = samples['feedback_text'].tolist()
        clean_texts = samples['clean_text'].tolist()
        keywords = top_keywords(clean_texts, k=6)
        # representative examples: top by shortness
        examples = sorted(texts, key=lambda x: len(x))[:8]
        theme = dict(
            cluster=c,
            mentions=len(texts),
            unique_customers=samples['customer_id'].nunique(),
            enterprise_customers=int((samples['customer_segment']=='Enterprise').sum()),
            samples_idx=idx,
            representative_examples=examples,
            keywords=keywords,
            # placeholder label & summary used by LLM later
            label=f"Theme {c}",
            summary=' '.join(keywords[:6])
        )
        themes.append(theme)
    return themes
