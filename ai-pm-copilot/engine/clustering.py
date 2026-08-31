from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import numpy as np
import streamlit as st

MODEL_NAME = 'all-MiniLM-L6-v2'

@st.cache_resource
def get_model():
    return SentenceTransformer(MODEL_NAME)

@st.cache_data
def build_embeddings_and_clusters(df, n_clusters=9):
    texts = df['clean_text'].tolist()
    model = get_model()
    embeddings = model.encode(texts, show_progress_bar=False)
    # heuristic cluster count if user doesn't specify
    if n_clusters is None:
        n_clusters = max(2, int(len(df) / 12))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    labels = kmeans.fit_predict(embeddings)
    cluster_info = dict(labels=labels, centroids=kmeans.cluster_centers_)
    return embeddings, cluster_info
