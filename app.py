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

# Category Definitions beside metrics
core = df[df["Category"] == "Core"]["Current Value (£)"].sum()
growth = df[df["Category"] == "Growth"]["Current Value (£)"].sum()
spec = df[df["Category"] == "Speculative"]["Current Value (£)"].sum()
total = core + growth + spec

col1, col2, col3 = st.columns(3)
col1.metric("Core %", f"{core/total:.2%}")
col1.caption("Stable, long-term holdings with reliable returns.")
col2.metric("Growth %", f"{growth/total:.2%}")
col2.caption("Medium-risk stocks with high upside potential.")
col3.metric("Speculative %", f"{spec/total:.2%}")
col3.caption("High-risk, high-reward stocks including penny stocks.")

# --- Latest Holdings Snapshot Table ---
st.subheader("Latest Holdings Snapshot")
snapshot_cols = ["Ticker", "Company", "Category", "Current Value (£)", "Gain/Loss (£ / %)", "Country", "Sector"]
if set(snapshot_cols).issubset(df.columns):
    st.dataframe(df[snapshot_cols].sort_values(by="Current Value (£)", ascending=False).round(2))
else:
    st.warning("Some expected columns for snapshot table are missing.")

# --- Country Allocation Pie Chart ---
st.subheader("Allocation by Country")
country_map = {
    "US": "United States", "UK": "United Kingdom", "RU": "Russia", "IL": "Israel",
    "DE": "Germany", "FR": "France", "CN": "China", "NL": "Netherlands"
}
df["Country Group"] = df["Country"].map(lambda x: (
    "US" if x == "US" else
    "UK" if x == "UK" else
    "Asia" if x in ["CN", "IN", "JP", "SG"] else
    "Europe" if x in ["FR", "DE", "NL", "ES", "IT", "SE", "FI", "NO", "DK"] else
    "Rest of World"
))
country_data = df.groupby("Country Group")["Current Value (£)"].sum()
fig3, ax3 = plt.subplots()
ax3.pie(country_data, labels=country_data.index, autopct='%1.1f%%', startangle=90)
ax3.axis('equal')
st.pyplot(fig3)

# --- Sector Allocation Pie Chart ---
st.subheader("Allocation by Sector")
if "Sector" in df.columns:
    sector_data = df.groupby("Sector")["Current Value (£)"].sum()
    fig4, ax4 = plt.subplots()
    ax4.pie(sector_data, labels=sector_data.index, autopct='%1.1f%%', startangle=90)
    ax4.axis('equal')
    st.pyplot(fig4)

# --- Analyst Data Table ---
st.subheader("Analyst Data")
analyst_cols = [
    "Ticker", "Current Stock Price", "Analyst Price High", "Analyst Price Low", "Analyst Price Target",
    "Target Price Upside (%)", "Number of Analysts", "Analyst Data Confidence", "Analyst Consensus Score"
]
st.dataframe(df[analyst_cols].round(2))

# --- Financial Fundamentals Table ---
st.subheader("Financial Fundamentals")
fund_cols = [
    "Ticker", "EPS Growth Score", "Revenue Growth Score",
    "EPS Last 12M", "EPS Next 12M", "Revenue Last FY (£)", "Revenue Next FY (£)"
]
st.dataframe(df[fund_cols].round(2))

# --- Other Information Table ---
st.subheader("Other Information")
all_displayed_cols = analyst_cols + fund_cols + snapshot_cols
remaining_cols = [col for col in df.columns if col not in all_displayed_cols and col != "Suggested Action"]
st.dataframe(df[["Ticker"] + remaining_cols].round(2))

# --- Suggested Actions Table ---
st.subheader("Suggested Actions")
action_table = df[["Ticker", "Suggested Action"]]
st.dataframe(action_table)

# --- New Stock Picks Section ---
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
combined = pd.concat([df, new_picks], sort=False)
combined = combined[combined["Suggested Action"] != "Sell Entirely"]
combined = combined.sort_values(by="Adjusted Score (out of 100)", ascending=False).head(10)
amounts = [200, 150, 100, 50] + [0]*(len(combined)-4)
for idx, row in enumerate(combined.itertuples()):
    if idx < len(amounts) and amounts[idx] > 0:
        st.write(f"£{amounts[idx]} → {row.Ticker} ({row.Company}) — Score: {row._7:.2f}")

# --- Footer ---
st.markdown("---")
st.caption("Built by Ross")