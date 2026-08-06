import streamlit as st
import plotly.express as px
import pandas as pd


from utils import load_data


st.title("👥 Customer Analytics")


df = load_data()



# ==========================
# CUSTOMER KPIs
# ==========================

st.subheader("Customer KPIs")


total_customers = df['CustomerID'].nunique()


avg_customer_spend = (
    df.groupby('CustomerID')['Revenue']
    .sum()
    .mean()
)


avg_orders_customer = (
    df.groupby('CustomerID')['OrderID']
    .count()
    .mean()
)



col1,col2,col3 = st.columns(3)


col1.metric(
    "Total Customers",
    total_customers
)


col2.metric(
    "Average Customer Spend",
    f"₹ {avg_customer_spend:,.0f}"
)


col3.metric(
    "Avg Orders / Customer",
    f"{avg_orders_customer:.2f}"
)



# ==========================
# CUSTOMER SEGMENTATION
# ==========================


st.subheader("Customer Segmentation")


customer_value = (
    df.groupby('CustomerID')
    .agg(
        Total_Revenue=('Revenue','sum'),
        Total_Orders=('OrderID','count'),
        Total_Profit=('Profit','sum')
    )
    .reset_index()
)



# Create segments

customer_value['Customer_Segment'] = pd.qcut(
    customer_value['Total_Revenue'],
    q=4,
    labels=[
        "Low Value",
        "Regular",
        "Loyal",
        "Premium"
    ]
)



segment_summary = (
    customer_value
    .groupby('Customer_Segment',
             observed=True)
    .agg(
        Customers=('CustomerID','count'),
        Revenue=('Total_Revenue','sum'),
        Profit=('Total_Profit','sum')
    )
    .reset_index()
)



col1,col2 = st.columns(2)



with col1:

    fig1 = px.pie(
        segment_summary,
        names="Customer_Segment",
        values="Customers",
        title="Customer Segment Distribution"
    )

    st.plotly_chart(
    fig1,
    width="stretch"
)



with col2:

    fig2 = px.bar(
        segment_summary,
        x="Customer_Segment",
        y="Revenue",
        title="Revenue Contribution by Segment"
    )

    st.plotly_chart(
    fig2,
    width="stretch"
)



# ==========================
# TOP CUSTOMERS
# ==========================


st.subheader("🏆 Top 10 Customers")


top_customers = (
    customer_value
    .sort_values(
        "Total_Revenue",
        ascending=False
    )
    .head(10)
)



fig3 = px.bar(
    top_customers,
    x="CustomerID",
    y="Total_Revenue",
    title="Top Customers by Revenue"
)


st.plotly_chart(
    fig3,
    width="stretch"
)



st.dataframe(
    top_customers,
    use_container_width=True
)



# ==========================
# CUSTOMER DEMOGRAPHICS
# ==========================


st.subheader("Customer Demographics")

col1,col2 = st.columns(2)


with col1:

    gender = (
        df['Customer Gender']
        .value_counts()
        .reset_index()
    )

    gender.columns=[
        "Gender",
        "Count"
    ]


    fig4 = px.pie(
        gender,
        names="Gender",
        values="Count",
        title="Gender Distribution"
    )


    st.plotly_chart(
    fig4,
    width="stretch"
)



with col2:

    fig5 = px.histogram(
        df,
        x="Customer Age",
        nbins=10,
        title="Customer Age Distribution"
    )


    st.plotly_chart(
    fig5,
    width="stretch"
)



# ==========================
# INSIGHTS
# ==========================


st.subheader("💡 Customer Insights")


premium = segment_summary.loc[
    segment_summary['Customer_Segment']=="Premium"
]


premium_revenue = (
    premium['Revenue'].values[0]
)


st.write(
f"""
### Findings:

• Total customers analyzed:
**{total_customers}**

• Premium customers generated:
**₹ {premium_revenue:,.0f} revenue**

• Average customer spending:
**₹ {avg_customer_spend:,.0f}**

• Highest value customers can be targeted
for loyalty programs and retention campaigns.
"""
)