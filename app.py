# Streamlit Prototype for Ross's Investment Dashboard
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data (normally would connect to your spreadsheet or database)
df = pd.read_excel("Ross_Complete_Portfolio_System.xlsx", sheet_name="Holdings")
new_picks = pd.read_excel("Ross_Complete_Portfolio_System.xlsx", sheet_name="New Stock Picks")

# --- Sidebar ---
st.sidebar.title("Portfolio Controls")
risk_profile = st.sidebar.selectbox("Select Risk Profile:", ["Aggressive", "Balanced", "Conservative"])

# --- Portfolio Overview ---
st.title("Ross's Investment Dashboard")
st.header("Portfolio Overview")

core = df[df["Category"] == "Core"]["Current Value (£)"].sum()
growth = df[df["Category"] == "Growth"]["Current Value (£)"].sum()
spec = df[df["Category"] == "Speculative"]["Current Value (£)"].sum()
total = core + growth + spec

st.metric("Core %", f"{core/total:.1%}")
st.metric("Growth %", f"{growth/total:.1%}")
st.metric("Speculative %", f"{spec/total:.1%}")

# --- Category Allocation Pie Chart ---
st.subheader("Allocation by Category")
categories = ["Core", "Growth", "Speculative"]
values = [core, growth, spec]
fig1, ax1 = plt.subplots()
ax1.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig1)

# --- Holdings Table ---
st.header("Current Holdings")
selected_status = st.selectbox("Filter by Sell Alert:", ["All", "Yes", "No"])
if selected_status != "All":
    filtered_df = df[df["Sell Alert?"] == selected_status]
else:
    filtered_df = df

st.dataframe(filtered_df[["Ticker", "Company", "Category", "Adjusted Score (out of 100)", "Sell Alert?", "Suggested Action"]])

# --- New Picks ---
st.header("New Stock Picks")
st.write("These are new candidates for your consideration.")
for index, row in new_picks.iterrows():
    with st.expander(f"{row['Ticker']} - {row['Company']} (Score: {row['Score']})"):
        st.markdown(f"**Pros:** {row['Pros']}")
        st.markdown(f"**Cons:** {row['Cons']}")
        st.markdown("---")

# --- Monthly Allocation ---
st.header("Monthly £500 Allocation")
allocations = df[df["Suggested Action"] != "Sell Entirely"]
allocations = allocations.sort_values(by="Adjusted Score (out of 100)", ascending=False).head(3)
amounts = [200, 150, 150]  # Example distribution
for idx, row in enumerate(allocations.itertuples()):
    st.write(f"£{amounts[idx]} → {row.Ticker} ({row.Company}) — Score: {row._7}")