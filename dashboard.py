import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from processing import os, compute_turnover, extract_info_table_xml, parse_info_table_xml, load_filings

folder_path = "./sec-edgar-filings/0001167483/13F-HR/"

print("Current working directory:", os.getcwd())
print("Exists?", os.path.exists(folder_path))
print("Contents:", os.listdir(folder_path))

filings = load_filings()
if not filings:
    st.error("No filings loaded — check your folder path or file structure.")
    st.stop()

turnover_df = compute_turnover(filings)

if turnover_df.empty:
    st.error("Turnover DataFrame is empty — likely due to date parsing issues.")
    st.stop()
st.title("Fund Turnover Dashboard")

years = sorted(turnover_df['from_year'].unique())
print("Turnover DataFrame columns:", turnover_df.columns.tolist())
print("Turnover DataFrame preview:\n", turnover_df.head())
start_year, end_year = st.slider(
    'Select Year Range',
    min_value=min(years),
    max_value=max(years),
    value=(min(years), max(years))
)

filtered_df = turnover_df[(turnover_df['from_year'] >= start_year) & (turnover_df['from_year'] <= end_year)]
st.write(f"Showing data from {start_year} to {end_year}")

fig, ax = plt.subplots(figsize=(10,5))
ax.plot(filtered_df['from_year'].astype(str) + "->" + filtered_df['to_year'].astype(str), filtered_df['turnover_pct'], marker='o')
plt.xticks(rotation=45)
ax.set_xlabel('Period')
ax.set_ylabel('Turnover Percentage')
ax.set_title('Turnover Percentage Over Time')
plt.grid(True)
st.pyplot(fig)

heatmap_df = turnover_df.pivot(index='from_year', columns='to_year', values='turnover_pct')
heatmap_df = heatmap_df.reset_index().melt(id_vars='from_year', var_name='to_year', value_name='turnover_pct')

fig = px.imshow(
    heatmap_df.pivot(index='from_year', columns='to_year', values='turnover_pct'),
    labels=dict(x="To Year", y="From Year", color="Turnover %"),
    x=sorted(turnover_df["to_year"].unique()),
    y=sorted(turnover_df["from_year"].unique()),
    color_continuous_scale="YlGnBu",
    aspect="auto"
)

st.subheader("Interactive Turnover Heatmap")
st.plotly_chart(fig, use_container_width=True)