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

core = df[df["Category"] == "Core"]["Current Value (£)"].sum()
growth = df[df["Category"] == "Growth"]["Current Value (£)"].sum()
spec = df[df["Category"] == "Speculative"]["Current Value (£)"].sum()
total = core + growth + spec

st.metric("Core %", f"{core/total:.2%}")
st.metric("Growth %", f"{growth/total:.2%}")
st.metric("Speculative %", f"{spec/total:.2%}")

# --- Last Uploaded Holdings Summary ---
st.subheader("Latest Holdings Snapshot")
df_sorted = df.sort_values(by="Adjusted Score (out of 100)", ascending=False)
for idx, row in df_sorted.iterrows():
    st.write(f"{row['Ticker']}: {row['Company']} — Score: {row['Adjusted Score (out of 100)']:.2f}, Suggested Action: {row['Suggested Action']}")
    if idx == 4:
        break

# --- Category Allocation Pie Chart ---
st.subheader("Allocation by Category")
categories = ["Core", "Growth", "Speculative"]
values = [core, growth, spec]
fig1, ax1 = plt.subplots()
ax1.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')
st.pyplot(fig1)

# --- Target vs Actual Bar Chart ---
st.subheader("Target vs Actual Allocation")
targets = [15, 35, 50]
actuals = [core/total*100, growth/total*100, spec/total*100]
fig2, ax2 = plt.subplots()
bar_width = 0.35
r1 = range(len(categories))
r2 = [x + bar_width for x in r1]
ax2.bar(r1, targets, width=bar_width, label='Target')
ax2.bar(r2, actuals, width=bar_width, label='Actual')
ax2.set_xticks([r + bar_width/2 for r in r1])
ax2.set_xticklabels(categories)
ax2.legend()
st.pyplot(fig2)

# --- Country Allocation Pie Chart ---
st.subheader("Allocation by Region")
def map_to_region(country):
    if country in ["US", "CA"]:
        return "US"
    elif country in ["CN", "JP", "KR", "IN"]:
        return "Asia"
    elif country in ["UK"]:
        return "UK"
    elif country in ["DE", "FR", "IT", "ES", "NL", "SE"]:
        return "Europe"
    else:
        return "Rest of World"

df["Region"] = df["Country"].apply(map_to_region)
region_data = df.groupby("Region")["Current Value (£)"].sum()
fig3, ax3 = plt.subplots()
ax3.pie(region_data, labels=region_data.index, autopct='%1.1f%%', startangle=90)
ax3.axis('equal')
st.pyplot(fig3)

# --- Sector Allocation Pie Chart ---
st.subheader("Allocation by Sector")
sector_data = df.groupby("Sector")["Current Value (£)"].sum()
fig4, ax4 = plt.subplots()
ax4.pie(sector_data, labels=sector_data.index, autopct='%1.1f%%', startangle=90)
ax4.axis('equal')
st.pyplot(fig4)

# --- Holdings Table ---
st.header("Current Holdings — Full View")
st.dataframe(df.round(2))

# --- New Picks ---
st.header("New Stock Picks")
st.write("These are new candidates for your consideration.")
for index, row in new_picks.iterrows():
    with st.expander(f"{row['Ticker']} - {row['Company']} (Score: {row['Score']})"):
        st.markdown(f"**Pros:** {row['Pros']}")
        st.markdown(f"**Cons:** {row['Cons']}")
        st.markdown("---")

# --- Toggle to Show New Picks Raw Data ---
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