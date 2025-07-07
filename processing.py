from sec_edgar_downloader import Downloader
from bs4 import BeautifulSoup
from datetime import datetime


import os
import re
import requests
import unicodedata
import pandas as pd
import csv
import xml.etree.ElementTree as ET
import yfinance as yf
import streamlit as st

def extract_info_table_xml(txt_file_path):
    """
    Extracts the XML string within <INFORMATIONTABLE> tags from the full .txt filing.
    """
    with open(txt_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Use regex to extract everything between <INFORMATIONTABLE>...</INFORMATIONTABLE>
    match = re.search(r"<INFORMATIONTABLE[\s\S]*?</INFORMATIONTABLE>", content, re.IGNORECASE)

    if match:
        return match.group(0)
    else:
        return None  

def parse_info_table_xml(xml_string):
    """
    Parses the extracted XML string into a list of holdings as a pandas DataFrame.
    """
    xml_string_clean = re.sub(r'\sxmlns="[^"]+"', '', xml_string, count=1)

    root = ET.fromstring(xml_string_clean)

    data = []
    for info in root.findall("infoTable"):
        row = {}
        for child in info:
            if list(child): 
                for subchild in child:
                    tag = subchild.tag.strip()
                    text = subchild.text.strip() if subchild.text else ''
                    row[tag] = text
            else:
                tag = child.tag.strip()
                text = child.text.strip() if child.text else ''
                row[tag] = text
        data.append(row)

    return pd.DataFrame(data)
    
def filter_2016(folder_name):
    match = re.search(r'-([0-9]{2})-', folder_name)
    if match:
        year_suffix = int(match.group(1))
        year = 2000 + year_suffix
        return year > 2016
    return False

def extract_date(accession):
    match = re.search(r'(\d{4})(\d{2})(\d{2})', accession)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
    else:
        return accession

def load_filings():
    folder_path = "./sec-edgar-filings/0001167483/13F-HR/"
    holdings = []
    filings = []

    for folder in os.listdir(folder_path):
        if not filter_2016(folder):
            continue

        access_folder_path = os.path.join(folder_path, folder)

        for file in os.listdir(access_folder_path):
            if file.endswith(".txt"):
                file_path = os.path.join(access_folder_path, file)
                print(f"Processing: {file_path}")
                
                xml_str = extract_info_table_xml(file_path)
                if xml_str:
                    df = parse_info_table_xml(xml_str)
                    df["source_file"] = file
                    df["accession"] = folder

                    date_match = re.search(r'(\d{4}-\d{2}-\d{2})', folder)  
                    if not date_match:
                        date_match = re.search(r'(\d{4}-\d{2}-\d{2})', file)  
                    date = date_match.group(1) if date_match else "Unknown"

                    filings.append({
                        "date": date,
                        "df": df
                    })
                    holdings.append(df)

    return filings

def clean_and_compute_allocation(df):
    cols_for_numeric = ['value', 'sshPrnamt', 'Sole', 'Shared', 'None']
    
    for col in cols_for_numeric:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df = df.dropna(subset=['value'])
    
    total_value = df['value'].sum()
    
    df['%_allocation'] = 100 * (df['value'] / total_value)
    
    return df 

## Function to track how the holdings in filings change
def holdings_compare(df_1, df_2):
    prev_set = set(df_1['cusip'])
    curr_set = set(df_2['cusip'])

    new_buys = curr_set - prev_set
    full_exits = prev_set - curr_set
    kept = prev_set & curr_set

    return {
        'new_buys': len(new_buys),
        'exits': len(full_exits),
        'kept': len(kept),
        'total_prev': len(prev_set),
        'total_curr': len(curr_set),
        'turnover_pct': (len(new_buys | full_exits) / ((len(prev_set) + len(curr_set)) / 2)) * 100
    }

def compute_turnover(filings):
    # Fix year extraction to first part of date string (year)
    for f in filings:
        f['year'] = int(f['date'].split('-')[0])

    turnover_results = []
    year_to_filing = {f['year']: f for f in filings}
    sorted_years = sorted(year_to_filing.keys())

    for i in range(1, len(sorted_years)):
        prev_year = sorted_years[i-1]
        curr_year = sorted_years[i]

        if curr_year == prev_year + 1:
            prev = year_to_filing[prev_year]
            curr = year_to_filing[curr_year]

            comparison = holdings_compare(prev['df'], curr['df'])
            comparison['period'] = f"{prev['date']} -> {curr['date']}"
            comparison['from_year'] = prev_year
            comparison['to_year'] = curr_year
        
            turnover_results.append(comparison)

    turnover_df = pd.DataFrame(turnover_results)
    return turnover_df

