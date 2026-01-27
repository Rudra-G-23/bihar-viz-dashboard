import time
import polars as pl
import streamlit as st
from pathlib import Path
import plotly.express as px

path = Path("data") / "BL02.parquet"

st.set_page_config(
    page_title="Level 02",
)

st.title("Level 02")

@st.cache_data
def load_data():
    df = pl.read_parquet(path)
    return df

df = load_data()

fdf = df.clone()


tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(
    ["Gender", "Year of Edu.", "Internet Used",
     "Age", "Education Level", "Marital Status",
     "Relation to Head", "Data Frame"]   
)

with tab1:
    with st.spinner("Gender Graph Loading..."):
        fig = px.pie(
            fdf['Gender_label'].value_counts(),
            values='count',
            names='Gender_label',
            title="Gender Pie Chart"
        )

        fig.update_layout(showlegend=True)

        st.plotly_chart(fig)

with tab2:
    with st.spinner("Year of Education Loading..."): 
        fig = px.bar(
            fdf['Years_of_Education'].value_counts(),
            x='Years_of_Education',
            y='count',
            range_y=[0, 8_000],
            title="Year of Education Distribution"
        )
        
        st.plotly_chart(fig)

        fig = px.box(
            fdf,
            x='Used_Internet_Last_30_Days',
            y='Years_of_Education',
            color='Gender',
            title="Last used Internet w/ Gender w/ Age"
        )

        fig.update_layout(showlegend=True)

        fig.update_xaxes(
            tickvals=[1, 2],
            ticktext=['Yes', 'No']
        ) 
        st.plotly_chart(fig)

with tab3:
    
    fig = px.box(
    fdf[['Used_Internet_Last_30_Days', 'Years_of_Education']],
    x='Used_Internet_Last_30_Days',
    y='Years_of_Education',
    title="Relationship b/w Internet Used w/ Year of Edu  "
    )

    fig.update_xaxes(
        tickvals=[1, 2],
        ticktext=['Yes', 'No']
    )

    st.plotly_chart(fig)
    
    fig = px.pie(
    fdf['Used_Internet_Last_30_Days'].value_counts(),
    values='count',
    names='Used_Internet_Last_30_Days', 
    title='Internet Usage in Last 30 Days'
    )
    
    fig.update_layout(showlegend=True)
    st.plotly_chart(fig)

    fig = px.box(
        fdf[['Used_Internet_Last_30_Days', 'Age', 'Gender']],
        x='Used_Internet_Last_30_Days',
        y='Age',
        color='Gender',
        title="Last used Internet w/ Gender w/ Age"
    )

    fig.update_layout(showlegend=True)

    fig.update_xaxes(
        tickvals=[1, 2],
        ticktext=['Yes', 'No']
    )
    st.plotly_chart(fig)

with tab4:
    fig = px.box(
        fdf['Age'],
        title="Age Boxplot"
        ) 

    st.plotly_chart(fig)

    fig = px.histogram(df, x='Age', title="Age Distribution")
    st.plotly_chart(fig)


    fig = px.bar(
        fdf['Age'].value_counts(),
        x='Age',
        y='count',
        text_auto=True,
        title="Age Count")
    st.plotly_chart(fig)

with tab5:

    fig = px.bar(
        fdf['Education_Level'].value_counts(),
        x='Education_Level',
        y='count',
        text_auto=True,
        title="Education Level Count",
        width=800,
    )
    
    st.plotly_chart(fig)

with tab6:
    fig = px.pie(
    fdf['Marital_Status_label'].value_counts(),
    values='count',
    names='Marital_Status_label',
    title="Marital Status Pie Chart"
    )

    fig.update_layout(showlegend=True)
    st.plotly_chart(fig)

    fig = px.density_heatmap(
        fdf[['Marital_Status', 'Education_Level']], 
        x='Marital_Status', 
        y='Education_Level', 
        text_auto=True, 
        title='Marital Status by Education Level'
    )

    fig.update_xaxes(
        tickvals=[1, 2, 3, 4],
        ticktext=['Never Married', 'Currently Married', 'Widowed', 'Divorced/Separated']
    )
    st.plotly_chart(fig)

with tab7:
    fig = px.box(
    fdf[['Relation_to_Head', 'Age', 'Gender']],
    x='Relation_to_Head',
    y='Age',
    color='Gender',
    title="Relation to Head w/ Gender w/ Age",
    width=800,
    )

    st.plotly_chart(fig)
    
    fig = px.scatter(
        fdf[['Age', 'Gender', 'Days_Away_From_Home_Last_30_Days']],
        x='Age', 
        y='Days_Away_From_Home_Last_30_Days',
        symbol='Gender',
        title="Relationship between Age and Days Away by Gender"
    )

    st.plotly_chart(fig)
    
with tab8:
    st.dataframe(fdf)    


