import streamlit as st
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

LEVEL_05_PATH = Path("data\BL05.parquet")

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

category_fn = CATEGORY_FN_MAP[selected_category]   
category_dict = category_fn()
cat_df = category_dict_to_dataframe(category_dict, fdf)

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "t1", "t2", "t3", "t4", "t5", "t6", 
])

with tab1:
    st.write(f"Total Rows: {df.shape[0]}")
    st.write(df.describe())

with tab2:
        
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