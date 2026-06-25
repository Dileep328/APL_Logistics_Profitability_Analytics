import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Product Analytics",
    page_icon="📦",
    layout="wide"
)

# ==========================================
# LOAD DATA
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
# TITLE
# ==========================================

st.title("📦 Product Analytics Dashboard")

st.markdown("""
Analyze product and category profitability,
margin performance and loss-making products.
""")

# ==========================================
# SIDEBAR FILTERS
# ==========================================

st.sidebar.header("Filters")

selected_category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category Name"].unique()),
    default=sorted(df["Category Name"].unique())
)

filtered_df = df[
    df["Category Name"].isin(
        selected_category
    )
]

# ==========================================
# CATEGORY ANALYSIS
# ==========================================

category_df = (
    filtered_df.groupby(
        "Category Name"
    )
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum")
    )
    .reset_index()
)

category_df["Margin"] = (
    category_df["Profit"]
    /
    category_df["Revenue"]
) * 100

# ==========================================
# KPIs
# ==========================================

total_categories = (
    category_df.shape[0]
)

best_category = (
    category_df.loc[
        category_df["Profit"].idxmax(),
        "Category Name"
    ]
)

worst_category = (
    category_df.loc[
        category_df["Profit"].idxmin(),
        "Category Name"
    ]
)

avg_margin = (
    category_df["Margin"].mean()
)

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Categories",
        total_categories
    )

with c2:
    st.metric(
        "Best Category",
        best_category
    )

with c3:
    st.metric(
        "Worst Category",
        worst_category
    )

with c4:
    st.metric(
        "Avg Margin",
        f"{avg_margin:.2f}%"
    )

st.divider()

# ==========================================
# CATEGORY PROFITABILITY
# ==========================================

st.subheader(
    "Category Profitability"
)

fig = px.bar(
    category_df.sort_values(
        "Profit",
        ascending=False
    ),
    x="Category Name",
    y="Profit",
    color="Profit",
    text="Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# CATEGORY MARGIN
# ==========================================

st.subheader(
    "Category Margin Analysis"
)

fig = px.bar(
    category_df.sort_values(
        "Margin",
        ascending=False
    ),
    x="Category Name",
    y="Margin",
    color="Margin",
    text="Margin"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# PRODUCT ANALYSIS
# ==========================================

product_df = (
    filtered_df.groupby(
        "Product Name"
    )
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum")
    )
    .reset_index()
)

# ==========================================
# TOP PRODUCTS
# ==========================================

st.subheader(
    "🏆 Top 10 Products by Profit"
)

top_products = (
    product_df
    .sort_values(
        "Profit",
        ascending=False
    )
    .head(10)
)

fig = px.bar(
    top_products,
    x="Profit",
    y="Product Name",
    orientation="h",
    text="Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# LOSS MAKING PRODUCTS
# ==========================================

st.subheader(
    "⚠️ Bottom 10 Products"
)

bottom_products = (
    product_df
    .sort_values(
        "Profit"
    )
    .head(10)
)

fig = px.bar(
    bottom_products,
    x="Profit",
    y="Product Name",
    orientation="h",
    text="Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# REVENUE VS PROFIT
# ==========================================

st.subheader(
    "Revenue vs Profit"
)

sample_products = product_df.sample(
    min(500, len(product_df)),
    random_state=42
)

fig = px.scatter(
    sample_products,
    x="Revenue",
    y="Profit",
    hover_name="Product Name",
    title="Product Revenue vs Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================
# HEATMAP DATA
# ==========================================

st.subheader(
    "Category Performance Table"
)

st.dataframe(
    category_df.sort_values(
        "Profit",
        ascending=False
    ),
    use_container_width=True
)

# ==========================================
# PRODUCT TABLE
# ==========================================

st.subheader(
    "Product Summary Table"
)

st.dataframe(
    product_df.sort_values(
        "Profit",
        ascending=False
    ),
    use_container_width=True
)

# ==========================================
# BUSINESS INSIGHTS
# ==========================================

st.subheader(
    "Business Insights"
)

st.success(
    f"""
### Key Findings

✅ Most Profitable Category:
{best_category}

⚠️ Lowest Performing Category:
{worst_category}

✅ Average Category Margin:
{avg_margin:.2f}%

### Recommendations

• Increase focus on high-margin categories

• Re-price loss-making products

• Reduce excessive discounting

• Optimize inventory allocation

• Promote profitable products
"""
)