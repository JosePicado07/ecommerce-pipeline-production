# 🛒 E-Commerce Analytics Pipeline

A complete data pipeline implementing **Medallion Architecture** on Databricks.

## 🚀 Live Demo

**[👉 View Live Dashboard](https://ecommerce-pipeline-appuction-zzwnqgphtc6gapcamduktj.streamlit.app/)**

## 📊 What I Built

End-to-end data pipeline processing Brazilian e-commerce data through:

- **Bronze Layer** - Raw data ingestion
- **Silver Layer** - Data cleaning & validation  
- **Gold Layer** - Business analytics & RFM segmentation
- **Dashboard** - Interactive analytics

## 🛠️ Tech Stack

- **Databricks** + **Delta Lake**
- **PySpark** - Data processing
- **Streamlit** - Dashboard
- **Great Expectations** - Data quality

## 📁 Project Structure

```bash
notebooks/
├── 01_bronze_layer.py.ipynb                # Raw data ingestion
├── 02_silver_layer_customers.py.ipynb
├── 02_silver_layer_order.py.ipynb
├── 02_silver_layer_orders_items.py.ipynb
├── 02_silver_layer_products.py.ipynb
├── 03_gold_layer.py.ipynb                  # Business analytics
└── 04_data_quality_checks.py.ipynb         # Data validation

dashboard/
└── app.py                                  # Streamlit dashboard


## 🎯 Features

- **Customer Segmentation** - RFM analysis
- **Revenue Analytics** - Daily trends
- **Product Performance** - Category insights
- **Data Quality** - Automated validation

## 🏃‍♂️ Quick Start

1. Upload data to Databricks
2. Run notebooks in numerical order
3. Launch dashboard: `streamlit run dashboard/app.py`

---

*Learning project for data engineering with Databricks* 🚀
