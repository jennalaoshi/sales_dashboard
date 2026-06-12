import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sales Dashboard",
    layout="wide"
)

st.title("Sales Dashboard")
st.write("Use this dashboard to analyze sales by region, product, and date.")

@st.cache_data
def load_data():
    df = pd.read_csv("sales_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    return df

df = load_data()

st.sidebar.header("Filters")

selected_regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=sorted(df["region"].unique()),
    default=sorted(df["region"].unique())
)

selected_products = st.sidebar.multiselect(
    "Select Product(s)",
    options=sorted(df["product"].unique()),
    default=sorted(df["product"].unique())
)

start_date, end_date = st.sidebar.date_input(
    "Select Date Range",
    value=[df["date"].min().date(), df["date"].max().date()]
)

filtered_df = df[
    (df["region"].isin(selected_regions)) &
    (df["product"].isin(selected_products)) &
    (df["date"] >= pd.to_datetime(start_date)) &
    (df["date"] <= pd.to_datetime(end_date))
]

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# KPI metrics
total_sales = filtered_df["sales"].sum()
total_quantity = filtered_df["quantity"].sum()
avg_sales = filtered_df["sales"].mean()
unique_products = filtered_df["product"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Quantity", f"{total_quantity}")
col3.metric("Average Sales", f"${avg_sales:,.0f}")
col4.metric("Unique Products", f"{unique_products}")

# Summary tables for charts
sales_by_product = (
    filtered_df.groupby("product", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
)

sales_by_region = (
    filtered_df.groupby("region", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
)

sales_by_date = (
    filtered_df.groupby("date", as_index=False)["sales"]
    .sum()
)

top_products = sales_by_product.head(3)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Trend",
    "Top Products",
    "Data"
])

with tab1:
    st.subheader("Sales by Product")
    st.bar_chart(sales_by_product, x="product", y="sales")

    st.subheader("Sales by Region")
    st.bar_chart(sales_by_region, x="region", y="sales")

with tab2:
    st.subheader("Sales Trend Over Time")
    st.line_chart(sales_by_date, x="date", y="sales")

with tab3:
    st.subheader("Top 3 Products by Sales")
    st.dataframe(top_products, use_container_width=True)

with tab4:
    st.subheader("Filtered Dataset")
    st.dataframe(filtered_df, use_container_width=True)