import os
import polars as pl
import streamlit as st
import plotly.express as px

st.set_page_config(
    initial_sidebar_state=True,
    layout="wide"
)
st.title("Bihar In-Depth Analysis Dashboard")

st.image("assets/pic/household-level.png", caption="Household Level Data and Person Level Data")
st.image("assets/pic/item-level.png", caption="Item Level Data")
st.image("assets/pic/single-merge-dataset.png", caption="Single Merge Dataset")

st.markdown("""
            Full Reports:  [How to merge](assets/reports/how-to-merge-solution.pdf)
            """)