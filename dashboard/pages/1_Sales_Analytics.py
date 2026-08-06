import streamlit as st
import plotly.express as px

from utils import load_data


st.title("📈 Sales Analytics")


df = load_data()



# ==========================
# KPI SECTION
# ==========================

st.subheader("Business KPIs")


total_revenue = df['Revenue'].sum()
total_profit = df['Profit'].sum()
total_orders = df['OrderID'].nunique()
avg_order = df['Revenue'].mean()

profit_margin = (
    total_profit / total_revenue
) * 100


col1,col2,col3,col4,col5 = st.columns(5)


col1.metric(
    "Revenue",
    f"₹ {total_revenue:,.0f}"
)


col2.metric(
    "Profit",
    f"₹ {total_profit:,.0f}"
)


col3.metric(
    "Orders",
    total_orders
)


col4.metric(
    "Average Order Value",
    f"₹ {avg_order:,.0f}"
)


col5.metric(
    "Profit Margin",
    f"{profit_margin:.2f}%"
)



# ==========================
# MONTHLY ANALYSIS
# ==========================


st.subheader("Monthly Sales Performance")


monthly_sales = (
    df.groupby('Month')
    .agg(
        Revenue=('Revenue','sum'),
        Profit=('Profit','sum'),
        Orders=('OrderID','count')
    )
    .reset_index()
)



fig = px.line(
    monthly_sales,
    x="Month",
    y=["Revenue","Profit"],
    markers=True,
    title="Monthly Revenue & Profit Trend"
)


st.plotly_chart(
    fig,
    width="stretch"
)



# ==========================
# DATA TABLE
# ==========================


st.subheader("Detailed Monthly Report")


st.dataframe(
    monthly_sales,
    use_container_width=True
)



# ==========================
# INSIGHTS
# ==========================


st.subheader("💡 Business Insights")


best_month = monthly_sales.loc[
    monthly_sales['Revenue'].idxmax()
]


best_profit_month = monthly_sales.loc[
    monthly_sales['Profit'].idxmax()
]


st.write(
f"""
### Key Findings:

• Highest revenue generated in **Month {best_month['Month']}**

• Revenue achieved:
**₹ {best_month['Revenue']:,.0f}**

• Highest profit generated in **Month {best_profit_month['Month']}**

• Profit achieved:
**₹ {best_profit_month['Profit']:,.0f}**

• Average order value:
**₹ {avg_order:,.0f}**
"""
)