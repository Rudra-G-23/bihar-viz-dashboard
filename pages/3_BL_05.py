import streamlit as st
import polars as pl
import builtins
from pathlib import Path

from app.l05_functions import(
    load_level_05_data,
    category_mapping,
)

LEVEL_05_PATH = Path("data\BL05.parquet")

st.set_page_config(
    page_title="Level 02",
    layout="wide"
)

st.title("Level 02")

df = load_level_05_data(LEVEL_05_PATH)
st.dataframe(df.head(2))

fdf = df.clone()

