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
        }
    )

def total_qty_vs_avg_price_by_category(df):
    return px.scatter(
        df,
        x="total_qty",
        y="total_avg_pice",
        color="category_mapped",
        title="Total Quantity vs Average Price by Category"
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

def consumption_pattern_by_category(df):
    return px.scatter(
        df,
        x="total_qty",
        y="total_value",
        size="total_avg_pice",
        color="category_mapped",
        title="Consumption Pattern by Category",
        size_max=40
    )

   
def category_mapping():
    return {
        129: "cereals",
        139: "cereal substitute",
        159: "pulses & products",
        179: "salt & sugar",
        169: "milk & milk products",
        219: "vegetables",
        239: "fruits (fresh)",
        249: "fruits (dry)",
        199: "egg, fish & meat",
        189: "edible oil",
        269: "spices",
        279: "beverages",
        289: "served processed food",
        299: "packaged processed food"
    }

def cereal_mapping():
    return {
        61: "rice-free",
        62: "wheat/atta-free",
        70: "coarse grains-free",
        101: "rice – PDS",
        102: "rice – other sources",
        103: "chira",
        105: "muri",
        106: "other rice products (khoi/lawa, etc.)",
        107: "wheat/atta – PDS",
        108: "wheat/atta – other sources",
        110: "maida",
        111: "suji/rawa",
        112: "vermicelli (sewai)",
        114: "other wheat products",
        1: "coarse grains – PDS",
        2: "coarse grains – other sources",
        122: "other cereals & products",
        129: "cereals: sub-total"
    }

def pulses_mapping ():
    return {
        140: "arhar/tur",
        141: "gram: split",
        142: "gram: whole",
        143: "moong",
        144: "masur",
        145: "urd",
        146: "peas/chickpeas",
        148: "other pulses (khesari, etc.)",
        150: "besan/gram products",
        152: "other pulse products (soya chunks, etc.)",
        158: "pulses – PDS",
        71: "pulses – free",
        72: "gram – free",
        # 159: "pulses & pulse products: sub-total"
    }

def salt_sugar_mapping():
    return {
        73: "salt – free",
        74: "sugar – free",
        178: "salt – PDS",
        170: "salt – other sources",
        171: "sugar – PDS",
        172: "sugar – other sources",
        173: "jaggery (gur)",
        174: "candy/misri",
        175: "honey",
        #179: "salt & sugar: sub-total"
    }

def milk_mapping():
    return {
        160: "milk: liquid",
        162: "milk: condensed/powder",
        163: "curd/yogurt",
        164: "ghee",
        165: "butter",
        166: "ice-cream",
        3: "paneer",
        4: "prepared sweets",
        5: "cheese",
        92: "other milk products (lassi, buttermilk, etc.)",
        # 169: "milk & milk products: sub-total"
    }

def vegetables_mapping():
    return {
        200: "potato",
        201: "onion",
        202: "tomato",
        203: "brinjal",
        204: "radish",
        205: "carrot",
        206: "leafy vegetables",
        207: "green chillies",
        208: "lady’s finger",
        210: "parwal/patal/kundru",
        211: "cauliflower",
        212: "cabbage",
        213: "gourd/pumpkin",
        214: "peas",
        215: "beans/barbati",
        216: "lemon",
        217: "other vegetables",
        # 219: "vegetables: sub-total"
    }

def fruits_fresh_mapping():
    return {
    220: "banana",
    224: "coconut",
    225: "green coconut",
    226: "guava",
    228: "orange/sweet lime (mausami)",
    230: "papaya",
    231: "mango",
    232: "kharbooza",
    236: "apple",
    237: "grapes",
    222: "watermelon",
    93: "other fresh fruits (litchi, pineapple, etc.)",
    # 239: "fruits (fresh): sub-total"
    }

def fruits_dry_mapping():
    return {
        240: "coconut: copra",
        241: "groundnut",
        242: "dates",
        243: "cashew nut",
        245: "other nuts (almond, pistachio, walnut, etc.)",
        246: "raisin/kishmish",
        94: "other dry fruits (apricot, fig, etc.)",
        # 249: "fruits (dry): sub-total"
    }

def nonveg_mapping():
    return {
        190: "eggs",
        191: "fish/prawn",
        192: "goat meat/mutton",
        193: "beef/buffalo meat",
        194: "pork",
        195: "chicken",
        196: "other meat (crab, oyster, etc.)",
        # 199: "egg, fish & meat: sub-total"
    }

def edible_oil_mapping():
    return {
        181: "mustard oil",
        182: "groundnut oil",
        183: "coconut oil",
        184: "refined oil",
        188: "edible oil – PDS",
        95: "other oils (vanaspati, margarine, etc.)",
        75: "edible oil – free",
        # 189: "edible oil: sub-total"
    }

def spices_mapping():
    return {
        250: "ginger",
        251: "garlic",
        252: "cumin",
        253: "coriander",
        254: "turmeric",
        255: "black pepper",
        256: "dry chillies",
        257: "tamarind",
        258: "curry powder",
        260: "oilseeds",
        261: "other spices",
        263: "poppy seeds",
        # 269: "spices: sub-total"
    }   

def beverages_mapping():
    return {
        11: "soda drinks",
        270: "tea: cups",
        271: "tea: leaf",
        272: "coffee: cups",
        273: "coffee: powder",
        274: "mineral water",
        275: "other cold beverages",
        276: "fruit juice/shake",
        278: "other beverages (cocoa, health drinks)",
        # 279: "beverages: sub-total"
    }

