#  Supply Chain Data Integration System

A full-stack data integration and analytics project that combines sales, customer, and inventory data into a centralized warehouse using **BigQuery star schema** and delivers visual insights through a **Streamlit dashboard**.

---

##  Project Overview

This project demonstrates how to:
- Clean and transform raw supply chain data from CSV and API
- Design and load a star schema into BigQuery (in Jupyter Notebook)
- Build a real-time dashboard for KPIs, inventory trends, and performance

        
##  Tools & Technologies

| Layer              | Tech Stack                         |
|--------------------|------------------------------------|
| Language           | Python, Pandas, NumPy              |
| Cloud Warehouse    | Google BigQuery                    |
| Visualization      | Streamlit, Matplotlib              |
| Notebook Platform  | Jupyter Notebook                   |
| API Source         | [FakeStoreAPI](https://fakestoreapi.com/) |

---

##  Star Schema Design

###  Fact Tables:
- `fact_orders`: order_id, order_date, sales, profit, return_flag, etc.
- `fact_inventory`: product_id, date, inventory_level, stockouts, restock

###  Dimension Tables:
- `dim_product`: product_id, name, category, price
- `dim_customer`: customer_id, segment, region, market
- `dim_time`: date, year, month, weekday, etc.
- `dim_location`: region, market, shipping_mode (optional split)



---

##  ETL Flow

1. **Load** CSVs + API data (`train.csv`, Fake Store)
2. **Clean + enrich** orders, simulate inventory
3. **Build star schema** in Pandas
4. **Upload to BigQuery** using `google-cloud-bigquery`
5. **Query + visualize** using Streamlit filters

---

##  Dashboard Features

- KPIs: Total Sales, Avg Order Value, On-time Delivery
- Filter Panel: Segment, Sub-Category, Region, Ship Mode, Date Range
- Inventory trends by product
- Pie chart of shipping modes
- Lead time distribution
- Top returned products

Run the dashboard:

```bash
cd dashboard
streamlit run app.py

