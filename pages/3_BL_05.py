import streamlit as st
from pathlib import Path

from app.l05_functions import(
    load_level_05_data,
    category_dict_to_dataframe,
    total_consumption_qty_by_category,
    total_consumption_value_by_category,
    out_of_home_consumption_qty_by_category,
    out_of_home_consumption_value_by_category,
    
    distribution_of_metric_by_categories,
    total_qty_vs_total_value_by_category,
    total_qty_vs_avg_price_by_category,
    out_of_home_qty_vs_out_of_home_value_by_category,
    out_of_home_qty_vs_out_of_home_avg_price_by_category,
        
    
    group_bar_chart_qty_type,
    out_of_home_vs_total_qty_by_category,
    
    stack_bar_chart_on_value,
    out_of_home_vs_total_value_stack_graph,
    
    total_consumption_pattern_by_category,
    out_of_home_consumption_pattern_by_category
)

from app.l05_categories import (  
    category_mapping,
    cereal_mapping,
    pulses_mapping,
    salt_sugar_mapping,
    milk_mapping,
    vegetables_mapping,
    fruits_fresh_mapping,
    fruits_dry_mapping,
    nonveg_mapping,
    edible_oil_mapping,
    spices_mapping,
    beverages_mapping,
)

LEVEL_05_PATH = Path("data") / "BL05.parquet"

st.set_page_config(
    page_title="Level 05",
    layout="wide"
)

st.title("Level 05")

df = load_level_05_data(LEVEL_05_PATH)
fdf = df.clone()

CATEGORY_FN_MAP = {
    "All Category": category_mapping,
    "Cereal Family": cereal_mapping,
    "Pulses Family": pulses_mapping,
    "Salt & Sugar Family": salt_sugar_mapping,
    "Milk Family": milk_mapping,
    "Vegetables": vegetables_mapping,
    "Fresh Fruits": fruits_fresh_mapping,
    "Dry Fruits": fruits_dry_mapping,
    "Non-Veg": nonveg_mapping,
    "Edible Oil": edible_oil_mapping,
    "Spices Mapping": spices_mapping,
    "Beverages": beverages_mapping,
}

with st.expander("📦 Choose Category want to view", expanded=True):
    
    selected_category = st.pills(
        label="",
        options=list(CATEGORY_FN_MAP.keys()),
        selection_mode="single",
        default="All Category",
    )
    
st.write("---")

category_fn = CATEGORY_FN_MAP[selected_category]   
category_dict = category_fn()
cat_df = category_dict_to_dataframe(category_dict, fdf)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Statistical", "Consumption", "Distribution",
    "Qty, Value by Category", "Category", "Avg Qty, Value by Category", 
])

with tab1:
    st.write(f"Total Rows: {df.shape[0]}")
    
    with st.expander(label="Statistical Summary"):
        st.subheader("Statistical")
        st.write(df.describe())

    with st.expander(label="Category Dataframe"):   
        st.subheader("Category Dataframe")
        st.dataframe(cat_df) 
    
    with st.expander(label="Original Dataframe"):
        st.subheader("Original Dataframe")
        st.dataframe(df.head(20))

with tab2:
    st.subheader("Total Consumption")
        
    col1_tb2, col2_tb2 = st.columns(2)
    
    with col1_tb2:
        fig1 = total_consumption_qty_by_category(cat_df)
        st.plotly_chart(fig1)
    
    with col2_tb2:
        fig2 = total_consumption_value_by_category(cat_df)
        st.plotly_chart(fig2)
    
    st.write("---")
    st.subheader("Out of Home Consumption")
        
    col1_tb2, col2_tb2 = st.columns(2)
    
    with col1_tb2:
        fig11 = out_of_home_consumption_qty_by_category(cat_df)
        st.plotly_chart(fig11)
    
    with col2_tb2:
        fig22 = out_of_home_consumption_value_by_category(cat_df)
        st.plotly_chart(fig22)
    
with tab3:
    st.subheader("Distribution of Metrics by Category")
    fig3 = distribution_of_metric_by_categories(cat_df)
    st.plotly_chart(fig3)

with tab4:
    st.subheader("Total Qty, Value by Category")
    tb4_col1, tb4_col2 = st.columns(2)
    with tb4_col1:
        fig4 = total_qty_vs_total_value_by_category(cat_df)
        st.plotly_chart(fig4)
    
    with tb4_col2:
        fig5 = total_qty_vs_avg_price_by_category(cat_df)
        st.plotly_chart(fig5)
        
    st.write("---")
    st.subheader("Out of Home Qty, Value by Category")
    tb4_col1, tb4_col2 = st.columns(2)
    with tb4_col1:
        fig41 = out_of_home_qty_vs_out_of_home_value_by_category(cat_df)
        st.plotly_chart(fig41)
    
    with tb4_col2:
        fig51 = out_of_home_qty_vs_out_of_home_avg_price_by_category(cat_df)
        st.plotly_chart(fig51)
    
with tab5:
    st.subheader("Out of Home vs Total Qty by Category")
    tab5_col1, tab5_col2 = st.columns([1, 2])
    with tab5_col1:
        qty_df = group_bar_chart_qty_type(cat_df)
        st.dataframe(qty_df)
    with tab5_col2:
        fig6 = out_of_home_vs_total_qty_by_category(qty_df)
        st.plotly_chart(fig6)

    st.write("---")
    st.subheader("Out of Home vs Total Value by Category")
    tab5_col1, tab5_col2 = st.columns([1, 2])
    with tab5_col1:
        val_df = stack_bar_chart_on_value(cat_df)
        st.dataframe(val_df)
  
    with tab5_col2:
        fig7 = out_of_home_vs_total_value_stack_graph(val_df)
        st.plotly_chart(fig7)

with tab6:
    tb6_c1, tb6_c2 = st.columns(2)
    
    with tb6_c1:
        fig8 = total_consumption_pattern_by_category(cat_df)
        st.plotly_chart(fig8)
    
    with tb6_c2:
        fig9 = out_of_home_consumption_pattern_by_category(cat_df)
        st.plotly_chart(fig9)