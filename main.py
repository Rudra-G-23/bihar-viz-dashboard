import os
import polars as pl
import streamlit as st
import plotly.express as px
from pathlib import Path

SOLUTION_PDF_PATH = Path("assets/reports/how-to-merge-solution.pdf")

st.set_page_config(
    initial_sidebar_state=True,
    page_icon="🧑‍🔬",
    page_title="Bihar Dashboard",
    layout="wide"
)

st.title("Bihar In-Depth Analysis Dashboard")

st.image("assets/pic/household-level.png", caption="Household Level Data and Person Level Data")
st.image("assets/pic/item-level.png", caption="Item Level Data")
st.image("assets/pic/single-merge-dataset.png", caption="Single Merge Dataset")

with open(SOLUTION_PDF_PATH, "rb") as f:
    pdf_bytes = f.read()

st.download_button(
    label="📄 Open PDF",
    data=pdf_bytes,
    file_name="How to Merge Whole HCES DATA.pdf",
    mime="application/pdf"
)
