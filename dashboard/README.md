# E-Commerce Analytics Dashboard

An interactive Streamlit dashboard for visualizing Brazilian e-commerce data analytics from the Olist platform (2016-2018).

## Features

### 📊 Overview Page
- **Key Metrics**: Total Revenue, Total Orders, Total Customers, Average Order Value
- **Revenue Trend**: Last 90 days revenue performance
- **Customer Distribution**: Pie chart showing customer segments
- **Top Categories**: Top 10 product categories by revenue
- **Regional Analysis**: Customer and revenue distribution across Brazilian regions
- **Quick Statistics**: Date range, active days, product categories, and peak revenue day

### 💰 Revenue Analytics Page
- **Time Period Filters**: Last 30/90 days, 6 months, 1 year, or all time
- **Revenue Metrics**: Total, average daily revenue, total orders, average order value
- **Trend Analysis**: Revenue and orders over time with dual-axis chart
- **Revenue Distribution**: Histogram showing daily revenue patterns
- **Day of Week Analysis**: Average revenue by weekday
- **Monthly Performance**: Monthly revenue aggregation
- **Statistics Table**: Mean, median, std dev, min, max, and percentiles

### 👥 Customer Segments Page
- **RFM Segmentation**: Customer analysis using Recency, Frequency, Monetary methodology
- **Segment Metrics**: Total customers, average LTV, average orders, champions percentage
- **Segment Filters**: Filter analysis by specific customer segments
- **Distribution Charts**: Customer count and revenue by segment
- **RFM Score Analysis**: Individual distribution of R, F, and M scores
- **Segment Characteristics**: Detailed table with metrics per segment
- **Regional Analysis**: Customer distribution and LTV by Brazilian regions
- **Behavior Scatter Plot**: Orders vs spending visualization with segment coloring

### 🏆 Product Performance Page
- **Category Metrics**: Total revenue, product count, average products per category
- **Top 10 Categories**: Horizontal bar chart with revenue rankings
- **Product Count Analysis**: Categories with most products
- **Order Analysis**: Categories with most orders
- **Performance Comparison**: Scatter plot showing orders vs revenue
- **Revenue Distribution**: Treemap visualization of revenue share
- **Average Order Value**: Top categories by AOV
- **Detailed Table**: Complete category performance statistics
- **Product Drill-Down**: View top 20 products within selected category

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone the repository** (if not already done)
   ```bash
   cd ecommerce-pipeline-production
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Navigate to dashboard folder**
   ```bash
   cd dashboard
   ```

## Running the Dashboard

### Local Development

Run the Streamlit application:

```bash
streamlit run app.py
```

The dashboard will automatically open in your default browser at `http://localhost:8501`

### Custom Port

To run on a specific port:

```bash
streamlit run app.py --server.port 8080
```

### Network Access

To allow access from other devices on your network:

```bash
streamlit run app.py --server.address 0.0.0.0
```

## Data Configuration

### Current Setup (Demo Mode)

The dashboard currently generates sample data matching the schema of your Gold layer tables. This allows you to test the UI without connecting to Databricks.

### Connecting to Real Data

To connect to your actual Databricks Delta Lake tables, modify the `load_data()` function in `app.py`:

```python
@st.cache_data
def load_data():
    """Load data from Delta Lake tables"""
    from databricks import sql
    import os

    # Connection configuration
    connection = sql.connect(
        server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        access_token=os.getenv("DATABRICKS_TOKEN")
    )

    # Load revenue data
    revenue_data = pd.read_sql(
        "SELECT * FROM gold.revenue_by_day",
        connection
    )

    # Load customer RFM data
    customer_data = pd.read_sql(
        "SELECT * FROM gold.customer_rfm_segments",
        connection
    )

    # Load category summary
    category_summary = pd.read_sql(
        "SELECT * FROM gold.product_category_summary",
        connection
    )

    connection.close()

    return revenue_data, customer_data, category_summary
```

### Environment Variables

Create a `.env` file in the dashboard folder:

```env
DATABRICKS_SERVER_HOSTNAME=your-workspace.cloud.databricks.com
DATABRICKS_HTTP_PATH=/sql/1.0/warehouses/your-warehouse-id
DATABRICKS_TOKEN=your-access-token
```

## Dashboard Architecture

```
dashboard/
├── app.py                  # Main Streamlit application
├── README.md              # This file
└── .env                   # Environment variables (create this)
```

### Code Structure

The `app.py` file is organized into clear sections:

1. **Configuration**: Page setup and custom CSS styling
2. **Data Loading**: Functions to load and cache data
3. **Utility Functions**: Currency and number formatting
4. **Page Functions**: One function per dashboard page
   - `show_overview()` - Overview page
   - `show_revenue_analytics()` - Revenue analytics page
   - `show_customer_segments()` - Customer segmentation page
   - `show_product_performance()` - Product performance page
5. **Main Application**: Navigation and page routing

## Customization

### Changing Colors

Modify the color schemes in the chart configurations:

```python
# Example: Change revenue trend color
color_discrete_sequence=['#667eea']  # Purple
# Change to:
color_discrete_sequence=['#10b981']  # Green
```

### Adding New Metrics

1. Calculate the metric from your data
2. Add a new `st.metric()` component
3. Update the column layout if needed

### Adding New Charts

Use Plotly Express or Plotly Graph Objects:

```python
import plotly.express as px

fig = px.bar(data, x='category', y='value')
st.plotly_chart(fig, use_container_width=True)
```

## Performance Optimization

### Data Caching

The `@st.cache_data` decorator caches data loading to improve performance:

```python
@st.cache_data
def load_data():
    # Data loading logic
    return data
```

### Chart Sampling

For large datasets, the dashboard samples data for scatter plots to maintain performance:

```python
sample_size = min(1000, len(data))
sample_data = data.sample(sample_size)
```

## Troubleshooting

### Port Already in Use

If port 8501 is already in use:
```bash
streamlit run app.py --server.port 8502
```

### Module Not Found Error

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Data Loading Issues

1. Check your Databricks connection credentials
2. Verify table names match your Gold layer tables
3. Ensure you have read permissions on the tables

### Chart Not Displaying

1. Check browser console for JavaScript errors
2. Clear Streamlit cache: Click "☰" → "Clear cache"
3. Restart the Streamlit server

## Browser Compatibility

Tested and optimized for:
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Edge
- ✅ Safari

## Features Roadmap

- [ ] Export charts as PNG/PDF
- [ ] Download data as CSV
- [ ] Custom date range picker
- [ ] Comparison mode (compare periods)
- [ ] Email report scheduling
- [ ] Dark mode toggle
- [ ] Real-time data refresh

## Tech Stack

- **Frontend**: Streamlit 1.29.0
- **Charts**: Plotly 5.18.0
- **Data Processing**: Pandas 2.1.3, NumPy 1.24.3
- **Data Source**: Databricks Delta Lake
- **Language**: Python 3.8+

## Contributing

To add new features:

1. Create a new branch
2. Add your feature to `app.py`
3. Test thoroughly with sample data
4. Submit a pull request

## License

This dashboard is part of the E-Commerce Analytics Pipeline project.

---

**Built with ❤️ using Streamlit**
