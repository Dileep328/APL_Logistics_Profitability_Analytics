import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Discount Impact Analyzer",
    page_icon="💸",
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

st.title("💸 Discount Impact Analyzer")

st.markdown("""
Analyze how discounts affect profitability and margins.
""")

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("Discount Filter")

max_discount = float(
    df["Order Item Discount Rate"].max()
)

selected_discount = st.sidebar.slider(
    "Maximum Discount Rate",
    0.0,
    max_discount,
    max_discount
)

filtered_df = df[
    df["Order Item Discount Rate"]
    <= selected_discount
]

# ==========================================
# KPIs
# ==========================================

avg_discount = (
    filtered_df[
        "Order Item Discount Rate"
    ].mean()
) * 100

avg_margin = (
    filtered_df[
        "Profit_Margin"
    ].mean()
)

total_profit = (
    filtered_df[
        "Order Profit Per Order"
    ].sum()
)

loss_orders = (
    filtered_df[
        "Order Profit Per Order"
    ] < 0
).sum()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Avg Discount",
        f"{avg_discount:.2f}%"
    )

with c2:
    st.metric(
        "Avg Margin",
        f"{avg_margin:.2f}%"
    )

with c3:
    st.metric(
        "Total Profit",
        f"${total_profit:,.0f}"
    )

with c4:
    st.metric(
        "Loss Orders",
        loss_orders
    )

st.divider()

# ==========================================
# DISCOUNT BUCKET ANALYSIS
# ==========================================

st.subheader(
    "Margin by Discount Bucket"
)

bucket_df = (
    filtered_df.groupby(
        "Discount_Bucket"
    )
    .agg(
        Avg_Margin=(
            "Profit_Margin",
            "mean"
        ),
        Avg_Profit=(
            "Order Profit Per Order",
            "mean"
        )
    )
    .reset_index()
)

fig = px.bar(
    bucket_df,
    x="Discount_Bucket",
    y="Avg_Margin",
    text="Avg_Margin",
    color="Avg_Margin"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# DISCOUNT VS PROFIT
# ==========================================

st.subheader(
    "Discount vs Profit"
)

sample_df = filtered_df.sample(
    min(5000, len(filtered_df)),
    random_state=42
)

fig = px.scatter(
    sample_df,
    x="Order Item Discount Rate",
    y="Order Profit Per Order",
    title="Discount Impact on Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# DISCOUNT VS MARGIN
# ==========================================

st.subheader(
    "Discount vs Margin"
)

fig = px.scatter(
    sample_df,
    x="Order Item Discount Rate",
    y="Profit_Margin"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# WHAT IF ANALYSIS
# ==========================================

st.subheader(
    "What-If Discount Scenario"
)

scenario_discount = st.slider(
    "Apply Hypothetical Discount %",
    0,
    50,
    10
)

estimated_margin = (
    avg_margin -
    (scenario_discount * 0.4)
)

st.info(
    f"""
Estimated Margin after applying
{scenario_discount}% discount:

{estimated_margin:.2f}%
"""
)

# ==========================================
# DISCOUNT THRESHOLD
# ==========================================

st.subheader(
    "Discount Threshold Detection"
)

threshold_df = (
    filtered_df.groupby(
        "Discount_Bucket"
    )["Profit_Margin"]
    .mean()
)

st.dataframe(
    threshold_df,
    use_container_width=True
)

# ==========================================
# TOP DISCOUNTED PRODUCTS
# ==========================================

st.subheader(
    "Top Discounted Products"
)

discount_product = (
    filtered_df.groupby(
        "Product Name"
    )
    ["Order Item Discount Rate"]
    .mean()
    .sort_values(
        ascending=False
    )
    .head(10)
    .reset_index()
)

fig = px.bar(
    discount_product,
    x="Order Item Discount Rate",
    y="Product Name",
    orientation="h"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# INSIGHTS
# ==========================================

st.subheader(
    "Business Insights"
)

st.success(
    """
### Key Findings

✅ Higher discounts generally reduce profit margins

✅ Excessive discounts create loss-making orders

✅ Several products rely heavily on discounting

### Recommendations

• Set discount approval limits

• Monitor products with high discounts

• Review pricing strategy

• Focus on sustainable margins instead of revenue alone
"""
)