# 13F-trend-analysis
Data scraper to visualise 13F holding data, analysing trends in turnover with interactive features.

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
