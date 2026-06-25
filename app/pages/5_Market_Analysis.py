import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Market Analysis",
    page_icon="🌍",
    layout="wide"
)

# ==========================================
# LOAD DATA
# ==========================================

@st.cache_data
def load_data():

    project_root = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../.."
        )
    )

    file_path = os.path.join(
        project_root,
        "data",
        "processed",
        "cleaned_data.csv"
    )

    return pd.read_csv(file_path)

df = load_data()

# ==========================================
# TITLE
# ==========================================

st.title("🌍 Market & Regional Analysis")

st.markdown("""
Analyze profitability across markets,
regions and countries.
""")

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Filters")

selected_market = st.sidebar.multiselect(
    "Market",
    sorted(df["Market"].unique()),
    default=sorted(df["Market"].unique())
)

filtered_df = df[
    df["Market"].isin(selected_market)
]

# ==========================================
# MARKET AGGREGATION
# ==========================================

market_df = (
    filtered_df.groupby("Market")
    .agg(
        Revenue=("Sales","sum"),
        Profit=("Order Profit Per Order","sum")
    )
    .reset_index()
)

market_df["Margin"] = (
    market_df["Profit"]
    /
    market_df["Revenue"]
) * 100

# ==========================================
# KPIs
# ==========================================

best_market = market_df.loc[
    market_df["Profit"].idxmax(),
    "Market"
]

worst_market = market_df.loc[
    market_df["Profit"].idxmin(),
    "Market"
]

avg_margin = market_df["Margin"].mean()

total_markets = market_df.shape[0]

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "Markets",
        total_markets
    )

with c2:
    st.metric(
        "Best Market",
        best_market
    )

with c3:
    st.metric(
        "Worst Market",
        worst_market
    )

with c4:
    st.metric(
        "Avg Margin",
        f"{avg_margin:.2f}%"
    )

st.divider()

# ==========================================
# MARKET PROFITABILITY
# ==========================================

st.subheader("Market Profitability")

fig = px.bar(
    market_df.sort_values(
        "Profit",
        ascending=False
    ),
    x="Market",
    y="Profit",
    color="Profit",
    text="Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# MARKET MARGIN
# ==========================================

st.subheader("Market Margin Analysis")

fig = px.bar(
    market_df.sort_values(
        "Margin",
        ascending=False
    ),
    x="Market",
    y="Margin",
    color="Margin",
    text="Margin"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# REGION ANALYSIS
# ==========================================

st.subheader("Regional Performance")

region_df = (
    filtered_df.groupby(
        "Order Region"
    )
    .agg(
        Revenue=("Sales","sum"),
        Profit=("Order Profit Per Order","sum")
    )
    .reset_index()
)

fig = px.bar(
    region_df.sort_values(
        "Profit",
        ascending=False
    ),
    x="Order Region",
    y="Profit",
    color="Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# COUNTRY ANALYSIS
# ==========================================

st.subheader("Top Countries by Profit")

country_df = (
    filtered_df.groupby(
        "Order Country"
    )
    .agg(
        Revenue=("Sales","sum"),
        Profit=("Order Profit Per Order","sum")
    )
    .reset_index()
)

top_countries = (
    country_df.sort_values(
        "Profit",
        ascending=False
    )
    .head(15)
)

fig = px.bar(
    top_countries,
    x="Profit",
    y="Order Country",
    orientation="h"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# MARKET SHARE
# ==========================================

st.subheader("Profit Share by Market")

fig = px.pie(
    market_df,
    names="Market",
    values="Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# GEO MAP
# ==========================================

st.subheader("Geographical Profit Distribution")

geo_df = (
    filtered_df.groupby(
        "Order Country"
    )
    .agg(
        Profit=("Order Profit Per Order","sum")
    )
    .reset_index()
)

fig = px.choropleth(
    geo_df,
    locations="Order Country",
    locationmode="country names",
    color="Profit",
    hover_name="Order Country"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# MARKET TABLE
# ==========================================

st.subheader("Market Summary Table")

st.dataframe(
    market_df.sort_values(
        "Profit",
        ascending=False
    ),
    use_container_width=True
)

# ==========================================
# INSIGHTS
# ==========================================

st.subheader("Business Insights")

st.success(
    f"""
### Strategic Findings

✅ Best Performing Market:
{best_market}

⚠️ Weakest Market:
{worst_market}

✅ Average Margin:
{avg_margin:.2f}%

### Recommendations

• Invest more in profitable markets

• Review weak-performing regions

• Optimize pricing by geography

• Expand high-margin countries

• Use regional profitability for planning
"""
)