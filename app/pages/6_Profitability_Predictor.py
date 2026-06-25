import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Profitability Predictor",
    page_icon="🤖",
    layout="wide"
)

# ==========================================
# PATHS
# ==========================================

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../.."
    )
)

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "data",
    "processed",
    "cleaned_data.csv"
)

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "profitability_classifier.pkl"
)

ENCODER_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "label_encoders.pkl"
)

# ==========================================
# LOAD FILES
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

@st.cache_resource
def load_encoders():
    return joblib.load(ENCODER_PATH)

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

model = load_model()
encoders = load_encoders()
df = load_data()

# ==========================================
# TITLE
# ==========================================

st.title("🤖 Profitability Prediction Engine")

st.markdown("""
Predict whether an order will be profitable
before execution.
""")

st.divider()

# ==========================================
# USER INPUTS
# ==========================================

col1, col2 = st.columns(2)

with col1:

    sales = st.number_input(
        "Sales",
        min_value=0.0,
        value=500.0
    )

    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=2
    )

    discount_amount = st.number_input(
        "Discount Amount",
        min_value=0.0,
        value=10.0
    )

    discount_rate = st.slider(
        "Discount Rate",
        0.0,
        1.0,
        0.10
    )

    product_price = st.number_input(
        "Product Price",
        min_value=1.0,
        value=250.0
    )

with col2:

    real_shipping = st.number_input(
        "Actual Shipping Days",
        min_value=1,
        value=4
    )

    scheduled_shipping = st.number_input(
        "Scheduled Shipping Days",
        min_value=1,
        value=3
    )

    late_delivery = st.selectbox(
        "Late Delivery Risk",
        [0, 1]
    )

    customer_segment = st.selectbox(
        "Customer Segment",
        sorted(df["Customer Segment"].unique())
    )

    market = st.selectbox(
        "Market",
        sorted(df["Market"].unique())
    )

    shipping_mode = st.selectbox(
        "Shipping Mode",
        sorted(df["Shipping Mode"].unique())
    )

    category = st.selectbox(
        "Category",
        sorted(df["Category Name"].unique())
    )

# ==========================================
# FEATURE ENGINEERING
# ==========================================

shipping_delay = (
    real_shipping -
    scheduled_shipping
)

# ==========================================
# PREDICT BUTTON
# ==========================================

if st.button("Predict Profitability"):

    try:

        encoded_segment = encoders[
            "Customer Segment"
        ].transform(
            [customer_segment]
        )[0]

        encoded_market = encoders[
            "Market"
        ].transform(
            [market]
        )[0]

        encoded_shipping = encoders[
            "Shipping Mode"
        ].transform(
            [shipping_mode]
        )[0]

        encoded_category = encoders[
            "Category Name"
        ].transform(
            [category]
        )[0]

        input_df = pd.DataFrame({

            "Sales":[sales],

            "Order Item Quantity":[quantity],

            "Order Item Discount":[discount_amount],

            "Order Item Discount Rate":[discount_rate],

            "Product Price":[product_price],

            "Days for shipping (real)":[real_shipping],

            "Days for shipment (scheduled)":[scheduled_shipping],

            "Shipping_Delay":[shipping_delay],

            "Late_delivery_risk":[late_delivery],

            "Customer Segment":[encoded_segment],

            "Market":[encoded_market],

            "Shipping Mode":[encoded_shipping],

            "Category Name":[encoded_category]
        })

        prediction = model.predict(
            input_df
        )[0]

        probability = model.predict_proba(
            input_df
        )[0]

        st.divider()

        st.subheader("Prediction Result")

        if prediction == 1:

            st.success(
                f"""
                ✅ PROFITABLE ORDER

                Probability:
                {probability[1]*100:.2f}%
                """
            )

        else:

            st.error(
                f"""
                ❌ LOSS MAKING ORDER

                Probability:
                {probability[0]*100:.2f}%
                """
            )

        st.subheader(
            "Business Recommendation"
        )

        if discount_rate > 0.20:

            st.warning(
                "High discount detected. Review pricing."
            )

        if shipping_delay > 2:

            st.warning(
                "Shipping delay risk is high."
            )

        if prediction == 1:

            st.info(
                "Order is expected to generate profit."
            )

        else:

            st.info(
                "Review pricing and discount strategy."
            )

    except Exception as e:

        st.error(
            f"Prediction Error: {e}"
        )