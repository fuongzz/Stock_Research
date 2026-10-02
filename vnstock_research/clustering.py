from __future__ import annotations

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def cluster_windows(windows: pd.DataFrame, n_clusters: int = 3, method: str = "kmeans", pca_components: int = 0):
    feature_cols = [c for c in windows.columns if c.endswith("_mean") or c.endswith("_last")]
    clean = windows.dropna(subset=feature_cols).copy()
    scaler = StandardScaler()
    scaled = scaler.fit_transform(clean[feature_cols])
    projection = scaled
    pca = None
    if pca_components and pca_components < scaled.shape[1]:
        pca = PCA(n_components=pca_components, random_state=7)
        projection = pca.fit_transform(scaled)
    if method == "hdbscan":
        try:
            import hdbscan
            model = hdbscan.HDBSCAN(min_cluster_size=max(5, n_clusters))
            labels = model.fit_predict(projection)
        except ImportError:
            model = KMeans(n_clusters=n_clusters, random_state=7, n_init=20)
            labels = model.fit_predict(projection)
    else:
        model = KMeans(n_clusters=n_clusters, random_state=7, n_init=20)
        labels = model.fit_predict(projection)
    clean["cluster_id"] = labels
    return clean, {"feature_cols": feature_cols, "scaler": scaler, "pca": pca, "model": model}


def transform_windows(windows: pd.DataFrame, fitted: dict) -> pd.DataFrame:
    """Apply a train-fold transform to later windows without refitting."""
    feature_cols = fitted["feature_cols"]
    clean = windows.dropna(subset=feature_cols).copy()
    projection = fitted["scaler"].transform(clean[feature_cols])
    if fitted["pca"] is not None:
        projection = fitted["pca"].transform(projection)
    model = fitted["model"]
    if not hasattr(model, "predict"):
        raise ValueError("Configured clustering model cannot transform out-of-sample windows")
    clean["cluster_id"] = model.predict(projection)
    return clean
