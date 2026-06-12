import streamlit as st
import pandas as pd

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("Sales Dashboard")

df = pd.read_csv("sales_data.csv")

st.sidebar.header("Filters")

selected_regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=df["region"].unique(),
    default=df["region"].unique()
)

selected_products = st.sidebar.multiselect(
    "Select Product(s)",
    options=df["product"].unique(),
    default=df["product"].unique()
)

filtered_df = df[
    (df["region"].isin(selected_regions)) &
    (df["product"].isin(selected_products))
]

total_sales = filtered_df["sales"].sum()
total_quantity = filtered_df["quantity"].sum()
avg_sales = filtered_df["sales"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Quantity", f"{total_quantity}")
col3.metric("Average Sales", f"${avg_sales:,.0f}")

st.subheader("Filtered Data")
st.dataframe(filtered_df)