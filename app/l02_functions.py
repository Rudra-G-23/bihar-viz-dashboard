import time
import numpy as np
import pandas as pd
import polars as pl
import plotly.express as px
import streamlit as st
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Because this are continuous variables
pca_features = [
    "Age",
    "Years_of_Education",
    "Days_Away_From_Home_Last_30_Days",
    "Meals_Usually_Taken_Per_Day",
    "Meals_From_School",
    "Meals_From_Employer",
    "Meals_Other",
    "Meals_On_Payment",
    "Meals_At_Home",
    "Multiplier" # This is provide by the survey 
]

def correlation_df(df, pca_features):
    corr = df[pca_features].corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        aspect="auto",
        title="Feature Correlation Heatmap"
    )
    
    return corr, fig

@st.cache_resource
def apply_pca(df, n_components=10):
    X = (
        df
        .select(pca_features)
        .fill_null(0)
        .to_numpy()
    )
        
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    pca = PCA(n_components)
    X_pca = pca.fit_transform(X_scaled)
    X_pca_scaled = MinMaxScaler().fit_transform(X_pca)
    return pca, X_pca, X_pca_scaled

def explained_df_on_pca(pca):
    return pd.DataFrame({
        "PC": [f"PC{i+1}" for i in range(len(pca.explained_variance_ratio_))],
        "Explained_Variance": pca.explained_variance_ratio_,
        "Cumulative_Variance": np.cumsum(pca.explained_variance_ratio_)
    })

def cumulative_explained_variance_graph(df):
    return px.line(
        df,
        x="PC",
        y="Cumulative_Variance",
        markers=True,
        title="Cumulative Explained Variance (PCA)"
    )

def loadings_df(pca):
    return pd.DataFrame(
        pca.components_.T,
        columns=[f"PC{i+1}" for i in range(pca.components_.shape[0])],
        index=pca_features
    )

def pca_gender_2d_graphs(X_pca, df):
    
    pca_df = pd.DataFrame(
        X_pca[:, :2],
        columns=["PC1", "PC2"]
    )
    pca_df["Gender"] = df["Gender_label"]
    
    fig = px.scatter(
        pca_df,
        x="PC1",
        y="PC2",
        color="Gender",
        opacity=0.6,
        title="2D PCA Projection"
    )
    
    return fig

def education_pca_3d(X_pca, df):
    pca_df_3d = pd.DataFrame(
        X_pca[:, :3],
        columns=["PC1", "PC2", "PC3"]
    )

    pca_df_3d["Education"] = df["Education_Level_label"]
    
    fig = px.scatter_3d(
        pca_df_3d,
        x="PC1",
        y="PC2",
        z="PC3",
        color="Education",
        symbol="Education",
        hover_name="Education",
        opacity=0.6,
        title="3D PCA Projection",
        width=900,
        height=700,
        size_max=30
    )

    fig.update_traces(marker=dict(size=3))

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.25,
            xanchor="center",
            x=0.5
        ),
        margin=dict(b=120)
    )

    return pca_df_3d, fig

@st.cache_resource
def cluster_and_pca_on_overall_data(X_pca_scaled, pca_df_3d, n_clusters=6):
    
    kmeans = KMeans(n_clusters, random_state=42, n_init="auto")
    clusters = kmeans.fit_predict(X_pca_scaled[:, :3])

    pca_df_3d["Cluster"] = clusters
    
    
    fig = px.scatter_3d(
        pca_df_3d,
        x="PC1",
        y="PC2",
        z="PC3",
        color="Cluster",
        symbol="Cluster",
        title="PCA + KMeans Clusters",
        width=900,
        height=700,
    )

    fig.update_layout(
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.25,
            xanchor="center",
            x=0.5
        ),
        margin=dict(b=120)
    )

    return fig

def loading_animation_pca_time():
    with st.status("Model training, Cluster and PCA are working", expanded=True) as status:
        st.toast("Please wait ...", icon="⌛")
        st.write("Searching for data...")
        time.sleep(2)
        st.write("Feature Selection")
        time.sleep(2)
        st.write("Correlation and Graphs")
        time.sleep(2)
        st.write("Apply PCA")
        st.toast("Your `no. of components` applied.")
        time.sleep(4)
        st.write("Plot Elbow Graph")
        time.sleep(3)
        st.write("PCA on Gender graphs completed")
        time.sleep(2)
        st.write("PCA on Education graphs completed")
        time.sleep(2)
        st.write("KMeans Cluster performing....")
        st.toast("Your `no of cluster` applied.")
        time.sleep(5)
        st.write("Showing everything...")
        time.sleep(3)
        status.update(
            label="🎉 Graphs Ready!", state="complete", expanded=False
        )
