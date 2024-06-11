import streamlit as st
import pandas as pd
import altair as alt

# Set up Streamlit app layout
st.set_page_config(layout='wide', page_title='USA Real Estate Dashboard', initial_sidebar_state='expanded', page_icon=':house:')

# Sidebar configuration
st.sidebar.header('USA Real Estate Dashboard')

# Load the dataset
data = pd.read_csv('realtor-data.zip.csv')
data['price'] = pd.to_numeric(data['price'], errors='coerce')
data['bed'] = pd.to_numeric(data['bed'], errors='coerce')
data['bath'] = pd.to_numeric(data['bath'], errors='coerce')
data['state'] = data['state'].astype(str)
data['city'] = data['city'].fillna('Unknown')

# Handle missing values for prices, beds, and baths
data = data.dropna(subset=['price', 'bed', 'bath'])

# Remove unrealistic prices, beds, and baths
data = data[(data['price'] > 0) & (data['price'] < 1e8)]
data = data[(data['bed'] > 0) & (data['bed'] < 10)]
data = data[(data['bath'] >= 0) & (data['bath'] < 10)]

# Sidebar filters
st.sidebar.subheader('Filter by Price Range')
min_price = st.sidebar.slider('Minimum Price', int(data['price'].min()), int(data['price'].max()), int(data['price'].min()))
max_price = st.sidebar.slider('Maximum Price', int(data['price'].min()), int(data['price'].max()), int(data['price'].max()))

# Filter data based on price range
filtered_data = data[(data['price'] >= min_price) & (data['price'] <= max_price)]

# Sidebar filters for states
st.sidebar.subheader('Filter by State')
states = sorted(filtered_data['state'].dropna().unique())
selected_states = st.sidebar.multiselect('Select State(s)', states, default=states)

# Filter data based on selected states
filtered_data = filtered_data[filtered_data['state'].isin(selected_states)]

# Sample data to reduce size
if len(filtered_data) > 10000:
    filtered_data = filtered_data.sample(n=10000, random_state=42)

# Main layout
st.title(':house: USA Real Estate Dashboard')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Key Metrics
st.markdown('### Key Metrics')
total_properties = filtered_data.shape[0]
average_price = filtered_data['price'].mean()
median_price = filtered_data['price'].median()
total_listings = filtered_data['price'].count()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Properties", total_properties)
col2.metric("Average Price ($)", f"{average_price:,.2f}")
col3.metric("Median Price ($)", f"{median_price:,.2f}")
col4.metric("Total Listings", total_listings)

# Distribution of Property Prices as Line Chart
st.header("Distribution of Property Prices")
price_distribution_chart = alt.Chart(filtered_data).mark_line().encode(
    x=alt.X('price:Q', bin=alt.Bin(maxbins=100), title='Price ($)'),
    y=alt.Y('count():Q', title='Number of Properties')
).properties(
    width=800,
    height=400
)
st.altair_chart(price_distribution_chart, use_container_width=True)

# Property Prices by State and City
st.header("Property Prices by State and City")
avg_price_data = filtered_data.groupby(['state', 'city']).agg({
    'price': 'mean',
    'bed': 'mean',
    'bath': 'mean'
}).reset_index()

geo_distribution_chart = alt.Chart(avg_price_data).mark_circle(size=60).encode(
    x=alt.X('state:N', title='State'),
    y=alt.Y('city:N', title='City', sort=alt.EncodingSortField(field="price", op="mean", order="descending")),
    size=alt.Size('price:Q', scale=alt.Scale(range=[10, 1000]), title='Average Price ($)'),
    color='state:N',
    tooltip=[
        'state', 'city', 
        alt.Tooltip('price:Q', title='Avg. Price'),
        alt.Tooltip('bed:Q', title='Avg. Beds', format=',.0f'),
        alt.Tooltip('bath:Q', title='Avg. Baths', format=',.0f')
    ]
).properties(
    width=800,
    height=400
).interactive()

st.altair_chart(geo_distribution_chart, use_container_width=True)

# Top States by Listings
st.header("Top States by Listings")
top_states_chart = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X('count(price):Q', title='Number of Listings'),
    y=alt.Y('state:N', sort='-x', title='State')
).properties(
    width=800,
    height=400
)
st.altair_chart(top_states_chart, use_container_width=True)
