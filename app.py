# Streamlit Prototype for Ross's Investment Dashboard
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_excel("Ross_Complete_Portfolio_System.xlsx", sheet_name="Holdings")
new_picks = pd.read_excel("Ross_Complete_Portfolio_System.xlsx", sheet_name="New Stock Picks")

# --- Sidebar ---
st.sidebar.title("Portfolio Controls")
user = st.sidebar.selectbox("User:", ["Ross"])
risk_profile = st.sidebar.selectbox("Select Risk Profile:", ["Aggressive", "Balanced", "Conservative"])

# --- Portfolio Overview ---
st.title("Ross's Investment Dashboard")
st.header("Portfolio Overview")

# Category Definitions
with st.expander("What do Core, Growth, and Speculative mean?"):
    st.markdown("**Core:** Stable, long-term holdings with reliable returns.")
    st.markdown("**Growth:** Medium-risk stocks with high upside potential.")
    st.markdown("**Speculative:** High-risk, high-reward stocks including penny stocks.")

# --- Latest Holdings Snapshot Table ---
st.subheader("Latest Holdings Snapshot")
snapshot_data = {
    "Ticker": ["MVST", "ATAI", "NVDA", "LSEG", "NEBIUS", "CREO", "JOBY", "BBAI", "CGEN", "AMZN"],
    "Company": ["Microvast", "ATAI Life Sciences", "Nvidia", "LSE Group", "Nebius Group NV", "Creo Medical", "Joby Aviation", "BigBear.ai", "Compugen", "Amazon"],
    "Current Value (£)": [2667.70, 1680.75, 1109.34, 1164.01, 1167.96, 538.40, 247.23, 1475.53, 1232.06, 1502.45],
    "Gain/Loss (£ / %)": ["+1491.81 (126.87%)", "+348.20 (26.13%)", "+144.80 (15.01%)", "+106.01 (10.02%)", "+108.14 (10.20%)", "+38.40 (7.68%)", "–2.40 (0.96%)", "–49.46 (3.24%)", "–119.26 (8.83%)", "–120.52 (7.43%)"]
}
st.dataframe(pd.DataFrame(snapshot_data))

# --- Allocation Summary ---
core = df[df["Category"] == "Core"]["Current Value (£)"].sum()
growth = df[df["Category"] == "Growth"]["Current Value (£)"].sum()
spec = df[df["Category"] == "Speculative"]["Current Value (£)"].sum()
total = core + growth + spec

st.metric("Core %", f"{core/total:.2%}")
st.metric("Growth %", f"{growth/total:.2%}")
st.metric("Speculative %", f"{spec/total:.2%}")

# --- Holdings Breakdown ---
st.header("Current Holdings")

# Table 1: Core Info
st.subheader("Core Information")
core_cols = ["Ticker", "Company", "Category", "Current Value (£)", "Current Weight %", "Portfolio %"]
st.dataframe(df[core_cols].round(2))

# Table 2: Analyst Data
st.subheader("Analyst Data")
analyst_cols = ["Ticker", "Current Stock Price", "Analyst Price High", "Analyst Price Low", "Analyst Price Target", "Target Price Upside (%)", "Number of Analysts", "Analyst Data Confidence", "Analyst Consensus Score"]
st.dataframe(df[analyst_cols].round(2))

# Table 3: Financial Fundamentals
st.subheader("Financial Fundamentals")
fundamental_cols = ["Ticker", "EPS Growth Score", "Revenue Growth Score"]
st.dataframe(df[fundamental_cols].round(2))

# Table 4: Other Information
st.subheader("Other Information")
used_cols = set(core_cols + analyst_cols + fundamental_cols)
remaining_cols = [col for col in df.columns if col not in used_cols]
st.dataframe(df[["Ticker"] + remaining_cols].round(2))

# --- New Picks ---
st.header("New Stock Picks")
st.write("These are new candidates for your consideration.")
for index, row in new_picks.iterrows():
    with st.expander(f"{row['Ticker']} - {row['Company']} (Score: {row['Score']})"):
        st.markdown(f"**Pros:** {row['Pros']}")
        st.markdown(f"**Cons:** {row['Cons']}")
        st.markdown("---")

if st.checkbox("Show Raw Data for New Picks"):
    st.dataframe(new_picks.round(2))

# --- Monthly Allocation ---
st.header("Monthly £500 Allocation")
allocations = df[df["Suggested Action"] != "Sell Entirely"]
allocations = allocations.sort_values(by="Adjusted Score (out of 100)", ascending=False).head(3)
amounts = [200, 150, 150]
for idx, row in enumerate(allocations.itertuples()):
    st.write(f"£{amounts[idx]} → {row.Ticker} ({row.Company}) — Score: {row._7:.2f}")

# --- Footer ---
st.markdown("---")
st.caption("Built by Ross")