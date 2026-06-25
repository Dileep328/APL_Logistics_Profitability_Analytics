import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# Page Config
# ==========================================

st.set_page_config(
    page_title="Customer Analytics",
    page_icon="👥",
    layout="wide"
)

# ==========================================
# Load Data
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
# Title
# ==========================================

st.title("👥 Customer Analytics Dashboard")

st.markdown(
"""
Analyze customer profitability, revenue contribution,
and identify high-value customers.
"""
)

# ==========================================
# Sidebar Filters
# ==========================================

st.sidebar.header("Filters")

segment = st.sidebar.multiselect(
    "Customer Segment",
    options=sorted(df["Customer Segment"].unique()),
    default=sorted(df["Customer Segment"].unique())
)

market = st.sidebar.multiselect(
    "Market",
    options=sorted(df["Market"].unique()),
    default=sorted(df["Market"].unique())
)

filtered_df = df[
    (df["Customer Segment"].isin(segment))
    &
    (df["Market"].isin(market))
]

# ==========================================
# Customer Aggregation
# ==========================================

customer_df = (
    filtered_df.groupby(
        ["Customer Id", "Customer_Full_Name"]
    )
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum"),
        Orders=("Customer Id", "count")
    )
    .reset_index()
)

# ==========================================
# KPI Cards
# ==========================================

total_customers = customer_df.shape[0]

profitable_customers = (
    customer_df["Profit"] > 0
).sum()

loss_customers = (
    customer_df["Profit"] < 0
).sum()

avg_profit = customer_df["Profit"].mean()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Customers",
        total_customers
    )

with c2:
    st.metric(
        "Profitable Customers",
        profitable_customers
    )

with c3:
    st.metric(
        "Loss Making Customers",
        loss_customers
    )

with c4:
    st.metric(
        "Avg Profit",
        f"${avg_profit:,.0f}"
    )

st.divider()

# ==========================================
# Top Customers
# ==========================================

st.subheader("🏆 Top 10 Customers by Profit")

top_customers = (
    customer_df
    .sort_values(
        "Profit",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    top_customers,
    x="Customer_Full_Name",
    y="Profit",
    text="Profit",
    title="Top Customers by Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# Bottom Customers
# ==========================================

st.subheader("⚠️ Bottom 10 Customers by Profit")

bottom_customers = (
    customer_df
    .sort_values(
        "Profit"
    )
    .head(10)
)

fig = px.bar(
    bottom_customers,
    x="Customer_Full_Name",
    y="Profit",
    text="Profit",
    title="Loss Making Customers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# Revenue vs Profit
# ==========================================

st.subheader("Revenue vs Profit by Customer")

sample_df = customer_df.sample(
    min(1000, len(customer_df)),
    random_state=42
)

fig = px.scatter(
    sample_df,
    x="Revenue",
    y="Profit",
    size="Orders",
    hover_name="Customer_Full_Name",
    title="Customer Revenue vs Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# Pareto Analysis
# ==========================================

st.subheader("80/20 Profit Contribution Analysis")

pareto_df = customer_df.sort_values(
    by="Profit",
    ascending=False
)

pareto_df["Cum_Profit"] = (
    pareto_df["Profit"]
    .cumsum()
)

pareto_df["Cum_Percent"] = (
    pareto_df["Cum_Profit"]
    /
    pareto_df["Profit"].sum()
) * 100

fig = px.line(
    pareto_df,
    y="Cum_Percent",
    title="Pareto Curve"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# Customer Segment Contribution
# ==========================================

st.subheader("Customer Segment Contribution")

segment_df = (
    filtered_df.groupby(
        "Customer Segment"
    )
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum")
    )
    .reset_index()
)

fig = px.pie(
    segment_df,
    names="Customer Segment",
    values="Profit",
    title="Profit Contribution by Segment"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# Data Table
# ==========================================

st.subheader("Customer Summary Table")

st.dataframe(
    customer_df.sort_values(
        "Profit",
        ascending=False
    ),
    use_container_width=True
)

# ==========================================
# Insights
# ==========================================

st.subheader("Business Insights")

best_customer = top_customers.iloc[0][
    "Customer_Full_Name"
]

st.success(
    f"""
### Key Findings

✅ Total Customers Analyzed: {total_customers}

✅ Most Profitable Customer:
{best_customer}

✅ {loss_customers} customers are currently loss-making.

### Recommendations

• Retain high-value customers

• Review loss-making customer accounts

• Create loyalty programs for profitable customers

• Use customer profitability in pricing decisions
"""
)