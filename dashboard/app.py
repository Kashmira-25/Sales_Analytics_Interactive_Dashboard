import streamlit as st
import plotly.express as px

from utils import load_data, apply_filters


# ------------------
# Page Configuration
# ------------------

st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# ------------------
# Load Data
# ------------------

@st.cache_data
def get_data():
    return load_data()


df = get_data()


# Apply global filters
filtered_df = apply_filters(df)



# ------------------
# Title
# ------------------

st.title(
    "📊 E-Commerce Sales Analytics Dashboard"
)


st.caption(
    "50K+ transaction analysis using Python, Pandas, Plotly & Streamlit"
)



# ------------------
# KPI Section
# ------------------

revenue = filtered_df['Revenue'].sum()

profit = filtered_df['Profit'].sum()

orders = filtered_df['OrderID'].nunique()

customers = filtered_df['CustomerID'].nunique()

margin = (
    profit / revenue
) * 100



c1,c2,c3,c4,c5 = st.columns(5)


c1.metric(
    "Total Revenue",
    f"₹ {revenue:,.0f}"
)


c2.metric(
    "Total Profit",
    f"₹ {profit:,.0f}"
)


c3.metric(
    "Total Orders",
    orders
)


c4.metric(
    "Customers",
    customers
)


c5.metric(
    "Profit Margin",
    f"{margin:.2f}%"
)



# ------------------
# Revenue Trend
# ------------------

st.subheader("📈 Monthly Revenue Trend")


monthly = (
    filtered_df
    .groupby('Month')
    ['Revenue']
    .sum()
    .reset_index()
)



fig1 = px.line(
    monthly,
    x="Month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue"
)


st.plotly_chart(
    fig1,
    use_container_width=True
)



# ------------------
# Category & Region Analysis
# ------------------

col1,col2 = st.columns(2)



with col1:

    category_sales = (
        filtered_df
        .groupby('Category')
        ['Revenue']
        .sum()
        .reset_index()
    )


    fig2 = px.bar(
        category_sales,
        x="Category",
        y="Revenue",
        title="Revenue by Category"
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )



with col2:

    region_sales = (
        filtered_df
        .groupby('Region')
        ['Revenue']
        .sum()
        .reset_index()
    )


    fig3 = px.pie(
        region_sales,
        names="Region",
        values="Revenue",
        title="Revenue Contribution by Region"
    )


    st.plotly_chart(
        fig3,
        use_container_width=True
    )



# ------------------
# Data Preview
# ------------------

st.subheader("📋 Filtered Data Preview")


st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)



# ------------------
# Download
# ------------------

csv = filtered_df.to_csv(
    index=False
)


st.download_button(
    label="⬇️ Download Filtered Dataset",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)