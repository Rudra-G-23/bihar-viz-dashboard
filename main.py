import streamlit as st
from pathlib import Path

st.set_page_config(
    initial_sidebar_state=True,
    page_icon="🧑‍🔬",
    page_title="Bihar Dashboard",
    layout="wide"
)

st.title("Bihar In-Depth Analysis Dashboard")

SOLUTION_PDF_PATH = Path("reports/how-to-merge-solution.pdf")

if not SOLUTION_PDF_PATH.exists():
    st.error(f"PDF not found at {SOLUTION_PDF_PATH.resolve()}")
else:
    with open(SOLUTION_PDF_PATH, "rb") as f:
        pdf_bytes = f.read()

    st.download_button(
        label="📄 Open PDF",
        data=pdf_bytes,
        file_name="How_to_Merge_Whole_HCES_DATA.pdf",
        mime="application/pdf" 
    )

with st.expander("🖼️ Efficient way to merge", expanded=True):
    st.image("assets/pic/household-level.png", caption="Household Level Data and Person Level Data")
    st.image("assets/pic/item-level.png", caption="Item Level Data")
    st.image("assets/pic/single-merge-dataset.png", caption="Single Merge Dataset")
