import streamlit as st
import polars as pl

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

