import streamlit as st
import pandas as pd
import altair as alt

# Set up Streamlit app layout
st.set_page_config(layout='wide', page_title='Sustainable Energy Dashboard', initial_sidebar_state='expanded', page_icon=':bar_chart:')

# Sidebar configuration
st.sidebar.header('Sustainable Energy Dashboard')

# Load the dataset
data = pd.read_csv('global-data-on-sustainable-energy.csv', encoding='latin1')
data['Year'] = pd.to_datetime(data['Year'], format='%Y')

# Sidebar filters
st.sidebar.subheader('Filter by Year')
min_year = st.sidebar.slider('Start Year', int(data['Year'].dt.year.min()), int(data['Year'].dt.year.max()), int(data['Year'].dt.year.min()))
max_year = st.sidebar.slider('End Year', int(data['Year'].dt.year.min()), int(data['Year'].dt.year.max()), int(data['Year'].dt.year.max()))

# Filter data based on year
filtered_data = data[(data['Year'].dt.year >= min_year) & (data['Year'].dt.year <= max_year)]

# Sidebar filters for countries
st.sidebar.subheader('Filter by Country')
countries = sorted(filtered_data['Entity'].unique())
selected_countries = st.sidebar.multiselect('Select Country(ies)', countries, default=countries)

# Filter data based on selected countries
filtered_data = filtered_data[filtered_data['Entity'].isin(selected_countries)]

# Main layout
st.title(':bar_chart: Sustainable Energy Dashboard')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Key Metrics
st.markdown('### Key Metrics')
total_countries = filtered_data['Entity'].nunique()
avg_access_electricity = filtered_data['Access to electricity (% of population)'].mean()
avg_access_clean_fuels = filtered_data['Access to clean fuels for cooking'].mean()
total_renewable_capacity = filtered_data['Renewable-electricity-generating-capacity-per-capita'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Total Countries", total_countries)
col2.metric("Avg. Access to Electricity (%)", f"{avg_access_electricity:.2f}")
col3.metric("Avg. Access to Clean Fuels (%)", f"{avg_access_clean_fuels:.2f}")

# Sales Revenue Over Time
st.header("Access to Electricity Over Time")
electricity_chart = alt.Chart(filtered_data).mark_line().encode(
    x=alt.X('Year:T', title='Year'),
    y=alt.Y('mean(Access to electricity (% of population)):Q', title='Access to Electricity (%)'),
    color='Entity:N'
).properties(
    width=800,
    height=400
)
st.altair_chart(electricity_chart, use_container_width=True)

# Access to Clean Fuels Over Time
st.header("Access to Clean Fuels Over Time")
clean_fuels_chart = alt.Chart(filtered_data).mark_line().encode(
    x=alt.X('Year:T', title='Year'),
    y=alt.Y('mean(Access to clean fuels for cooking):Q', title='Access to Clean Fuels (%)'),
    color='Entity:N'
).properties(
    width=800,
    height=400
)
st.altair_chart(clean_fuels_chart, use_container_width=True)

# Renewable Electricity Generation by Country
st.header("Renewable Electricity Generation by Country")
renewable_chart = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X('sum(Renewable-electricity-generating-capacity-per-capita):Q', title='Renewable Capacity (Watts per Capita)'),
    y=alt.Y('Entity:N', sort='-x', title='Country'),
    tooltip=['Entity', 'sum(Renewable-electricity-generating-capacity-per-capita):Q']
).properties(
    width=800,
    height=400
)
st.altair_chart(renewable_chart, use_container_width=True)

# Financial Aid Distribution
st.header("Financial Aid Distribution by Country")
financial_aid_chart = alt.Chart(filtered_data).mark_bar().encode(
    x=alt.X('sum(Financial flows to developing countries (US $)):Q', title='Financial Aid (USD)'),
    y=alt.Y('Entity:N', sort='-x', title='Country'),
    tooltip=['Entity', 'sum(Financial flows to developing countries (US $)):Q']
).properties(
    width=800,
    height=400
)
st.altair_chart(financial_aid_chart, use_container_width=True)