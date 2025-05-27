
# Streamlit App for Ross's Investment Dashboard
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_excel("Ross_Complete_Portfolio_System_FINAL.xlsx", sheet_name="Holdings")

# Sidebar controls
st.sidebar.title("Portfolio Controls")
user = st.sidebar.selectbox("User:", ["Ross"])
risk_profile = st.sidebar.selectbox("Risk Profile:", ["Aggressive", "Balanced", "Conservative"])

# Portfolio Overview
st.title("Ross's Investment Dashboard")
st.header("Portfolio Overview")

# Category percentages
core = df[df["Category"] == "Core"]["Current Value (£)"].sum()
growth = df[df["Category"] == "Growth"]["Current Value (£)"].sum()
spec = df[df["Category"] == "Speculative"]["Current Value (£)"].sum()
total = core + growth + spec

col1, col2, col3 = st.columns(3)
col1.metric("Core %", f"{core/total:.2%}")
col1.caption("Stable, long-term holdings")
col2.metric("Growth %", f"{growth/total:.2%}")
col2.caption("Medium-risk, high upside")
col3.metric("Speculative %", f"{spec/total:.2%}")
col3.caption("High-risk, high-reward bets")

# Latest Holdings Snapshot
st.subheader("Latest Holdings Snapshot")
snapshot_cols = ["Ticker", "Company", "Current Value (£)", "Category", "Sector", "Country"]
st.dataframe(df[snapshot_cols].sort_values(by="Current Value (£)", ascending=False).round(2))

# Core Info Table
st.subheader("Core Information")
core_cols = ["Ticker", "Company", "Category", "Current Value (£)", "Current Weight %"]
st.dataframe(df[core_cols].round(2))

# Analyst Data Table
st.subheader("Analyst Data")
analyst_cols = [
    "Ticker", "Current Stock Price", "Analyst Price High", "Analyst Price Low",
    "Analyst Price Target", "Target Price Upside (%)", "Number of Analysts",
    "Analyst Data Confidence", "Analyst Consensus Score"
]
st.dataframe(df[analyst_cols].round(2))

# Financial Fundamentals Table
st.subheader("Financial Fundamentals")
fund_cols = ["Ticker", "EPS Growth Score", "Revenue Growth Score"]
st.dataframe(df[fund_cols].round(2))

# Other Info Table (minus suggested action for now)
st.subheader("Other Information")
exclude_cols = set(core_cols + analyst_cols + fund_cols)
other_cols = [col for col in df.columns if col not in exclude_cols and col != "Suggested Action"]
st.dataframe(df[["Ticker"] + other_cols].round(2))

# Suggested Actions Table
st.subheader("Suggested Actions")
st.dataframe(df[["Ticker", "Suggested Action"]])

# Footer
st.markdown("---")
st.caption("Built by Ross")
