# 13F-trend-analysis
Data scraper to visualise 13F holding data, analysing trends in turnover with interactive features.

![GitHub last commit](https://img.shields.io/github/last-commit/087narain/13F-trend-analysis)
![GitHub repo size](https://img.shields.io/github/repo-size/087narain/13F-trend-analysis)
![GitHub stars](https://img.shields.io/github/stars/087narain/13F-trend-analysis?style=social)
![Issues](https://img.shields.io/github/issues/087narain/13F-trend-analysis)

![EDGAR](https://img.shields.io/badge/Data%20Source-SEC%20EDGAR-blue)
![Python Version](https://img.shields.io/badge/Python-3.9+-blue.svg)

### 🚀 Technologies Used

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=Jupyter&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-007ACC?style=for-the-badge&logo=matplotlib&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-7CBAFF?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## Features:
- Parsing & cleaning of 13F-HR filings taken from EDGAR 
- Turnover analysis - tracking new buys, full exits & position retention over time.
- Interactive dashboard built with Streamlit, showing visualisations
- Visual comparison across years via the turnover heatmap

## Methodology:
- Data was collected via the SEC's EDGAR interface, focusing on Tiger Global funds.
- Focused on parsing filings from 2016 onwards, as they follow the HTML-like format 
- This made the parsing more scalable
- Turnover was defined as: (new buys + exits) / average of positions across quarters

## Figures
- 3 figures attached taken from the notebook: `cleaned turnover_over_time.png`, `heatmap.png`, and `new buys & exits.png`

## Future improvements:
- Sector-level analysis was not implemented due to CUSIP-to-sector mappings requiring a paid API or database. Integrating open-source or scraped ticker mappings in the future could allow for sector-wise turnover trends.
- The dashboard could be extended to include multiple fund comparisons, filtering by holding value or position size
