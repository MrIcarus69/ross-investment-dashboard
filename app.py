# Streamlit Prototype for Ross's Investment Dashboard
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_excel("Ross_Complete_Portfolio_System_FINAL.xlsx", sheet_name="Holdings")
new_picks = pd.read_excel("Ross_Complete_Portfolio_System_FINAL.xlsx", sheet_name="New Stock Picks")

# --- Sidebar ---
st.sidebar.title("Portfolio Controls")
user = st.sidebar.selectbox("User:", ["Ross"])
risk_profile = st.sidebar.selectbox("Select Risk Profile:", ["Aggressive", "Balanced", "Conservative"])

# --- Portfolio Overview ---
st.title("Ross's Investment Dashboard")
st.header("Portfolio Overview")

# Allocation Summary
core = df[df["Category"] == "Core"]["Current Value (£)"].sum()
growth = df[df["Category"] == "Growth"]["Current Value (£)"].sum()
spec = df[df["Category"] == "Speculative"]["Current Value (£)"].sum()
total = core + growth + spec

st.subheader("Allocation Summary")
st.markdown(f"**Core (Stable, long-term holdings):** {core/total:.2%}")
st.markdown(f"**Growth (Medium-risk, high potential):** {growth/total:.2%}")
st.markdown(f"**Speculative (High-risk, high-reward):** {spec/total:.2%}")

# --- Latest Holdings Snapshot ---
st.subheader("Latest Holdings Snapshot")
snapshot_cols = ["Ticker", "Company", "Category", "Current Value (£)", "Sector", "Country"]
st.dataframe(df[snapshot_cols].sort_values(by="Current Value (£)", ascending=False).head(10).round(2))

# --- Current Holdings ---
st.header("Current Holdings")

# Table 1: Core Info
st.subheader("Core Information")
core_cols = ["Ticker", "Company", "Category", "Current Value (£)", "Portfolio %"]
st.dataframe(df[core_cols].round(2))

# Table 2: Analyst Data
st.subheader("Analyst Data")
analyst_cols = [
    "Ticker", "Current Stock Price", "Analyst Price High", "Analyst Price Low",
    "Analyst Price Target", "Target Price Upside (%)", "Number of Analysts",
    "Analyst Data Confidence", "Analyst Consensus Score"
]
st.dataframe(df[analyst_cols].round(2))

# Table 3: Financial Fundamentals
st.subheader("Financial Fundamentals")
fund_cols = [
    "Ticker", "EPS Growth Score", "Revenue Growth Score", "EPS (TTM)",
    "Revenue (TTM)", "Net Margin (%)", "Debt/Equity Ratio", "ROE (%)"
]
st.dataframe(df[fund_cols].round(2))

# Table 4: Other Information
st.subheader("Other Information")
used_cols = set(core_cols + analyst_cols + fund_cols)
remaining_cols = [col for col in df.columns if col not in used_cols and col != "Suggested Action"]
st.dataframe(df[["Ticker"] + remaining_cols].round(2))

# --- Suggested Actions
st.subheader("Suggested Actions")
actions_df = df[["Ticker", "Suggested Action"]]
st.dataframe(actions_df)

# --- New Stock Picks ---
st.header("New Stock Picks")

# Summary View
for index, row in new_picks.iterrows():
    with st.expander(f"{row['Ticker']} - {row['Company']} (Score: {row['Analyst Consensus Score']})"):
        st.markdown(f"**Category:** {row['Category']}")
        st.markdown(f"**Sector:** {row['Sector']}, **Country:** {row['Country']}")
        st.markdown(f"**Current Price:** £{row['Current Stock Price']}, **Target Upside:** {row['Target Price Upside (%)']}%")
        st.markdown("---")

# Tables matching holdings layout
st.subheader("New Picks — Analyst Data")
st.dataframe(new_picks[analyst_cols].round(2))

st.subheader("New Picks — Financial Fundamentals")
st.dataframe(new_picks[fund_cols].round(2))

st.subheader("New Picks — Other Information")
new_remaining_cols = [col for col in new_picks.columns if col not in used_cols and col != "Suggested Action"]
st.dataframe(new_picks[["Ticker"] + new_remaining_cols].round(2))

# --- Monthly Allocation ---
st.header("Monthly £500 Allocation")
candidates = pd.concat([df, new_picks])
candidates = candidates[candidates["Suggested Action"] != "Sell Entirely"]
top_allocations = candidates.sort_values(by="Analyst Consensus Score", ascending=False).head(3)

allocation_amounts = [200, 150, 150]
for i, row in enumerate(top_allocations.itertuples()):
    st.write(f"£{allocation_amounts[i]} → {row.Ticker} ({row.Company}) — Score: {row._analyst_consensus_score:.2f}")

# --- Footer ---
st.markdown("---")
st.caption("Built by Ross")
