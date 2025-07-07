import streamlit as st
from processing import compute_turnover, extract_info_table_xml, parse_info_table_xml

folder_path = "./sec-edgar-filings/0001167483/13F-HR/"
filings = []


turnover_df = compute_turnover(filings)

st.title("Fund Turnover Dashboard")

years = sorted(turnover_df['from_year'].unique())
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