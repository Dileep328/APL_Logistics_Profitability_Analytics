import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# Load Data
# ==========================================

@st.cache_data
def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)


st.sidebar.header("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload cleaned_data.csv",
    type=["csv"]
)

if uploaded_file is None:
    st.warning(
        "Please upload cleaned_data.csv to continue."
    )
    st.stop()

df = load_data(uploaded_file)

# ==========================================
# Title
# ==========================================

st.title("📊 APL Logistics Executive Dashboard")

st.markdown(
"""
### Customer, Product & Profitability Performance Analysis

This dashboard provides:

- Revenue & Profit Overview
- Customer Insights
- Product Performance
- Market Analysis
- Profitability Intelligence
"""
)

st.divider()

# ==========================================
# KPIs
# ==========================================

total_revenue = df["Sales"].sum()

total_profit = df["Order Profit Per Order"].sum()

profit_margin = (
    total_profit / total_revenue
) * 100

total_customers = df["Customer Id"].nunique()

# ==========================================
# KPI CARDS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Revenue",
        f"${total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "📈 Profit",
        f"${total_profit:,.0f}"
    )

with col3:
    st.metric(
        "🎯 Profit Margin",
        f"{profit_margin:.2f}%"
    )

with col4:
    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

st.divider()

# ==========================================
# Revenue vs Profit
# ==========================================

st.subheader("Revenue vs Profit")

revenue_profit_df = pd.DataFrame(
    {
        "Metric": ["Revenue", "Profit"],
        "Value": [
            total_revenue,
            total_profit
        ]
    }
)

fig = px.bar(
    revenue_profit_df,
    x="Metric",
    y="Value",
    text="Value",
    title="Revenue vs Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# Customer Segment Analysis
# ==========================================

st.subheader("Customer Segment Performance")

segment_df = (
    df.groupby("Customer Segment")
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum")
    )
    .reset_index()
)

fig = px.bar(
    segment_df,
    x="Customer Segment",
    y=["Revenue", "Profit"],
    barmode="group",
    title="Revenue & Profit by Customer Segment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# Market Analysis
# ==========================================

st.subheader("Market Profitability")

market_df = (
    df.groupby("Market")
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum")
    )
    .reset_index()
)

market_df["Margin"] = (
    market_df["Profit"] /
    market_df["Revenue"]
) * 100

fig = px.bar(
    market_df,
    x="Market",
    y="Margin",
    color="Margin",
    text="Margin",
    title="Profit Margin by Market"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# Profit Distribution
# ==========================================

st.subheader("Profit Distribution")

fig = px.histogram(
    df,
    x="Order Profit Per Order",
    nbins=50,
    title="Order Profit Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# Top Markets
# ==========================================

st.subheader("Top Markets by Profit")

top_markets = (
    market_df.sort_values(
        by="Profit",
        ascending=False
    )
)

fig = px.bar(
    top_markets,
    x="Market",
    y="Profit",
    text="Profit",
    title="Market Profit Ranking"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# Executive Insights
# ==========================================

st.subheader("Executive Insights")

best_market = market_df.loc[
    market_df["Margin"].idxmax(),
    "Market"
]

worst_market = market_df.loc[
    market_df["Margin"].idxmin(),
    "Market"
]

st.success(
    f"""
### Key Business Findings

✅ Total Revenue: ${total_revenue:,.0f}

✅ Total Profit: ${total_profit:,.0f}

✅ Profit Margin: {profit_margin:.2f}%

✅ Best Market: {best_market}

⚠️ Lowest Margin Market: {worst_market}

### Recommendations

• Focus on high-profit customers

• Reduce excessive discounting

• Expand profitable markets

• Monitor loss-making transactions

• Use ML predictions for pricing decisions
"""
)