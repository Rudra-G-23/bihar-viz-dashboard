import streamlit as st
import polars as pl
import builtins
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

@st.cache_data
def load_level_05_data(path):
    # Load the data
    df = pl.read_parquet(path)
    
    # Correct datatype
    df = df.with_columns(
            (pl.col("OutOfHome_Consumption_Quantity").cast(pl.Float64, strict=False)),
            (pl.col("OutOfHome_Consumption_Value").cast(pl.Float64, strict=False))
        )
    
    # Select useful columns only
    df = df.select([
        'FSU_Serial_No','Sector','NSS_Region','District','Stratum',
        'Sub_stratum','Panel','Sub_sample','FOD_Sub_Region',
        'Sample_SU_No','Sample_Household_No','Questionnaire_No',
        'Item_Code','OutOfHome_Consumption_Quantity','OutOfHome_Consumption_Value',
        'Total_Consumption_Quantity','Total_Consumption_Value'
    ])
    
    return df

@st.cache_data
def category_dict_to_dataframe(category_mapping:dict, fdf):
    """
    1. Create the dataframe form the dict
    2. Join with the original / Filter dataset
    3. Create totally new dataset for further analysis
        a. Only valid data 
        b. Then category, Out of Home and Total columns selected
        c. Aggregate the columns
        d. Provide a clean and valid dataset for further analysis.
    """
     
    # Create the dataframe form dictionary
    map_df = pl.DataFrame({
        "Item_Code": builtins.list(category_mapping.keys()),
        "category_mapped": builtins.list(category_mapping.values()),
    })

    # Join the category dataframe & whole dataset
    fdf = fdf.join(map_df, on="Item_Code", how="left")
    
    # Create a totally new dataframe with desire columns
    cat_df = fdf.filter(
        pl.col("category_mapped").is_not_null()
        ) \
        [
        'OutOfHome_Consumption_Quantity',
        'OutOfHome_Consumption_Value',
        'Total_Consumption_Quantity',
        'Total_Consumption_Value',
        "category_mapped"
        ] \
        .group_by("category_mapped").agg(
            pl.col("OutOfHome_Consumption_Value").sum().alias("out_home_value"),
            pl.col("OutOfHome_Consumption_Quantity").sum().alias("out_home_qty"),
            pl.col("Total_Consumption_Quantity").sum().alias("total_qty"),
            pl.col("Total_Consumption_Value").sum().alias("total_value")
        ).with_columns(
            out_of_home_avg_pice = pl.when(pl.col("out_home_qty") > 0) 
                            .then(pl.col("out_home_value") / pl.col("out_home_qty"))
                            .otherwise(0),
            total_avg_pice = pl.when(pl.col("total_qty") > 0) 
                            .then(pl.col("total_value") / pl.col("total_qty"))
                            .otherwise(0),
        ) 
        
    return cat_df

def total_consumption_qty_by_category(cat_df):
    return px.bar(
        cat_df.sort('total_qty'),
        x="total_qty",
        y="category_mapped",
        orientation="h",
        title="Total Consumption Quantity by Category"
    )
    
def total_consumption_value_by_category(cat_df):
    return px.bar(
        cat_df.sort('total_value'),
        x="total_value",
        y="category_mapped",
        orientation="h",
        title="Total Consumption Value by Category"
    )  

def out_of_home_consumption_qty_by_category(cat_df):
    return px.bar(
        cat_df.sort('out_home_qty'),
        x="out_home_qty",
        y="category_mapped",
        orientation="h",
        title="Out of Home Consumption Quantity by Category"
    )
    
def out_of_home_consumption_value_by_category(cat_df):
    return px.bar(
        cat_df.sort('out_home_value'),
        x="out_home_value",
        y="category_mapped",
        orientation="h",
        title="Out of Home Consumption Value by Category"
    )  
          
def distribution_of_metric_by_categories(
    df ,
    cols = [
        "out_home_value","out_home_qty","out_of_home_avg_pice",
        "total_qty","total_value","total_avg_pice"
        ],
    title="Distribution of Metrics by Category"
):
    fig = make_subplots(
        rows=2,
        cols=3,
        subplot_titles=cols
    )

    positions = [
        (1, 1), (1, 2), (1, 3),
        (2, 1), (2, 2), (2, 3)
    ]

    for col, (r, c) in zip(cols, positions):
        fig.add_trace(
            go.Box(
                y=df[col],
                name=col,
                boxmean=True,
                hovertext=df["category_mapped"],

            ),
            row=r,
            col=c
        )

    fig.update_layout(
        title=title,
        showlegend=False,
        height=700
    )

    return fig    

def total_qty_vs_total_value_by_category(df):
    return px.scatter(
        df,
        x="total_qty",
        y="total_value",
        color="category_mapped",
        symbol="category_mapped",
        title="Total Quantity vs Total Value by Category",
        labels={
            "total_qty": "Total Quantity",
            "total_value": "Total Value"
        },
        hover_name="category_mapped",
        size="total_value",
        size_max=30
    )

def total_qty_vs_avg_price_by_category(df):
    return px.scatter(
        df,
        x="total_qty",
        y="total_avg_pice",
        color="category_mapped",
        symbol="category_mapped",
        title="Total Quantity vs Average Price by Category",
        hover_name="category_mapped",
        size="total_avg_pice",
        size_max=30
    )

def out_of_home_qty_vs_out_of_home_value_by_category(df):
    return px.scatter(
        df,
        x="out_home_qty",
        y="out_home_value",
        color="category_mapped",
        symbol="category_mapped",
        title="Out of Home Quantity vs Out of Home Value by Category",
        hover_name="category_mapped",
        size="out_home_value",
        size_max=30
    )

def out_of_home_qty_vs_out_of_home_avg_price_by_category(df):
    return px.scatter(
        df,
        x="out_home_qty",
        y="out_of_home_avg_pice",
        color="category_mapped",
        symbol="category_mapped",
        title="Total Quantity vs Average Price by Category",
        hover_name="category_mapped",
        size="out_of_home_avg_pice",
        size_max=30
    )

def group_bar_chart_qty_type(df):
    return df.select([
        "category_mapped",
        "out_home_qty",
        "total_qty"
    ]).unpivot(
        index="category_mapped",
        on=["out_home_qty", "total_qty"],
        variable_name="quantity_type",
        value_name="quantity"
    )

def out_of_home_vs_total_qty_by_category(qty_df):
    return px.bar(
        qty_df,
        x="category_mapped",
        y="quantity",
        color="quantity_type",
        barmode="group",
        title="Out-of-Home vs Total Quantity by Category"
    )

def stack_bar_chart_on_value(df):
    return df.select([
        "category_mapped",
        "out_home_value",
        "total_value"
    ]).unpivot(
        index="category_mapped",
        on=["out_home_value", "total_value"],
        variable_name="value_type",
        value_name="value"
    )

def out_of_home_vs_total_value_stack_graph(val_df):
    return px.bar(
        val_df,
        x="category_mapped",
        y="value",
        color="value_type",
        barmode="stack",
        title="Out-of-Home vs Total Consumption Value"
    )

def total_consumption_pattern_by_category(df):
    return px.scatter(
        df,
        x="total_qty",
        y="total_value",
        size="total_avg_pice",
        color="category_mapped",
        symbol="category_mapped",
        title="Total Consumption Pattern by Category",
        size_max=20
    )
    
def out_of_home_consumption_pattern_by_category(df):
    return px.scatter(
        df,
        x="out_home_qty",
        y="out_home_value",
        size="out_of_home_avg_pice",
        color="category_mapped",
        symbol="category_mapped",
        title="Average Out of Home Consumption Pattern by Category",
        size_max=20
    )