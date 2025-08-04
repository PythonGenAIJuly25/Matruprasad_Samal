import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Data 
orders_df = pd.read_csv("E:\My_Notebook\Revature project\data\clean_orders.csv", parse_dates=["Order Date", "Ship Date"])
inventory_df = pd.read_csv("E:\My_Notebook\Revature project\data\simulated_inventory.csv", parse_dates=["date"])
products_df = pd.read_csv("E:\My_Notebook\Revature project\data\products.csv")

# --- Page Setup ---
st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")
st.title("SUPPLY CHAIN DASHBOARD")

# FILTERS 
st.sidebar.header(" FILTERS PANEL ")

# Orders Filters Section
st.sidebar.header("🔷 Order Filters")

# Date Range
min_date = orders_df["Order Date"].min()
max_date = orders_df["Order Date"].max()
selected_date = st.sidebar.date_input("Select Order Date Range", [min_date, max_date])

#  Segment
segments = orders_df["Segment"].dropna().unique().tolist()
selected_segments = st.sidebar.multiselect("Segment", segments, default=segments)

# Ship Mode
ship_modes = orders_df["Ship Mode"].dropna().unique().tolist()
selected_modes = st.sidebar.multiselect("Ship Mode", ship_modes, default=ship_modes)

#  Sub-Category
sub_categories = orders_df["Sub-Category"].dropna().unique().tolist()
selected_subcats = st.sidebar.multiselect("Sub-Category", sub_categories, default=sub_categories)

# Order Priority
priorities = orders_df["Order Priority"].dropna().unique().tolist()
selected_priorities = st.sidebar.multiselect("Order Priority", priorities, default=priorities)

# Market
markets = orders_df["Market"].dropna().unique().tolist()
selected_markets = st.sidebar.multiselect("Market", markets, default=markets)

# Category from orders_df
order_categories = orders_df["Category"].dropna().unique().tolist()
selected_order_categories = st.sidebar.multiselect("Order Category", order_categories, default=order_categories)

st.sidebar.markdown("---")


# Inventory Filters Section
st.sidebar.header("🔶 Inventory Filters")


#  Category
categories = inventory_df["category"].dropna().unique().tolist()
selected_categories = st.sidebar.multiselect("Inventory Category", categories, default=categories)




# APPLY FILTERS 
filtered_orders = orders_df[
    (orders_df["Order Date"] >= pd.to_datetime(selected_date[0])) &
    (orders_df["Order Date"] <= pd.to_datetime(selected_date[1])) &
    (orders_df["Segment"].isin(selected_segments)) &
    (orders_df["Ship Mode"].isin(selected_modes)) &
    (orders_df["Sub-Category"].isin(selected_subcats)) &
    (orders_df["Order Priority"].isin(selected_priorities)) &
    (orders_df["Market"].isin(selected_markets)) &
    (orders_df["Category"].isin(selected_order_categories))
]






filtered_inventory = inventory_df[inventory_df["category"].isin(selected_categories)]

# --- KPIs ---
st.subheader(" Key Performance Indicators ")
col1, col2, col3, col4, col5 = st.columns(5)

total_sales = filtered_orders["Sales"].sum()
aov = total_sales / len(filtered_orders) if len(filtered_orders) > 0 else 0
fill_rate = filtered_orders[~filtered_orders['Returned']].shape[0] / len(filtered_orders) if len(filtered_orders) > 0 else 0
on_time_delivery = filtered_orders['On-time Delivery'].mean() if not filtered_orders.empty else 0
return_rate = filtered_orders['Returned'].mean() if not filtered_orders.empty else 0

col1.metric(" Total Sales", f"${total_sales:,.2f}")
col2.metric(" Avg Order Value", f"${aov:,.2f}")
col3.metric(" Fill Rate", f"{fill_rate:.2%}")
col4.metric("On-Time Delivery", f"{on_time_delivery:.2%}")
col5.metric("Return Rate", f"{return_rate:.2%}")

st.markdown("---")

# --- Inventory Trend ---
st.subheader(" Inventory Trend (Last 30 Days)")

inventory_trend = filtered_inventory.groupby(['date', 'product_name'])['inventory_level'].mean().reset_index()
selected_products = st.multiselect(
    "Select products to compare:",
    inventory_trend['product_name'].unique(),
    default=inventory_trend['product_name'].unique()[:3]
)

filtered_inventory_plot = inventory_trend[inventory_trend['product_name'].isin(selected_products)]
if not filtered_inventory_plot.empty:
    inventory_pivot = filtered_inventory_plot.pivot(index='date', columns='product_name', values='inventory_level')
    st.line_chart(inventory_pivot)
else:
    st.info("No inventory data for the selected filters.")

st.markdown("---")

# --- Ship Mode Distribution ---
st.subheader("Ship Mode Distribution")

if not filtered_orders.empty:
    ship_mode_counts = filtered_orders['Ship Mode'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(ship_mode_counts, labels=ship_mode_counts.index, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    st.pyplot(fig1)
else:
    st.info("No data available for Ship Mode distribution.")

st.markdown("---")

# --- Top Returned Products ---
st.subheader(" Top Returned Products")

if not filtered_orders.empty:
    returned_products = filtered_orders[filtered_orders['Returned']]
    top_returns = returned_products['Product Name'].value_counts().head(5)
    st.bar_chart(top_returns)
else:
    st.info("No returned products in this filter.")

st.markdown("---")

# --- Avg Inventory by Category ---
st.subheader(" Average Inventory by Category")

avg_inventory = filtered_inventory.groupby("category")["inventory_level"].mean().sort_values(ascending=False)
if not avg_inventory.empty:
    st.bar_chart(avg_inventory)
else:
    st.info("No inventory data for selected categories.")

st.markdown("---")

# --- Lead Time Histogram ---
st.subheader(" Shipping Lead Time Distribution")

if not filtered_orders.empty:
    fig2, ax2 = plt.subplots()
    filtered_orders['Lead Time (days)'].hist(bins=20, ax=ax2)
    ax2.set_xlabel("Lead Time (days)")
    ax2.set_ylabel("Number of Orders")
    ax2.set_title("Shipping Lead Time Distribution")
    st.pyplot(fig2)
else:
    st.info("No order data available for lead time distribution.")

# --- Footer ---
st.markdown("---")

