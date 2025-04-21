import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import matplotlib.pyplot as plt
import os
from bs4 import BeautifulSoup

# --------------------------- Functions ---------------------------

def get_financial_news():
    headlines = []
    urls = {
        "Moneycontrol": "https://www.moneycontrol.com/news/business/",
        "Livemint": "https://www.livemint.com/market",
        "ETMoney": "https://economictimes.indiatimes.com/markets"
    }
    
    for source, url in urls.items():
        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(res.text, 'html.parser')
            articles = soup.find_all('a')[:5]
            for a in articles:
                text = a.get_text(strip=True)
                if text:
                    headlines.append(f"{source}: {text}")
        except Exception as e:
            headlines.append(f"{source}: Unable to fetch news")
    return headlines

def generate_market_report():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Market Insights Report - {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='C')

    headlines = get_financial_news()
    pdf.ln(10)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Today's Headlines:", ln=True)

    for line in headlines:
        pdf.multi_cell(0, 10, txt=f"- {line}")

    filename = "market_insight_report.pdf"
    pdf.output(filename)
    return filename

def get_sebi_investigations():
    investigations = []
    # Placeholder: Replace with actual SEBI scraping logic
    sample_data = [
        {"company": "ABC Ltd", "reason": "Insider trading", "market_cap": 1200},
        {"company": "XYZ Corp", "reason": "Fraudulent reporting", "market_cap": 850},
        {"company": "TinyCap Inc", "reason": "Mismanagement", "market_cap": 200},
    ]
    for entry in sample_data:
        if entry['market_cap'] >= 500:
            investigations.append(f"SEBI investigates {entry['company']} for {entry['reason']}.")
    return investigations

# --------------------------- UI ---------------------------

st.title("📈 Daily Market Report & 🕵️ SEBI Shade Check")

# Market Report
if st.button("📄 Generate Market Insight Report"):
    report_path = generate_market_report()
    with open(report_path, "rb") as f:
        st.download_button("Download Market Report", f, file_name=report_path, mime="application/pdf")

# Shade Check
if st.button("🔍 Shade Check - SEBI Investigations"):
    st.subheader("SEBI Investigations (Companies > ₹500Cr Market Cap)")
    shades = get_sebi_investigations()
    for line in shades:
        st.write(f"- {line}")
