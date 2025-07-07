import streamlit as st
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