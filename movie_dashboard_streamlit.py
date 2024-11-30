import streamlit as st
import pandas as pd
import plotly.express as px

# Load the cleaned dataset
df = pd.read_csv(r"C:\Users\anupt\OneDrive\Desktop\MovieDashboard\cleaned_Dashboard_Dataset.csv")

# Sidebar Filters
st.sidebar.header("Filters")
selected_actor = st.sidebar.multiselect(
    "Select Actor",
    list(set(df['Star1'].dropna().unique()).union(
        set(df['Star2'].dropna().unique()),
        set(df['Star3'].dropna().unique()),
        set(df['Star4'].dropna().unique())
    ))
)
selected_director = st.sidebar.multiselect("Select Director", df['Director'].dropna().unique())
selected_genre = st.sidebar.multiselect("Select Genre", df['Genre'].dropna().unique())
selected_platform = st.sidebar.multiselect("Select Platform", df['Platform'].dropna().unique())
selected_gross_range = st.sidebar.slider(
    "Select Gross Range (in $)",
    min_value=float(df['Gross'].min()),
    max_value=float(df['Gross'].max()),
    value=(float(df['Gross'].min()), float(df['Gross'].max()))
)

# Filter DataFrame
filtered_df = df.copy()
if selected_actor:
    filtered_df = filtered_df[
        filtered_df['Star1'].isin(selected_actor) |
        filtered_df['Star2'].isin(selected_actor) |
        filtered_df['Star3'].isin(selected_actor) |
        filtered_df['Star4'].isin(selected_actor)
    ]
if selected_director:
    filtered_df = filtered_df[filtered_df['Director'].isin(selected_director)]
if selected_genre:
    filtered_df = filtered_df[filtered_df['Genre'].str.contains('|'.join(selected_genre))]
if selected_platform:
    filtered_df = filtered_df[filtered_df['Platform'].isin(selected_platform)]
if selected_gross_range:
    filtered_df = filtered_df[(filtered_df['Gross'] >= selected_gross_range[0]) & 
                              (filtered_df['Gross'] <= selected_gross_range[1])]

# Treemap Visualization
st.title("Enhanced Movie Dashboard")
if not filtered_df.empty:
    fig = px.treemap(
        filtered_df,
        path=['Platform', 'Genre', 'Series_Title'],
        values='Gross',
        color='IMDB_Rating',
        title="Movie Dashboard Treemap",
        color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig)
else:
    st.warning("No data matches the selected filters. Please adjust your filters.")
