import os
import pandas as pd
import streamlit as st


def load_data():

    BASE_DIR = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )

    DATA_PATH = os.path.join(
        BASE_DIR,
        "data",
        "ecommerce_sales_50k_15cols.csv"
    )


    df = pd.read_csv(DATA_PATH)


    df['Date'] = pd.to_datetime(df['Date'])


    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter
    df['Day_Name'] = df['Date'].dt.day_name()


    df['Profit_Margin'] = (
        df['Profit'] /
        df['Revenue']
    ) * 100


    return df



def apply_filters(df):

    st.sidebar.header("🔍 Dashboard Filters")


    years = st.sidebar.multiselect(
        "Select Year",
        df['Year'].unique(),
        default=df['Year'].unique()
    )


    regions = st.sidebar.multiselect(
        "Select Region",
        df['Region'].unique(),
        default=df['Region'].unique()
    )


    categories = st.sidebar.multiselect(
        "Select Category",
        df['Category'].unique(),
        default=df['Category'].unique()
    )


    filtered_df = df[
        (df['Year'].isin(years)) &
        (df['Region'].isin(regions)) &
        (df['Category'].isin(categories))
    ]


    return filtered_df