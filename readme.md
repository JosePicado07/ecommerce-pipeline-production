```markdown
# 🛒 E-Commerce Analytics Pipeline

A complete data pipeline implementing **Medallion Architecture** on Databricks, processing Brazilian e-commerce data from Olist.

## 🚀 Live Demo

**[👉 View Live Dashboard](https://ecommerce-pipeline-appuction-zzwnqgphtc6gapcamduktj.streamlit.app/)**

## 📊 Architecture

```
Raw CSVs → Bronze (Raw) → Silver (Cleaned) → Gold (Analytics) → Dashboard
```

## 🛠️ Tech Stack

- **Databricks** + **Delta Lake** (Medallion Architecture)
- **PySpark** - Data processing
- **Great Expectations** - Data quality
- **Streamlit** - Dashboard
- **Plotly** - Visualizations

## 📁 Pipeline Structure

### **Bronze Layer** (Raw Ingestion)
- `01_bronze_layer.py.ipynb` - Raw data ingestion

### **Silver Layer** (Data Cleaning)
- `02_silver_layer_customers.py.ipynb` - Customer data
- `02_silver_layer_order.py.ipynb` - Order data  
- `02_silver_layer_orders_items.py.ipynb` - Order items
- `02_silver_layer_products.py.ipynb` - Product data

### **Gold Layer** (Business Analytics)
- `03_gold_layer.py.ipynb` - RFM segmentation & revenue metrics

### **Data Quality**
- `04_data_quality_checks.py.ipynb` - Validation framework

## 🎯 Key Features

- **Customer RFM Segmentation** - Identify high-value customers
- **Revenue Analytics** - Daily trends & performance
- **Product Performance** - Category-level insights
- **Data Quality Framework** - Automated validation with Great Expectations

## 🏃‍♂️ Quick Start

1. **Upload CSV files** to Databricks DBFS
2. **Run notebooks in order**:
   ```bash
   01_bronze → 02_silver_* → 03_gold → 04_quality
   ```
3. **Launch dashboard**:
   ```bash
   streamlit run dashboard/app.py
   ```

## 📈 Results

- **99,441+ customers** analyzed with RFM segmentation
- **43MB e-commerce data** processed end-to-end
- **Interactive dashboard** with real-time insights
- **Production-ready** data pipeline

---

*Hands-on learning project for Databricks & Medallion Architecture* 🚀
