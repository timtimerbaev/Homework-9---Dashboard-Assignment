import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set up Streamlit app layout
st.set_page_config(layout='wide', page_title= 'E Commerce Dashboard', initial_sidebar_state='expanded', page_icon=':clipboard:')

# Sidebar configuration
st.sidebar.header('E-Commerce Dashboard')
st.sidebar.subheader('Filter Data')

# Load the dataset
data = pd.read_csv('data.csv', encoding='latin1')
data['InvoiceDate'] = pd.to_datetime(data['InvoiceDate'])
data['TotalPrice'] = data['Quantity'] * data['UnitPrice']

st.title(' :clipboard: E Commerce Dashboard')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

st.sidebar.markdown('### KPIs')
total_sales_revenue = data['TotalPrice'].sum()
average_order_value = total_sales_revenue / data['InvoiceNo'].nunique()
total_orders = data['InvoiceNo'].nunique()
total_customers = data['CustomerID'].nunique()

st.sidebar.metric(label="Total Sales Revenue ($)", value=f"{total_sales_revenue:,.2f}")
st.sidebar.metric(label="Average Order Value ($)", value=f"{average_order_value:,.2f}")
st.sidebar.metric(label="Total Number of Orders", value=total_orders)
st.sidebar.metric(label="Total Number of Customers", value=total_customers)

# Filter options
st.sidebar.subheader('Sales Revenue Over Time')
time_filter = st.sidebar.radio('Select Time Period', ('Monthly', 'Daily'))

st.sidebar.subheader('Top Products')
num_products = st.sidebar.slider('Select number of top products to display', 5, 20, 10)

st.sidebar.subheader('Sales by Country')
num_countries = st.sidebar.slider('Select number of top countries to display', 5, 20, 10)

# Main layout
st.title("E-Commerce Store Dashboard")

# Row A - Metrics
st.markdown('### Key Metrics')
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales Revenue ($)", f"{total_sales_revenue:,.2f}")
col2.metric("Average Order Value ($)", f"{average_order_value:,.2f}")
col3.metric("Total Number of Orders", total_orders)
col4.metric("Total Number of Customers", total_customers)

# Row B - Sales Revenue Over Time
st.markdown('### Sales Revenue Over Time')
if time_filter == 'Monthly':
    sales_over_time = data.resample('M', on='InvoiceDate').sum()['TotalPrice'].reset_index()
else:
    sales_over_time = data.resample('D', on='InvoiceDate').sum()['TotalPrice'].reset_index()

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='InvoiceDate', y='TotalPrice', data=sales_over_time, ax=ax)
ax.set_title('Sales Revenue Over Time')
ax.set_xlabel('Date')
ax.set_ylabel('Total Revenue ($)')
st.pyplot(fig)

# Row C - Top Selling Products
st.markdown('### Top Selling Products')
top_products = data.groupby('StockCode').agg({'Quantity': 'sum'}).reset_index().sort_values(by='Quantity', ascending=False).head(num_products)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Quantity', y='StockCode', data=top_products, ax=ax)
ax.set_title('Top Selling Products')
ax.set_xlabel('Quantity Sold')
ax.set_ylabel('Product Code')
st.pyplot(fig)

# Row D - Sales by Country
st.markdown('### Sales by Country')
sales_by_country = data.groupby('Country').agg({'TotalPrice': 'sum'}).reset_index().sort_values(by='TotalPrice', ascending=False).head(num_countries)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='TotalPrice', y='Country', data=sales_by_country, ax=ax)
ax.set_title('Sales by Country')
ax.set_xlabel('Total Revenue ($)')
ax.set_ylabel('Country')
st.pyplot(fig)