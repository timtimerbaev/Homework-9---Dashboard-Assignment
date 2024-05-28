import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up Streamlit app layout
st.set_page_config(layout='wide', page_title='E-Commerce Dashboard', initial_sidebar_state='expanded', page_icon=':clipboard:')

# Sidebar configuration
st.sidebar.header('E-Commerce Dashboard')

# Load the dataset
data = pd.read_csv('data.csv', encoding='latin1')
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
data['TotalPrice'] = data['Quantity'] * data['UnitPrice']

st.title(':clipboard: E-Commerce Dashboard')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

total_sales_revenue = data['TotalPrice'].sum()
average_order_value = total_sales_revenue / data['InvoiceNo'].nunique()
total_orders = data['InvoiceNo'].nunique()
total_customers = data['CustomerID'].nunique()

# Filter options
st.sidebar.subheader('Sales Revenue Over Time')
time_filter = st.sidebar.radio('Select Time Period', ('Monthly', 'Daily'))

st.sidebar.subheader('Top Products')
num_products = st.sidebar.slider('Select number of top products to display', 5, 20, 10)

st.sidebar.subheader('Sales by Country')
num_countries = st.sidebar.slider('Select number of top countries to display', 5, 20, 10)

# Main layout

# Row A - Metrics
st.markdown('### Key Metrics')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales Revenue ($)", f"{total_sales_revenue:,.2f}")
col2.metric("Average Order Value ($)", f"{average_order_value:,.2f}")
col3.metric("Total Number of Orders", total_orders)
col4.metric("Total Number of Customers", total_customers)

# Create a container for the plots
with st.container():
    # Row B - Sales Revenue Over Time
    st.markdown('### Sales Revenue Over Time')
    if time_filter == 'Monthly':
        sales_over_time = data.resample('M', on='InvoiceDate').sum()['TotalPrice'].reset_index()
    else:
        sales_over_time = data.resample('D', on='InvoiceDate').sum()['TotalPrice'].reset_index()

    fig1, ax1 = plt.subplots(figsize=(12, 4))
    sns.lineplot(x='InvoiceDate', y='TotalPrice', data=sales_over_time, ax=ax1)
    ax1.set_title('Sales Revenue Over Time')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Total Revenue ($)')
    st.pyplot(fig1)

    # Row C - Top Selling Products and Sales by Country side by side
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Top Selling Products')
        top_products = data.groupby('StockCode').agg({'Quantity': 'sum'}).reset_index().sort_values(by='Quantity', ascending=False).head(num_products)

        fig2, ax2 = plt.subplots(figsize=(12, 4))
        sns.barplot(x='Quantity', y='StockCode', data=top_products, ax=ax2)
        ax2.set_title('Top Selling Products')
        ax2.set_xlabel('Quantity Sold')
        ax2.set_ylabel('Product Code')
        st.pyplot(fig2)

    with col2:
        st.markdown('### Sales by Country')
        sales_by_country = data.groupby('Country').agg({'TotalPrice': 'sum'}).reset_index().sort_values(by='TotalPrice', ascending=False).head(num_countries)

        fig3, ax3 = plt.subplots(figsize=(12, 4))
        sns.barplot(x='TotalPrice', y='Country', data=sales_by_country, ax=ax3)
        ax3.set_title('Sales by Country')
        ax3.set_xlabel('Total Revenue ($)')
        ax3.set_ylabel('Country')
        st.pyplot(fig3)
