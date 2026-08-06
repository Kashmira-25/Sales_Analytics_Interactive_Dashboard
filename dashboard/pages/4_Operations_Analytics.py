import streamlit as st
import plotly.express as px
import pandas as pd

from utils import load_data


st.title("⚙️ Operations Analytics")


df = load_data()



# ==========================
# OPERATION KPIs
# ==========================

st.subheader("Operational KPIs")


total_orders = df['OrderID'].nunique()


delivered_orders = (
    df[df['Order Status']=="Delivered"]
    ['OrderID']
    .nunique()
)


returned_orders = (
    df[df['Order Status']=="Returned"]
    ['OrderID']
    .nunique()
)


cancelled_orders = (
    df[df['Order Status']=="Cancelled"]
    ['OrderID']
    .nunique()
)


delivery_rate = (
    delivered_orders / total_orders
) * 100


return_rate = (
    returned_orders / total_orders
) * 100


cancel_rate = (
    cancelled_orders / total_orders
) * 100



col1,col2,col3,col4 = st.columns(4)


col1.metric(
    "Total Orders",
    total_orders
)


col2.metric(
    "Delivery Rate",
    f"{delivery_rate:.2f}%"
)


col3.metric(
    "Return Rate",
    f"{return_rate:.2f}%"
)


col4.metric(
    "Cancellation Rate",
    f"{cancel_rate:.2f}%"
)



# ==========================
# ORDER STATUS ANALYSIS
# ==========================

st.subheader("Order Status Analysis")


status_analysis = (
    df.groupby('Order Status')
    .agg(
        Orders=('OrderID','count'),
        Revenue=('Revenue','sum'),
        Profit=('Profit','sum')
    )
    .reset_index()
)



col1,col2 = st.columns(2)


with col1:

    fig1 = px.pie(
        status_analysis,
        names="Order Status",
        values="Orders",
        title="Order Status Distribution"
    )


    st.plotly_chart(
        fig1,
        use_container_width=True
    )


with col2:

    fig2 = px.bar(
        status_analysis,
        x="Order Status",
        y="Revenue",
        title="Revenue by Order Status"
    )


    st.plotly_chart(
        fig2,
        use_container_width=True
    )



# ==========================
# PAYMENT ANALYSIS
# ==========================

st.subheader("Payment Method Analysis")


payment_analysis = (
    df.groupby('Payment Method')
    .agg(
        Orders=('OrderID','count'),
        Revenue=('Revenue','sum')
    )
    .reset_index()
    .sort_values(
        "Revenue",
        ascending=False
    )
)



fig3 = px.bar(
    payment_analysis,
    x="Payment Method",
    y="Revenue",
    title="Revenue by Payment Method"
)


st.plotly_chart(
    fig3,
    use_container_width=True
)


st.dataframe(
    payment_analysis,
    use_container_width=True
)



# ==========================
# SHIPPING ANALYSIS
# ==========================

st.subheader("Shipping Analysis")


shipping_analysis = (
    df.groupby('Shipping Method')
    .agg(
        Orders=('OrderID','count'),
        Avg_Shipping_Cost=('Shipping Cost','mean'),
        Revenue=('Revenue','sum')
    )
    .reset_index()
)



col1,col2 = st.columns(2)


with col1:

    fig4 = px.bar(
        shipping_analysis,
        x="Shipping Method",
        y="Orders",
        title="Orders by Shipping Method"
    )


    st.plotly_chart(
        fig4,
        use_container_width=True
    )


with col2:

    fig5 = px.bar(
        shipping_analysis,
        x="Shipping Method",
        y="Avg_Shipping_Cost",
        title="Average Shipping Cost"
    )


    st.plotly_chart(
        fig5,
        use_container_width=True
    )



# ==========================
# DISCOUNT IMPACT
# ==========================

st.subheader("Discount Impact Analysis")


discount_analysis = (
    df.groupby('Discount (%)')
    .agg(
        Revenue=('Revenue','sum'),
        Profit=('Profit','sum'),
        Orders=('OrderID','count')
    )
    .reset_index()
)



fig6 = px.line(
    discount_analysis,
    x="Discount (%)",
    y="Revenue",
    markers=True,
    title="Discount vs Revenue"
)


st.plotly_chart(
    fig6,
    use_container_width=True
)



# ==========================
# DETAILED TABLE
# ==========================

st.subheader("Operational Report")


st.dataframe(
    status_analysis,
    use_container_width=True
)



# ==========================
# INSIGHTS
# ==========================

st.subheader("💡 Operational Insights")


best_payment = payment_analysis.iloc[0]

best_shipping = (
    shipping_analysis
    .sort_values(
        'Orders',
        ascending=False
    )
    .iloc[0]
)



st.write(
f"""
### Findings:

• Delivery success rate:
**{delivery_rate:.2f}%**

• Return rate:
**{return_rate:.2f}%**

• Most preferred payment method:
**{best_payment['Payment Method']}**

• Highest order shipping method:
**{best_shipping['Shipping Method']}**

• Operational improvements can focus on reducing
returns and cancellations.
"""
)