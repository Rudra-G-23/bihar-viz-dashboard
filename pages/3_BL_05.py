import streamlit as st
import polars as pl
import builtins
from pathlib import Path

from app.l05_functions import(
    load_level_05_data,
    category_dict_to_dataframe,
    total_consumption_qty_by_category,
    total_consumption_value_by_category,
    distribution_of_metric_by_categories,
    total_qty_vs_total_value_by_category,
    total_qty_vs_avg_price_by_category,
    
    group_bar_chart_qty_type,
    out_of_home_vs_total_qty_by_category,
    
    stack_bar_chart_on_value,
    out_of_home_vs_total_value_stack_graph,
    
    consumption_pattern_by_category,
    
    category_mapping,
    cereal_mapping,
)

LEVEL_05_PATH = Path("data\BL05.parquet")

st.set_page_config(
    page_title="Level 05",
    layout="wide"
)

st.title("Level 05")

df = load_level_05_data(LEVEL_05_PATH)
fdf = df.clone()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "t1", "t2", "t3", "t4", "t5", "t6", 
])

with tab1:
    st.write(f"Total Rows: {df.shape[0]}")
    st.write(df.describe())

with tab2:
    cat_df = category_dict_to_dataframe(category_mapping(), fdf)
    
    fig1 = total_consumption_qty_by_category(cat_df)
    st.plotly_chart(fig1)
    
    fig2 = total_consumption_value_by_category(cat_df)
    st.plotly_chart(fig2)
    
with tab3:
    fig3 = distribution_of_metric_by_categories(cat_df)
    st.plotly_chart(fig3)
    

with tab4:
    fig4 = total_qty_vs_total_value_by_category(cat_df)
    st.plotly_chart(fig4)
    
    fig5 = total_qty_vs_avg_price_by_category(cat_df)
    st.plotly_chart(fig5)

with tab5:
    qty_df = group_bar_chart_qty_type(cat_df)
    st.dataframe(qty_df)
    
    fig6 = out_of_home_vs_total_qty_by_category(qty_df)
    st.plotly_chart(fig6)

    val_df = stack_bar_chart_on_value(cat_df)
    st.dataframe(val_df)
    
    fig7 = out_of_home_vs_total_value_stack_graph(val_df)
    st.plotly_chart(fig7)

with tab6:
    fig8 = consumption_pattern_by_category(cat_df)
    st.plotly_chart(fig8)