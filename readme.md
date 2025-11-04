# E-Commerce Analytics Pipeline

A production-grade data engineering project implementing the **Medallion Architecture** (Bronze → Silver → Gold) on **Databricks** for processing and analyzing Brazilian e-commerce data from the Olist platform.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Data Pipeline Layers](#data-pipeline-layers)
  - [Bronze Layer](#bronze-layer-raw-data-ingestion)
  - [Silver Layer](#silver-layer-cleaned--validated-data)
  - [Gold Layer](#gold-layer-business-analytics)
- [Data Quality Framework](#data-quality-framework)
- [Dataset Information](#dataset-information)
- [Technologies Used](#technologies-used)
- [Setup & Installation](#setup--installation)
- [Usage](#usage)
- [Business Insights](#business-insights)
- [Implementation Status](#implementation-status)
- [Future Enhancements](#future-enhancements)

---

## Overview

This project demonstrates modern data engineering best practices by building a scalable, production-ready analytics pipeline. It processes over 43MB of Brazilian e-commerce data through a three-tier medallion architecture, implementing comprehensive data quality checks and generating actionable business insights.

**Key Features:**
- ✅ **Medallion Architecture** - Progressive data refinement through Bronze, Silver, and Gold layers
- ✅ **Delta Lake** - ACID transactions, time travel, and schema enforcement
- ✅ **Data Quality Validation** - Automated quality checks using Great Expectations
- ✅ **Business Analytics** - RFM customer segmentation, revenue analysis, and product performance metrics
- ✅ **Data Governance** - Full metadata tracking and data lineage
- ✅ **Scalable Design** - Built on Apache Spark for distributed processing

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA SOURCES                            │
│  • olist_customers_dataset.csv (8.8 MB)                         │
│  • olist_orders_dataset.csv (17 MB)                             │
│  • olist_order_items_dataset.csv (15 MB)                        │
│  • olist_products_dataset.csv (2.4 MB)                          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      BRONZE LAYER (Raw Data)                     │
│  • bronze.customers          • bronze.orders                    │
│  • bronze.order_items        • bronze.products                  │
│  ─────────────────────────────────────────────────────────────  │
│  Storage: Delta Lake  |  No Transformations  |  Full Audit      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 SILVER LAYER (Cleaned & Validated)               │
│  • silver.customers (+ region enrichment)                       │
│  • silver.orders (+ temporal validation)                        │
│  • silver.order_items (+ business rules)                        │
│  • silver.products (+ standardization)                          │
│  ─────────────────────────────────────────────────────────────  │
│  Data Cleaning | Validation | Enrichment | Standardization      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                   GOLD LAYER (Business Analytics)                │
│  • gold.revenue_by_day - Daily revenue performance              │
│  • gold.customer_rfm_segments - Customer value analysis         │
│  • gold.product_category_summary - Product performance          │
│  ─────────────────────────────────────────────────────────────  │
│  Aggregations | Business Metrics | KPIs | Segmentation          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA QUALITY CHECKS                         │
│  Framework: Great Expectations v0.18.12                         │
│  • Null checks  • Range validation  • Business logic            │
│  • Uniqueness   • Consistency       • Completeness              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
ecommerce-pipeline-production/
│
├── data/                                    # Source CSV files (43 MB total)
│   ├── olist_customers_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_order_items_dataset.csv
│   └── olist_products_dataset.csv
│
├── notebooks/                               # Databricks notebooks
│   ├── 01_bronze_layer.py.ipynb            # Raw data ingestion
│   ├── 02_silver_layer_customers.py.ipynb  # Customer data cleaning
│   ├── 02_silver_layer_order.py.ipynb      # Order data validation
│   ├── 02_silverl_layer_orders_items.ipynb # Order items processing
│   ├── 02_silver_layer_products.py.ipynb   # Product data standardization
│   ├── 03_gold_layer.ipynb                 # Business analytics layer
│   └── 04_data_quality_checks.ipynb        # Quality validation framework
│
├── src/                                     # Source code modules
│   └── src.py
│
├── test/                                    # Unit tests
│   └── test_quality.py
│
├── dashboard/                               # Dashboard application
│   └── app.py
│
├── docs/                                    # Documentation
│   └── architecture.png
│
├── requirements.txt                         # Python dependencies
└── readme.md                                # Project documentation
```

---

## Data Pipeline Layers

### Bronze Layer (Raw Data Ingestion)

**Notebook:** [01_bronze_layer.py.ipynb](notebooks/01_bronze_layer.py.ipynb)

**Purpose:** Ingest raw data from source without any transformations, preserving data in its original form.

**Process:**
1. Read CSV files from the `data/` directory
2. Add metadata columns for lineage tracking:
   - `ingesttime` - Timestamp of data ingestion
   - `data_source` - Source system identifier ("olist")
   - `data_layer` - Current layer ("bronze")
   - `data_status` - Data state ("raw_unaltered")
3. Write to Delta Lake format with overwrite mode
4. Create database and tables in Delta format

**Output Tables:**
- `bronze.customers` - Raw customer data
- `bronze.orders` - Raw order data
- `bronze.order_items` - Raw order line items
- `bronze.products` - Raw product catalog

**Key Features:**
- No data transformation or cleaning
- Full data preservation for audit purposes
- ACID transactions via Delta Lake
- Schema evolution support

---

### Silver Layer (Cleaned & Validated Data)

**Notebooks:**
- [02_silver_layer_customers.py.ipynb](notebooks/02_silver_layer_customers.py.ipynb)
- [02_silver_layer_order.py.ipynb](notebooks/02_silver_layer_order.py.ipynb)
- [02_silverl_layer_orders_items.ipynb](notebooks/02_silverl_layer_orders_items.ipynb)
- [02_silver_layer_products.py.ipynb](notebooks/02_silver_layer_products.py.ipynb)

**Purpose:** Clean, validate, standardize, and enrich data for downstream analytics.

#### **Silver Customers (`silver.customers`)**

**Transformations:**
- **Standardization:**
  - Uppercase and trim `customer_state` and `customer_city`
  - Clean whitespace from all text fields

- **Enrichment:**
  - Add `region` column based on state mapping:
    - **SUDESTE:** SP, RJ, MG, ES
    - **SUL:** RS, SC, PR
    - **NORDESTE:** BA, SE, AL, PE, CE, PB, RN, MA, PI
    - **CENTRO_OESTE:** GO, DF, MT, MS
    - **NORTE:** All others (AM, PA, RO, AC, etc.)

- **Validation:**
  - Remove records with null states
  - Validate city names (alphabetic characters only)
  - Validate zip code prefix length (exactly 5 characters)

- **Metadata:**
  - `processingdate` - Processing timestamp
  - `data_source`, `data_layer`, `data_status: "cleaned"`

#### **Silver Orders (`silver.orders`)**

**Transformations:**
- **Standardization:**
  - Uppercase and trim `order_status`

- **Validation:**
  - **Temporal consistency checks:**
    - Purchase timestamp ≤ Approved timestamp
    - Approved timestamp ≤ Delivered to carrier timestamp
    - Carrier timestamp ≤ Delivered to customer timestamp
  - **Not null checks:** `order_id`, `customer_id`, `order_status`

- **Metadata:**
  - `processed_at`, `data_source`, `data_layer`, `data_status: "cleaned"`

#### **Silver Order Items (`silver.order_items`)**

**Transformations:**
- **Validation:**
  - Not null checks: `product_id`, `seller_id`, `shipping_limit_date`, `price`, `freight_value`
  - Business rule validation (optional): Filter out zero-value transactions

- **Metadata:**
  - `processed_at`, `data_source`, `data_layer`, `data_status: "cleaned"`

#### **Silver Products (`silver.products`)**

**Transformations:**
- **Standardization:**
  - Trim and uppercase `product_category_name`

- **Validation:**
  - `product_name_lenght` > 0
  - `product_description_lenght` > 0
  - `product_photos_qty` > 0

- **Metadata:**
  - `processed_at`, `data_source`, `data_layer`, `data_status: "cleaned"`

---

### Gold Layer (Business Analytics)

**Notebook:** [03_gold_layer.ipynb](notebooks/03_gold_layer.ipynb)

**Purpose:** Create aggregated, business-ready datasets for analytics and reporting.

#### **1. Revenue by Day (`gold.revenue_by_day`)**

**Business Question:** *What is our daily revenue performance?*

**Metrics:**
- `purchase_date` - Date of purchase
- `total_revenue` - Total revenue (price + freight)
- `total_orders` - Total order count
- `total_unique_orders` - Distinct order count

**Use Cases:**
- Daily revenue trend analysis
- Sales performance monitoring
- Forecasting and budgeting

---

#### **2. Customer RFM Segmentation (`gold.customer_rfm_segments`)**

**Business Question:** *Who are our most valuable customers?*

**RFM Analysis Framework:**

| Metric | Description | Scoring (1-5) |
|--------|-------------|---------------|
| **Recency** | Days since last purchase | 5: ≤90 days, 4: ≤180, 3: ≤365, 2: ≤730, 1: >730 |
| **Frequency** | Total number of orders | 5: ≥10, 4: ≥5, 3: ≥3, 2: ≥2, 1: 1 |
| **Monetary** | Total amount spent | 5: ≥$1000, 4: ≥$500, 3: ≥$200, 2: ≥$100, 1: <$100 |

**Customer Segments:**
- **Champions** - Best customers (High R, F, M ≥ 4)
- **Loyal Customers** - Regular buyers (High frequency ≥ 4)
- **Potential Loyalist** - Recent buyers (Recency ≥ 4, Frequency ≥ 2)
- **At Risk** - Haven't purchased recently (Recency ≤ 2, Frequency ≥ 3)
- **Hibernating** - Inactive customers (Low R ≤ 2, Low F ≤ 2)
- **New Customers** - First-time buyers (Recency ≥ 4, Frequency = 1)
- **Need Attention** - All others

**Metrics per Customer:**
- `customer_id`, `customer_state`, `customer_city`, `region`
- `days_since_last_order`, `total_orders`, `total_spent`
- `recency_score`, `frequency_score`, `monetary_score`
- `segment` - Customer classification

**Use Cases:**
- Targeted marketing campaigns
- Customer retention strategies
- Loyalty program optimization
- Churn prediction

---

#### **3. Product Performance by Category (`gold.product_category_summary`)**

**Business Question:** *Which product categories and products are top performers?*

**Category-Level Metrics:**
- `product_category_name`
- `category_total_revenue` - Total revenue per category
- `category_total_orders` - Total orders per category
- `products_in_category` - Number of unique products
- `revenue_rank` - Category ranking by revenue

**Product-Level Metrics:**
- `product_id`
- `item_revenue` - Total revenue per product
- `total_orders` - Orders per product
- `avg_order_value` - Average order value

**Use Cases:**
- Inventory optimization
- Category management
- Product portfolio analysis
- Pricing strategy

---

## Data Quality Framework

**Notebook:** [04_data_quality_checks.ipynb](notebooks/04_data_quality_checks.ipynb)

**Framework:** Great Expectations v0.18.12

**Quality Dimensions:**
- **Completeness** - Null value checks
- **Validity** - Data type and range validation
- **Uniqueness** - Primary key constraints
- **Consistency** - Business logic validation
- **Accuracy** - Cross-table validation

### Validation Coverage

#### **Gold.revenue_by_day**
- ✅ Null checks on all columns
- ✅ Revenue ≥ 0
- ✅ Business logic: total_orders ≥ total_unique_orders
- ✅ Date range validation

#### **Gold.customer_rfm_segments**
- ✅ Customer ID uniqueness
- ✅ RFM scores range (1-5)
- ✅ Recency ≥ 0, Frequency ≥ 1, Monetary > 0
- ✅ Valid segment values

#### **Gold.product_category_summary**
- ✅ Product ID uniqueness
- ✅ Revenue > 0, Orders ≥ 1
- ✅ Average order value consistency

**Quality Reporting:**
- Success rate per table
- Overall pipeline success rate
- Failed record counts
- Quality status classification:
  - **EXCELLENT:** ≥ 95% success rate
  - **GOOD:** ≥ 80% success rate
  - **NEEDS ATTENTION:** < 80% success rate

---

## Dataset Information

**Source:** Brazilian E-Commerce Public Dataset by Olist

This dataset contains real commercial data from the Brazilian e-commerce platform Olist, covering orders made between 2016 and 2018.

| File | Size | Records | Description |
|------|------|---------|-------------|
| `olist_customers_dataset.csv` | 8.8 MB | ~99,441 | Customer information and location |
| `olist_orders_dataset.csv` | 17 MB | ~99,441 | Order details and timestamps |
| `olist_order_items_dataset.csv` | 15 MB | ~112,650 | Order line items with pricing |
| `olist_products_dataset.csv` | 2.4 MB | ~32,951 | Product catalog and attributes |

**Total Dataset Size:** ~43 MB

**Key Entities:**
- **Customers:** 99,441 unique customers across Brazil
- **Orders:** 99,441 orders with complete lifecycle timestamps
- **Products:** 32,951 products across multiple categories
- **Order Items:** 112,650 individual line items

---

## Technologies Used

| Technology | Purpose | Version |
|------------|---------|---------|
| **Apache Spark (PySpark)** | Distributed data processing engine | Latest |
| **Delta Lake** | ACID-compliant storage layer | Latest |
| **Databricks Community Edition** | Cloud-based development platform | N/A |
| **Great Expectations** | Data quality validation framework | 0.18.12 |
| **Python** | Primary programming language | 3.x |
| **SQL (Spark SQL)** | Data querying and transformation | N/A |

**Planned Technologies:**
- **Prefect** - Workflow orchestration
- **Streamlit** - Interactive dashboard

---

## Setup & Installation

### Prerequisites
- Databricks Community Edition account
- Python 3.x installed locally (for development)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd ecommerce-pipeline-production
   ```

2. **Upload Data to Databricks**
   - Create a Databricks workspace
   - Upload CSV files from `data/` directory to DBFS:
     ```
     /FileStore/tables/olist_customers_dataset.csv
     /FileStore/tables/olist_orders_dataset.csv
     /FileStore/tables/olist_order_items_dataset.csv
     /FileStore/tables/olist_products_dataset.csv
     ```

3. **Import Notebooks**
   - Import all notebooks from `notebooks/` directory into Databricks workspace
   - Maintain the same folder structure

4. **Configure File Paths**
   - Update file paths in notebooks if you used different DBFS locations
   - Default path pattern: `/FileStore/tables/<filename>.csv`

5. **Install Dependencies**
   - Great Expectations is pre-installed in Databricks
   - For local development, install requirements:
     ```bash
     pip install pyspark delta-spark great-expectations==0.18.12
     ```

---

## Usage

### Running the Pipeline

Execute notebooks in the following order:

**1. Bronze Layer Ingestion**
```python
# Run: 01_bronze_layer.py.ipynb
# Creates: bronze.customers, bronze.orders, bronze.order_items, bronze.products
```

**2. Silver Layer Processing** (Run in any order)
```python
# Run: 02_silver_layer_customers.py.ipynb
# Run: 02_silver_layer_order.py.ipynb
# Run: 02_silverl_layer_orders_items.ipynb
# Run: 02_silver_layer_products.py.ipynb
```

**3. Gold Layer Analytics**
```python
# Run: 03_gold_layer.ipynb
# Creates: gold.revenue_by_day, gold.customer_rfm_segments, gold.product_category_summary
```

**4. Data Quality Validation**
```python
# Run: 04_data_quality_checks.ipynb
# Validates all Gold layer tables
```

### Querying the Data

**Example: Daily Revenue Analysis**
```sql
SELECT
    purchase_date,
    total_revenue,
    total_unique_orders,
    ROUND(total_revenue / total_unique_orders, 2) as avg_order_value
FROM gold.revenue_by_day
WHERE purchase_date >= '2018-01-01'
ORDER BY purchase_date DESC;
```

**Example: Customer Segmentation**
```sql
SELECT
    segment,
    COUNT(*) as customer_count,
    ROUND(AVG(total_spent), 2) as avg_ltv,
    ROUND(AVG(total_orders), 1) as avg_orders
FROM gold.customer_rfm_segments
GROUP BY segment
ORDER BY customer_count DESC;
```

**Example: Top Product Categories**
```sql
SELECT
    product_category_name,
    category_total_revenue,
    category_total_orders,
    revenue_rank
FROM gold.product_category_summary
WHERE revenue_rank <= 10
ORDER BY revenue_rank;
```

---

## Business Insights

This pipeline enables comprehensive business analysis across multiple dimensions:

### 1. Revenue Analytics
- Daily, weekly, and monthly revenue trends
- Order volume and average order value metrics
- Revenue forecasting and growth analysis

### 2. Customer Intelligence
- Customer lifetime value (LTV) analysis
- Churn risk identification (At Risk, Hibernating segments)
- High-value customer identification (Champions, Loyal Customers)
- Customer acquisition and retention metrics

### 3. Product Performance
- Top-performing categories and products
- Revenue contribution by category
- Product portfolio optimization opportunities
- Inventory planning and demand forecasting

### 4. Geographic Analysis
- Regional sales distribution (5 regions across Brazil)
- State and city-level performance
- Geographic expansion opportunities

### 5. Operational Metrics
- Order fulfillment timeline analysis
- Delivery performance monitoring
- Shipping cost analysis

---

## Implementation Status

### ✅ Completed

- **Bronze Layer:** 4/4 tables implemented
  - ✅ bronze.customers
  - ✅ bronze.orders
  - ✅ bronze.order_items
  - ✅ bronze.products

- **Silver Layer:** 4/4 tables implemented
  - ✅ silver.customers (with region enrichment)
  - ✅ silver.orders (with temporal validation)
  - ✅ silver.order_items (with business rules)
  - ✅ silver.products (with standardization)

- **Gold Layer:** 3/3 analytics tables
  - ✅ gold.revenue_by_day
  - ✅ gold.customer_rfm_segments
  - ✅ gold.product_category_summary

- **Data Quality:** Comprehensive validation framework
  - ✅ Great Expectations integration
  - ✅ Automated quality checks
  - ✅ Quality reporting and scoring

### 🚧 In Progress / Planned

- **Workflow Orchestration:** Prefect integration
- **Dashboard:** Streamlit application
- **Testing:** Unit test implementation
- **Documentation:** API documentation
- **CI/CD:** Automated deployment pipeline

---

## Future Enhancements

### Short-Term
1. **Workflow Orchestration**
   - Implement Prefect for automated pipeline execution
   - Schedule daily/weekly batch runs
   - Add failure notifications and retry logic

2. **Interactive Dashboard**
   - Build Streamlit dashboard for business users
   - Real-time metrics visualization
   - Self-service analytics interface

3. **Testing Framework**
   - Unit tests for transformation logic
   - Integration tests for end-to-end pipeline
   - Performance benchmarking

### Long-Term
1. **Advanced Analytics**
   - Predictive modeling (churn prediction, demand forecasting)
   - Customer cohort analysis
   - Market basket analysis

2. **Real-Time Processing**
   - Streaming data ingestion with Spark Streaming
   - Real-time dashboards
   - Event-driven architecture

3. **Data Governance**
   - Data catalog integration
   - PII masking and encryption
   - GDPR compliance features

4. **Performance Optimization**
   - Table partitioning strategies
   - Z-ordering for query optimization
   - Caching layer implementation

---

## Best Practices Implemented

1. **Medallion Architecture** - Progressive data refinement
2. **Idempotent Operations** - Repeatable pipeline runs
3. **Schema Evolution** - Flexible schema management
4. **Metadata Tracking** - Full data lineage
5. **Data Validation** - Comprehensive quality checks
6. **Delta Lake** - ACID transactions and time travel
7. **Modular Design** - Separation of concerns
8. **Business Focus** - Analytics-ready gold layer

---

## Contributing

Contributions are welcome! Please follow these guidelines:
1. Fork the repository
2. Create a feature branch
3. Implement changes with tests
4. Submit a pull request

---

## License

This project is for educational and demonstration purposes.

---

## Contact

For questions or feedback about this project, please open an issue in the repository.

---

**Built with ❤️ on Databricks**
