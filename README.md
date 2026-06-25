# 🚚 Customer, Product & Profitability Performance Analysis in Supply Chain Operations

## 📌 Overview

This project analyzes customer, product, discount, and market profitability for a global logistics company (APL Logistics). The objective is to identify high-value customers, profitable products, margin erosion caused by discounts, and market-level performance while enabling profitability prediction using Machine Learning.

The project combines Data Analytics, Business Intelligence, Machine Learning, and an Interactive Streamlit Dashboard to support profit-driven decision making.

---

## 🎯 Business Problem

Organizations often focus on revenue growth without understanding actual profitability.

Key challenges include:

- High revenue customers generating low profits
- Excessive discounting reducing margins
- Loss-making products and categories
- Regional profitability differences
- Lack of visibility into customer value contribution

This project helps answer:

- Which customers generate the highest profits?
- Which products and categories drive profitability?
- How do discounts impact margins?
- Which markets are truly profitable?
- Can profitability be predicted before order execution?

---

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Plotly
- Scikit-Learn
- Streamlit
- Joblib

---

## 📂 Project Structure

APL_Logistics_Profitability_Analytics/

├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning_feature_engineering.ipynb
│   ├── 03_eda_profitability_analysis.ipynb
│   ├── 04_ml_profitability_prediction.ipynb
│   └── 05_business_recommendations.ipynb
│
├── models/
│   ├── profitability_classifier.pkl
│   └── label_encoders.pkl
│
├── app/
│   ├── app.py
│   └── pages/
│       ├── 1_Executive_Dashboard.py
│       ├── 2_Customer_Analytics.py
│       ├── 3_Product_Analytics.py
│       ├── 4_Discount_Impact.py
│       ├── 5_Market_Analysis.py
│       └── 6_Profitability_Predictor.py
│
├── requirements.txt
└── README.md

---

## 📊 Key Analysis Performed

### Revenue & Profit Analysis
- Total Revenue
- Total Profit
- Profit Margin
- Revenue vs Profit Comparison

### Customer Analysis
- Top Customers by Profit
- Bottom Customers by Profit
- Customer Segment Contribution
- Pareto Analysis (80/20 Rule)

### Product Analysis
- Product Profitability
- Category Margin Analysis
- Top & Bottom Products
- Revenue vs Profit Analysis

### Discount Analysis
- Discount Impact on Profit
- Margin Erosion Analysis
- Discount Threshold Detection
- What-if Discount Scenarios

### Market Analysis
- Market Profitability
- Regional Performance
- Country-Level Analysis
- Geographic Profit Distribution

---

## 🤖 Machine Learning Model

### Objective

Predict whether an order will be profitable before execution.

### Target Variable

- 1 = Profitable Order
- 0 = Loss-Making Order

### Features Used

- Sales
- Product Price
- Quantity
- Discount Amount
- Discount Rate
- Shipping Delay
- Customer Segment
- Market
- Shipping Mode
- Category

### Algorithms Evaluated

- Logistic Regression
- Random Forest Classifier

### Selected Model

✅ Random Forest Classifier

---

## 📈 Streamlit Dashboard Modules

### 1. Executive Dashboard
- Revenue KPIs
- Profit KPIs
- Margin Analysis
- Market Overview

### 2. Customer Analytics
- Top Customers
- Loss-Making Customers
- Customer Contribution
- Pareto Analysis

### 3. Product Analytics
- Product Profitability
- Category Analysis
- Margin Comparison

### 4. Discount Impact Analyzer
- Discount vs Profit
- Discount vs Margin
- What-if Scenarios

### 5. Market Analysis
- Market Profitability
- Regional Insights
- Country Performance
- Geographic Analysis

### 6. Profitability Predictor
- Real-Time Prediction
- Profitability Probability
- Business Recommendations

---

## 💡 Key Business Insights

- A small percentage of customers contribute the majority of profits.
- High revenue does not always translate into high profitability.
- Excessive discounting significantly reduces margins.
- Certain products generate revenue but remain low-margin.
- Market profitability varies substantially across regions.
- Predictive analytics can support better pricing decisions.

---

## 📌 Business Recommendations

### Customer Strategy
- Focus on retaining high-profit customers.
- Review and optimize low-margin customer accounts.

### Pricing Strategy
- Introduce discount approval limits.
- Monitor excessive discounting.

### Product Strategy
- Promote high-margin products.
- Re-price loss-making products.

### Market Strategy
- Expand profitable regions.
- Review underperforming markets.

### Predictive Analytics
- Use profitability predictions before approving large orders.
- Support pricing and discount decisions using ML insights.

---

## 🚀 Run Locally

### Install Dependencies

```bash
pip install -r requirements.txt# APL_Logistics_Profitability_Analytics
# APL_Logistics_Profitability_Analytics

## Dataset

Dataset is excluded from GitHub due to file size limitations.

To run the dashboard:

1. Launch Streamlit app
2. Upload cleaned_data.csv using the sidebar
3. Explore analytics dashboards
