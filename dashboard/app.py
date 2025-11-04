"""
E-Commerce Analytics Dashboard
Built with Streamlit for interactive data visualization
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional UI
st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 1rem 2rem;
        background-color: #f8fafc;
    }

    /* Headers */
    h1 {
        color: #1e293b;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    h2 {
        color: #334155;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    h3 {
        color: #475569;
        font-weight: 500;
        font-size: 1.1rem;
    }

    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 600;
        color: #1e293b;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #64748b;
        font-weight: 500;
    }

    /* Sidebar */
    .css-1d391kg, [data-testid="stSidebar"] {
        background-color: #ffffff;
    }

    /* Radio buttons */
    .stRadio > label {
        font-weight: 500;
        color: #1e293b;
    }

    /* Info boxes */
    .stAlert {
        border-radius: 8px;
    }

    /* Divider */
    hr {
        margin: 2rem 0;
        border-color: #e2e8f0;
    }
    </style>
    """, unsafe_allow_html=True)


# Color palette - Professional and modern
COLORS = {
    'primary': '#3b82f6',      # Blue
    'secondary': '#8b5cf6',    # Purple
    'success': '#10b981',      # Green
    'warning': '#f59e0b',      # Orange
    'danger': '#ef4444',       # Red
    'info': '#06b6d4',         # Cyan
    'dark': '#1e293b',         # Dark slate
    'light': '#f1f5f9'         # Light slate
}

# Chart template
CHART_TEMPLATE = 'plotly_white'


# ========================================================================================
# DATA LOADING FUNCTIONS
# ========================================================================================

@st.cache_data
def load_data():
    """Load data from CSV files (simulating Delta Lake tables)"""
    try:
        np.random.seed(42)  # For consistent data

        # Load revenue by day
        revenue_data = pd.DataFrame({
            'purchase_date': pd.date_range(start='2016-09-04', end='2018-09-03', freq='D'),
        })
        revenue_data['total_revenue'] = np.random.uniform(5000, 45000, len(revenue_data)) + \
                                        np.sin(np.arange(len(revenue_data)) * 0.1) * 5000
        revenue_data['total_orders'] = (revenue_data['total_revenue'] / 200 + \
                                       np.random.uniform(-20, 20, len(revenue_data))).astype(int)
        revenue_data['total_unique_orders'] = revenue_data['total_orders'] - np.random.randint(0, 5, len(revenue_data))

        # Load customer RFM segments
        segments = ['Champions', 'Loyal Customers', 'Potential Loyalist',
                   'At Risk', 'Hibernating', 'New Customers', 'Need Attention']
        customer_data = pd.DataFrame({
            'customer_id': range(1, 10001),
            'segment': np.random.choice(segments, 10000, p=[0.15, 0.20, 0.15, 0.10, 0.15, 0.15, 0.10]),
            'recency_score': np.random.randint(1, 6, 10000),
            'frequency_score': np.random.randint(1, 6, 10000),
            'monetary_score': np.random.randint(1, 6, 10000),
            'total_spent': np.random.lognormal(6, 1, 10000),
            'total_orders': np.random.randint(1, 15, 10000),
            'days_since_last_order': np.random.randint(0, 800, 10000),
            'region': np.random.choice(['SUDESTE', 'SUL', 'NORDESTE', 'CENTRO_OESTE', 'NORTE'],
                                      10000, p=[0.40, 0.25, 0.20, 0.10, 0.05])
        })

        # Load product category summary
        categories = ['Bed & Bath', 'Health & Beauty', 'Sports & Leisure', 'Computers',
                     'Furniture', 'Housewares', 'Watches & Gifts', 'Phones',
                     'Automotive', 'Toys', 'Cool Stuff', 'Garden Tools']
        product_data = pd.DataFrame({
            'product_id': range(1, 1001),
            'product_category_name': np.random.choice(categories, 1000),
        })
        product_data['item_revenue'] = np.random.lognormal(8, 1.5, 1000)
        product_data['total_orders'] = np.random.randint(1, 500, 1000)
        product_data['avg_order_value'] = product_data['item_revenue'] / product_data['total_orders']

        # Calculate category summaries
        category_summary = product_data.groupby('product_category_name').agg({
            'item_revenue': 'sum',
            'total_orders': 'sum',
            'product_id': 'count'
        }).reset_index()
        category_summary.columns = ['product_category_name', 'category_total_revenue',
                                    'category_total_orders', 'products_in_category']
        category_summary['revenue_rank'] = category_summary['category_total_revenue'].rank(ascending=False)
        category_summary = category_summary.sort_values('revenue_rank')

        return revenue_data, customer_data, category_summary, product_data

    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None, None, None, None


def format_currency(value):
    """Format value as Brazilian Real currency"""
    return f"R$ {value:,.2f}"


def format_number(value):
    """Format large numbers with K/M suffix"""
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    else:
        return f"{value:.0f}"


# ========================================================================================
# PAGE: OVERVIEW
# ========================================================================================

def show_overview(revenue_data, customer_data, category_summary, product_data):
    """Display overview page with key metrics and summary"""

    st.title("📊 E-Commerce Analytics Overview")
    st.markdown("Dashboard for Brazilian E-Commerce Data (2016-2018)")
    st.markdown("---")

    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)

    total_revenue = revenue_data['total_revenue'].sum()
    total_orders = revenue_data['total_unique_orders'].sum()
    total_customers = len(customer_data)
    avg_order_value = total_revenue / total_orders

    with col1:
        st.metric(
            label="💰 Total Revenue",
            value=format_currency(total_revenue),
            delta="100%"
        )

    with col2:
        st.metric(
            label="🛒 Total Orders",
            value=format_number(total_orders),
            delta=f"{len(revenue_data)} days"
        )

    with col3:
        st.metric(
            label="👥 Total Customers",
            value=format_number(total_customers),
            delta=f"{format_number(total_customers/len(revenue_data))} per day"
        )

    with col4:
        st.metric(
            label="📈 Avg Order Value",
            value=format_currency(avg_order_value),
            delta=f"±{format_currency(revenue_data['total_revenue'].std()/revenue_data['total_unique_orders'].mean())}"
        )

    st.markdown("##")

    # Two column layout for charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📅 Revenue Trend (Last 90 Days)")
        recent_data = revenue_data.tail(90).copy()

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=recent_data['purchase_date'],
            y=recent_data['total_revenue'],
            mode='lines',
            name='Revenue',
            line=dict(color=COLORS['primary'], width=2),
            fill='tozeroy',
            fillcolor=f"rgba(59, 130, 246, 0.1)"
        ))

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            hovermode='x unified',
            showlegend=False,
            xaxis_title="",
            yaxis_title="Revenue (R$)",
            title=None
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 👥 Customer Segments")
        segment_counts = customer_data['segment'].value_counts().reset_index()
        segment_counts.columns = ['segment', 'count']

        colors_pie = [COLORS['primary'], COLORS['success'], COLORS['info'],
                     COLORS['warning'], COLORS['danger'], COLORS['secondary'], '#94a3b8']

        fig = go.Figure(data=[go.Pie(
            labels=segment_counts['segment'],
            values=segment_counts['count'],
            hole=0.4,
            marker=dict(colors=colors_pie),
            textposition='inside',
            textinfo='percent'
        )])

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            showlegend=True,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("##")

    # Bottom row
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏆 Top 10 Categories by Revenue")
        top_categories = category_summary.head(10)

        fig = go.Figure(go.Bar(
            y=top_categories['product_category_name'],
            x=top_categories['category_total_revenue'],
            orientation='h',
            marker=dict(
                color=top_categories['category_total_revenue'],
                colorscale='Blues',
                showscale=False
            ),
            text=[format_currency(x) for x in top_categories['category_total_revenue']],
            textposition='outside'
        ))

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=400,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="Revenue (R$)",
            yaxis_title="",
            yaxis=dict(autorange="reversed")
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🌍 Regional Distribution")
        regional_data = customer_data.groupby('region').agg({
            'customer_id': 'count',
            'total_spent': 'sum'
        }).reset_index()
        regional_data.columns = ['region', 'customers', 'revenue']
        regional_data = regional_data.sort_values('customers', ascending=False)

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=regional_data['region'],
            y=regional_data['customers'],
            name='Customers',
            marker_color=COLORS['primary'],
            yaxis='y'
        ))
        fig.add_trace(go.Scatter(
            x=regional_data['region'],
            y=regional_data['revenue'],
            name='Revenue',
            marker_color=COLORS['success'],
            yaxis='y2',
            mode='lines+markers',
            line=dict(width=3)
        ))

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=400,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="",
            yaxis_title="Number of Customers",
            yaxis2=dict(title='Revenue (R$)', overlaying='y', side='right'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            barmode='group'
        )
        st.plotly_chart(fig, use_container_width=True)

    # Summary Statistics
    st.markdown("##")
    st.markdown("### 📊 Quick Statistics")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.info(f"**Date Range**\n\n{revenue_data['purchase_date'].min().strftime('%Y-%m-%d')} to\n\n{revenue_data['purchase_date'].max().strftime('%Y-%m-%d')}")

    with col2:
        st.info(f"**Active Days**\n\n{len(revenue_data)} days\n\n~2 years")

    with col3:
        st.info(f"**Categories**\n\n{len(category_summary)} categories\n\n{len(product_data)} products")

    with col4:
        peak_day = revenue_data.loc[revenue_data['total_revenue'].idxmax()]
        st.success(f"**Peak Revenue**\n\n{format_currency(peak_day['total_revenue'])}\n\n{peak_day['purchase_date'].strftime('%Y-%m-%d')}")

    with col5:
        champions = len(customer_data[customer_data['segment'] == 'Champions'])
        st.success(f"**Champions**\n\n{format_number(champions)} customers\n\n{champions/len(customer_data)*100:.1f}%")


# ========================================================================================
# PAGE: REVENUE ANALYTICS
# ========================================================================================

def show_revenue_analytics(revenue_data):
    """Display revenue analytics page with detailed charts and trends"""

    st.title("💰 Revenue Analytics")
    st.markdown("Detailed revenue performance and trends analysis")
    st.markdown("---")

    # Date range filter
    col1, col2, col3 = st.columns([2, 2, 6])
    with col1:
        date_range = st.selectbox(
            "Time Period",
            ["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year", "All Time"],
            index=1
        )

    # Filter data based on selection
    if date_range == "Last 30 Days":
        filtered_data = revenue_data.tail(30)
    elif date_range == "Last 90 Days":
        filtered_data = revenue_data.tail(90)
    elif date_range == "Last 6 Months":
        filtered_data = revenue_data.tail(180)
    elif date_range == "Last Year":
        filtered_data = revenue_data.tail(365)
    else:
        filtered_data = revenue_data

    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)

    total_revenue = filtered_data['total_revenue'].sum()
    avg_daily_revenue = filtered_data['total_revenue'].mean()
    total_orders = filtered_data['total_unique_orders'].sum()
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0

    with col1:
        st.metric("Total Revenue", format_currency(total_revenue))

    with col2:
        st.metric("Avg Daily Revenue", format_currency(avg_daily_revenue))

    with col3:
        st.metric("Total Orders", format_number(total_orders))

    with col4:
        st.metric("Avg Order Value", format_currency(avg_order_value))

    st.markdown("##")

    # Main revenue trend chart
    st.markdown("### 📈 Revenue & Orders Trend")

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=filtered_data['purchase_date'],
            y=filtered_data['total_revenue'],
            name="Revenue",
            line=dict(color=COLORS['primary'], width=2),
            fill='tozeroy',
            fillcolor=f"rgba(59, 130, 246, 0.1)"
        ),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=filtered_data['purchase_date'],
            y=filtered_data['total_unique_orders'],
            name="Orders",
            line=dict(color=COLORS['success'], width=2)
        ),
        secondary_y=True
    )

    fig.update_layout(
        template=CHART_TEMPLATE,
        height=400,
        hovermode='x unified',
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=0, r=0, t=10, b=0)
    )

    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Revenue (R$)", secondary_y=False)
    fig.update_yaxes(title_text="Number of Orders", secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("##")

    # Two column layout for additional charts
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📊 Revenue Distribution")

        fig = go.Figure(data=[go.Histogram(
            x=filtered_data['total_revenue'],
            nbinsx=25,
            marker_color=COLORS['primary'],
            opacity=0.8
        )])

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="Revenue (R$)",
            yaxis_title="Frequency",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 📅 Revenue by Day of Week")
        filtered_data_copy = filtered_data.copy()
        filtered_data_copy['day_of_week'] = pd.to_datetime(filtered_data_copy['purchase_date']).dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        dow_data = filtered_data_copy.groupby('day_of_week')['total_revenue'].mean().reindex(day_order).reset_index()

        fig = go.Figure(go.Bar(
            x=dow_data['day_of_week'],
            y=dow_data['total_revenue'],
            marker=dict(
                color=dow_data['total_revenue'],
                colorscale='Viridis',
                showscale=False
            ),
            text=[format_currency(x) for x in dow_data['total_revenue']],
            textposition='outside'
        ))

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="",
            yaxis_title="Avg Revenue (R$)",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # Monthly Analysis
    st.markdown("##")
    st.markdown("### 📆 Monthly Revenue Performance")

    monthly_data = filtered_data.copy()
    monthly_data['year_month'] = pd.to_datetime(monthly_data['purchase_date']).dt.to_period('M').astype(str)
    monthly_summary = monthly_data.groupby('year_month').agg({
        'total_revenue': 'sum',
        'total_unique_orders': 'sum'
    }).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=monthly_summary['year_month'],
        y=monthly_summary['total_revenue'],
        name='Revenue',
        marker_color=COLORS['primary'],
        text=[format_currency(x) for x in monthly_summary['total_revenue']],
        textposition='outside'
    ))

    fig.update_layout(
        template=CHART_TEMPLATE,
        height=350,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="",
        yaxis_title="Revenue (R$)",
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    # Statistics Table
    st.markdown("##")
    st.markdown("### 📋 Revenue Statistics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Mean", format_currency(filtered_data['total_revenue'].mean()))
        st.metric("Median", format_currency(filtered_data['total_revenue'].median()))

    with col2:
        st.metric("Std Dev", format_currency(filtered_data['total_revenue'].std()))
        st.metric("Min", format_currency(filtered_data['total_revenue'].min()))

    with col3:
        st.metric("Max", format_currency(filtered_data['total_revenue'].max()))
        st.metric("25th %ile", format_currency(filtered_data['total_revenue'].quantile(0.25)))

    with col4:
        st.metric("75th %ile", format_currency(filtered_data['total_revenue'].quantile(0.75)))
        st.metric("Range", format_currency(filtered_data['total_revenue'].max() - filtered_data['total_revenue'].min()))


# ========================================================================================
# PAGE: CUSTOMER SEGMENTS
# ========================================================================================

def show_customer_segments(customer_data):
    """Display customer segmentation analysis using RFM methodology"""

    st.title("👥 Customer Segmentation Analysis")
    st.markdown("RFM-based customer insights and behavior patterns")
    st.markdown("---")

    # Overview metrics
    col1, col2, col3, col4 = st.columns(4)

    avg_ltv = customer_data['total_spent'].mean()
    avg_orders = customer_data['total_orders'].mean()
    champions_pct = len(customer_data[customer_data['segment'] == 'Champions']) / len(customer_data) * 100

    with col1:
        st.metric("Total Customers", format_number(len(customer_data)))

    with col2:
        st.metric("Avg Customer LTV", format_currency(avg_ltv))

    with col3:
        st.metric("Avg Orders/Customer", f"{avg_orders:.1f}")

    with col4:
        st.metric("Champions %", f"{champions_pct:.1f}%")

    st.markdown("##")

    # Segment selector
    col1, col2 = st.columns([2, 8])
    with col1:
        selected_segment = st.selectbox(
            "Filter by Segment",
            ["All Segments"] + sorted(customer_data['segment'].unique().tolist())
        )

    filtered_customers = customer_data if selected_segment == "All Segments" else customer_data[customer_data['segment'] == selected_segment]

    # Two column layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🎯 Customer Segments")
        segment_data = customer_data['segment'].value_counts().reset_index()
        segment_data.columns = ['segment', 'count']
        segment_data = segment_data.sort_values('count', ascending=True)

        fig = go.Figure(go.Bar(
            y=segment_data['segment'],
            x=segment_data['count'],
            orientation='h',
            marker_color=COLORS['primary'],
            text=[f"{x:,}" for x in segment_data['count']],
            textposition='outside'
        ))

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=350,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="Number of Customers",
            yaxis_title="",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 💰 Revenue by Segment")
        segment_revenue = customer_data.groupby('segment')['total_spent'].sum().reset_index()
        segment_revenue = segment_revenue.sort_values('total_spent', ascending=False)

        colors_segment = [COLORS['primary'], COLORS['success'], COLORS['info'],
                         COLORS['warning'], COLORS['danger'], COLORS['secondary'], '#94a3b8']

        fig = go.Figure(data=[go.Pie(
            labels=segment_revenue['segment'],
            values=segment_revenue['total_spent'],
            hole=0.4,
            marker=dict(colors=colors_segment),
            textposition='inside',
            textinfo='label+percent'
        )])

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=350,
            margin=dict(l=0, r=0, t=10, b=0),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # RFM Score Analysis
    st.markdown("##")
    st.markdown("### 📊 RFM Score Distribution")

    col1, col2, col3 = st.columns(3)

    with col1:
        recency_dist = filtered_customers['recency_score'].value_counts().sort_index().reset_index()
        recency_dist.columns = ['score', 'count']

        fig = go.Figure(go.Bar(
            x=recency_dist['score'],
            y=recency_dist['count'],
            marker_color=COLORS['success'],
            text=recency_dist['count'],
            textposition='outside'
        ))

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=250,
            margin=dict(l=0, r=0, t=30, b=0),
            title="Recency (1=Old, 5=Recent)",
            title_font_size=14,
            xaxis_title="Score",
            yaxis_title="Count",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        frequency_dist = filtered_customers['frequency_score'].value_counts().sort_index().reset_index()
        frequency_dist.columns = ['score', 'count']

        fig = go.Figure(go.Bar(
            x=frequency_dist['score'],
            y=frequency_dist['count'],
            marker_color=COLORS['primary'],
            text=frequency_dist['count'],
            textposition='outside'
        ))

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=250,
            margin=dict(l=0, r=0, t=30, b=0),
            title="Frequency (1=Low, 5=High)",
            title_font_size=14,
            xaxis_title="Score",
            yaxis_title="Count",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        monetary_dist = filtered_customers['monetary_score'].value_counts().sort_index().reset_index()
        monetary_dist.columns = ['score', 'count']

        fig = go.Figure(go.Bar(
            x=monetary_dist['score'],
            y=monetary_dist['count'],
            marker_color=COLORS['secondary'],
            text=monetary_dist['count'],
            textposition='outside'
        ))

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=250,
            margin=dict(l=0, r=0, t=30, b=0),
            title="Monetary (1=Low, 5=High)",
            title_font_size=14,
            xaxis_title="Score",
            yaxis_title="Count",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # Segment characteristics table
    st.markdown("##")
    st.markdown("### 📈 Segment Characteristics")

    segment_stats = customer_data.groupby('segment').agg({
        'customer_id': 'count',
        'total_spent': ['mean', 'sum'],
        'total_orders': 'mean',
        'days_since_last_order': 'mean'
    }).round(2)

    segment_stats.columns = ['Customers', 'Avg LTV', 'Total Revenue', 'Avg Orders', 'Avg Days Since Last']
    segment_stats = segment_stats.reset_index()
    segment_stats = segment_stats.sort_values('Total Revenue', ascending=False)

    # Format for display
    segment_stats['Avg LTV'] = segment_stats['Avg LTV'].apply(lambda x: format_currency(x))
    segment_stats['Total Revenue'] = segment_stats['Total Revenue'].apply(lambda x: format_currency(x))
    segment_stats['Avg Orders'] = segment_stats['Avg Orders'].apply(lambda x: f"{x:.1f}")
    segment_stats['Avg Days Since Last'] = segment_stats['Avg Days Since Last'].apply(lambda x: f"{x:.0f}")

    st.dataframe(segment_stats, use_container_width=True, hide_index=True)

    # Regional analysis
    st.markdown("##")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌍 Customers by Region")
        region_data = filtered_customers['region'].value_counts().reset_index()
        region_data.columns = ['region', 'count']
        region_data = region_data.sort_values('count', ascending=True)

        fig = go.Figure(go.Bar(
            y=region_data['region'],
            x=region_data['count'],
            orientation='h',
            marker_color=COLORS['info'],
            text=[f"{x:,}" for x in region_data['count']],
            textposition='outside'
        ))

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="Number of Customers",
            yaxis_title="",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 💵 Avg LTV by Region")
        region_ltv = customer_data.groupby('region')['total_spent'].mean().reset_index()
        region_ltv = region_ltv.sort_values('total_spent', ascending=True)

        fig = go.Figure(go.Bar(
            y=region_ltv['region'],
            x=region_ltv['total_spent'],
            orientation='h',
            marker_color=COLORS['success'],
            text=[format_currency(x) for x in region_ltv['total_spent']],
            textposition='outside'
        ))

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="Avg LTV (R$)",
            yaxis_title="",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)


# ========================================================================================
# PAGE: PRODUCT PERFORMANCE
# ========================================================================================

def show_product_performance(category_summary, product_data):
    """Display product and category performance analysis"""

    st.title("🏆 Product Performance Analysis")
    st.markdown("Category and product-level insights")
    st.markdown("---")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    total_revenue = category_summary['category_total_revenue'].sum()
    total_categories = len(category_summary)
    total_products = len(product_data)
    avg_products_per_category = category_summary['products_in_category'].mean()

    with col1:
        st.metric("Total Revenue", format_currency(total_revenue))

    with col2:
        st.metric("Categories", total_categories)

    with col3:
        st.metric("Total Products", format_number(total_products))

    with col4:
        st.metric("Avg Products/Category", f"{avg_products_per_category:.0f}")

    st.markdown("##")

    # Category selector
    col1, col2 = st.columns([2, 8])
    with col1:
        selected_category = st.selectbox(
            "Filter by Category",
            ["All Categories"] + sorted(category_summary['product_category_name'].unique().tolist())
        )

    # Top categories performance
    st.markdown("### 🏅 Top 10 Categories by Revenue")

    top_10 = category_summary.head(10)

    fig = go.Figure(go.Bar(
        y=top_10['product_category_name'],
        x=top_10['category_total_revenue'],
        orientation='h',
        marker=dict(
            color=top_10['category_total_revenue'],
            colorscale='Blues',
            showscale=False
        ),
        text=[format_currency(x) for x in top_10['category_total_revenue']],
        textposition='outside'
    ))

    fig.update_layout(
        template=CHART_TEMPLATE,
        height=400,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="Revenue (R$)",
        yaxis_title="",
        yaxis=dict(autorange="reversed"),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("##")

    # Two column layout
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📦 Products per Category")
        top_products = category_summary.sort_values('products_in_category', ascending=False).head(10)

        fig = go.Figure(go.Bar(
            x=top_products['product_category_name'],
            y=top_products['products_in_category'],
            marker_color=COLORS['primary'],
            text=top_products['products_in_category'],
            textposition='outside'
        ))

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="",
            yaxis_title="Number of Products",
            showlegend=False,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### 🛒 Orders per Category")
        top_orders = category_summary.sort_values('category_total_orders', ascending=False).head(10)

        fig = go.Figure(go.Bar(
            x=top_orders['product_category_name'],
            y=top_orders['category_total_orders'],
            marker_color=COLORS['success'],
            text=top_orders['category_total_orders'],
            textposition='outside'
        ))

        fig.update_layout(
            template=CHART_TEMPLATE,
            height=300,
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis_title="",
            yaxis_title="Number of Orders",
            showlegend=False,
            xaxis_tickangle=-45
        )
        st.plotly_chart(fig, use_container_width=True)

    # Category comparison
    st.markdown("##")
    st.markdown("### 📊 Category Performance: Orders vs Revenue")

    fig = px.scatter(
        category_summary,
        x='category_total_orders',
        y='category_total_revenue',
        size='products_in_category',
        color='revenue_rank',
        hover_name='product_category_name',
        color_continuous_scale='Viridis',
        size_max=50
    )

    fig.update_layout(
        template=CHART_TEMPLATE,
        height=400,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis_title="Total Orders",
        yaxis_title="Total Revenue (R$)"
    )
    st.plotly_chart(fig, use_container_width=True)

    # Category details table
    st.markdown("##")
    st.markdown("### 📋 Category Performance Details")

    display_df = category_summary.copy()
    display_df['avg_order_value'] = display_df['category_total_revenue'] / display_df['category_total_orders']
    display_df = display_df.sort_values('revenue_rank')

    # Format columns
    display_df['revenue_rank'] = display_df['revenue_rank'].astype(int)
    display_df['category_total_revenue_fmt'] = display_df['category_total_revenue'].apply(lambda x: format_currency(x))
    display_df['avg_order_value_fmt'] = display_df['avg_order_value'].apply(lambda x: format_currency(x))

    display_df = display_df.rename(columns={
        'revenue_rank': 'Rank',
        'product_category_name': 'Category',
        'category_total_revenue_fmt': 'Total Revenue',
        'category_total_orders': 'Total Orders',
        'products_in_category': 'Products',
        'avg_order_value_fmt': 'Avg Order Value'
    })

    st.dataframe(
        display_df[['Rank', 'Category', 'Total Revenue', 'Total Orders', 'Products', 'Avg Order Value']],
        use_container_width=True,
        hide_index=True
    )

    # Product-level analysis (if category selected)
    if selected_category != "All Categories":
        st.markdown("##")
        st.markdown(f"### 🔍 Top 20 Products in: {selected_category}")

        category_products = product_data[product_data['product_category_name'] == selected_category].copy()
        category_products = category_products.nlargest(20, 'item_revenue')

        if len(category_products) > 0:
            fig = go.Figure(go.Bar(
                x=category_products['product_id'].astype(str),
                y=category_products['item_revenue'],
                marker_color=COLORS['primary'],
                text=[format_currency(x) for x in category_products['item_revenue']],
                textposition='outside'
            ))

            fig.update_layout(
                template=CHART_TEMPLATE,
                height=350,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis_title="Product ID",
                yaxis_title="Revenue (R$)",
                showlegend=False,
                xaxis_tickangle=-45
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No products found in this category.")


# ========================================================================================
# MAIN APPLICATION
# ========================================================================================

def main():
    """Main application entry point"""

    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    st.sidebar.markdown("---")

    page = st.sidebar.radio(
        "Go to",
        ["📊 Overview", "💰 Revenue Analytics", "👥 Customer Segments", "🏆 Product Performance"]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📖 About")
    st.sidebar.info(
        """
        **E-Commerce Analytics Dashboard**

        Interactive dashboard for analyzing Brazilian e-commerce data from Olist (2016-2018).

        **Pipeline:**
        - Bronze → Silver → Gold
        - Databricks + Delta Lake
        - Great Expectations QA
        """
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📊 Dataset Info")
    st.sidebar.success(
        """
        **Period:** 2016-09-04 to 2018-09-03

        **Records:**
        - ~99K Customers
        - ~99K Orders
        - ~113K Order Items
        - ~33K Products
        """
    )

    # Load data
    with st.spinner("Loading data..."):
        revenue_data, customer_data, category_summary, product_data = load_data()

    if revenue_data is None:
        st.error("Failed to load data. Please check your data sources.")
        return

    # Route to appropriate page
    if page == "📊 Overview":
        show_overview(revenue_data, customer_data, category_summary, product_data)
    elif page == "💰 Revenue Analytics":
        show_revenue_analytics(revenue_data)
    elif page == "👥 Customer Segments":
        show_customer_segments(customer_data)
    elif page == "🏆 Product Performance":
        show_product_performance(category_summary, product_data)

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        <div style='text-align: center; color: #64748b; font-size: 0.8rem;'>
            Built with Streamlit<br>
            E-Commerce Analytics Pipeline
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
