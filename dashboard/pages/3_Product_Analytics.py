import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_data


st.title("📦 Product Analytics")


df = load_data()



# ==========================
# PRODUCT KPIs
# ==========================

st.subheader("Product Performance KPIs")


total_products = df['Product'].nunique()


best_product = (
    df.groupby('Product')['Revenue']
    .sum()
    .idxmax()
)


highest_revenue = (
    df.groupby('Product')['Revenue']
    .sum()
    .max()
)


total_units = df['Units Sold'].sum()



col1,col2,col3,col4 = st.columns(4)


col1.metric(
    "Total Products",
    total_products
)


col2.metric(
    "Units Sold",
    f"{total_units:,}"
)


col3.metric(
    "Top Product",
    best_product
)


col4.metric(
    "Highest Product Revenue",
    f"₹ {highest_revenue:,.0f}"
)



# ==========================
# CATEGORY PERFORMANCE
# ==========================

st.subheader("Category Performance")


category_analysis = (
    df.groupby('Category')
    .agg(
        Revenue=('Revenue','sum'),
        Profit=('Profit','sum'),
        Units_Sold=('Units Sold','sum'),
        Orders=('OrderID','count')
    )
    .reset_index()
    .sort_values(
        'Revenue',
        ascending=False
    )
)



col1,col2 = st.columns(2)


with col1:

    fig1 = px.bar(
        category_analysis,
        x="Category",
        y="Revenue",
        title="Revenue by Category"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )



with col2:

    fig2 = px.bar(
        category_analysis,
        x="Category",
        y="Profit",
        title="Profit by Category"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )



# ==========================
# TOP PRODUCTS
# ==========================

st.subheader("🏆 Top Products")


product_analysis = (
    df.groupby('Product')
    .agg(
        Revenue=('Revenue','sum'),
        Profit=('Profit','sum'),
        Units_Sold=('Units Sold','sum'),
        Orders=('OrderID','count')
    )
    .reset_index()
)



top_products = (
    product_analysis
    .sort_values(
        'Revenue',
        ascending=False
    )
    .head(10)
)



fig3 = px.bar(
    top_products,
    x="Product",
    y="Revenue",
    title="Top 10 Products by Revenue"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)



# ==========================
# PROFITABILITY ANALYSIS
# ==========================

st.subheader("Revenue vs Profit Analysis")


fig4 = px.scatter(
    product_analysis,
    x="Revenue",
    y="Profit",
    size="Units_Sold",
    hover_name="Product",
    title="Product Profitability Analysis"
)


st.plotly_chart(
    fig4,
    use_container_width=True
)



# ==========================
# DETAILED TABLE
# ==========================

st.subheader("Detailed Product Report")


product_report = (
    product_analysis
    .sort_values(
        "Revenue",
        ascending=False
    )
)


st.dataframe(
    product_report,
    use_container_width=True
)



# ==========================
# INSIGHTS
# ==========================

st.subheader("💡 Product Insights")


best_category = category_analysis.iloc[0]


st.write(
f"""
### Findings:

• Best performing product:
**{best_product}**

• Highest product revenue:
**₹ {highest_revenue:,.0f}**

• Best performing category:
**{best_category['Category']}**

• Category revenue:
**₹ {best_category['Revenue']:,.0f}**

• Products with high revenue but low profit
should be reviewed for pricing and discount strategy.
"""
)