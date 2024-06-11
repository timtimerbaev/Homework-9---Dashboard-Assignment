import streamlit as st
import pandas as pd
import altair as alt

# Set up Streamlit app layout
st.set_page_config(layout='wide', page_title='Climate Change Dashboard', initial_sidebar_state='expanded', page_icon=':earth_americas:')

# Sidebar configuration
st.sidebar.header('Climate Change Dashboard')

# Importing the data
data = pd.read_csv('GlobalLandTemperaturesByMajorCity.csv')

# Preprocess the data
data['dt'] = pd.to_datetime(data['dt'])
data['year'] = data['dt'].dt.year
data['month'] = data['dt'].dt.month
data['Anomaly'] = data['AverageTemperature'] - data['AverageTemperature'].mean()

# Sidebar filters
st.sidebar.subheader('Filter by Year')
min_year = st.sidebar.slider('Start Year', int(data['year'].min()), int(data['year'].max()), int(data['year'].min()))
max_year = st.sidebar.slider('End Year', int(data['year'].min()), int(data['year'].max()), int(data['year'].max()))

# Filter data based on year
filtered_data = data[(data['year'] >= min_year) & (data['year'] <= max_year)]

# Sidebar filters for countries
st.sidebar.subheader('Filter by Country')
countries = sorted(data['Country'].unique())
selected_countries = st.sidebar.multiselect('Select Country(ies)', countries, default=countries)

# Filter data based on selected countries
filtered_data = filtered_data[filtered_data['Country'].isin(selected_countries)]

# Main layout
st.title(':earth_americas: Climate Change Dashboard')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Key Metrics
st.markdown('### Key Metrics')
total_cities = filtered_data['City'].nunique()
total_countries = filtered_data['Country'].nunique()
total_records = filtered_data.shape[0]

col1, col2, col3 = st.columns(3)
col1.metric("Total Cities", total_cities)
col2.metric("Total Countries", total_countries)
col3.metric("Total Records", total_records)

# Create a container for the charts
with st.container():
    # Line Chart for Temperature Trends
    st.header("Global Temperature Trends")
    line_chart = alt.Chart(filtered_data).mark_line().encode(
        x=alt.X('year:O', title='Year', axis=alt.Axis(format='d')),
        y='mean(AverageTemperature):Q'
    ).properties(
        title='Average Global Temperature Over Time',
        width=800,
        height=400
    )
    st.altair_chart(line_chart, use_container_width=True)

    # Bar Chart for Monthly Temperature Averages
    st.header("Monthly Temperature Averages")
    monthly_avg = filtered_data.groupby('month')['AverageTemperature'].mean().reset_index()
    bar_chart = alt.Chart(monthly_avg).mark_bar().encode(
        x=alt.X('month:O', title='Month'),
        y='AverageTemperature:Q'
    ).properties(
        title='Average Temperature by Month',
        width=800,
        height=400
    )
    st.altair_chart(bar_chart, use_container_width=True)

    # Scatter Plot for Temperature Anomalies
    st.header("Temperature Anomalies")
    scatter_plot = alt.Chart(filtered_data).mark_circle(size=60).encode(
        x=alt.X('year:O', title='Year', axis=alt.Axis(format='d')),
        y='Anomaly:Q',
        color='Country:N',
        tooltip=['year:T', 'Anomaly:Q', 'City:N', 'Country:N']
    ).properties(
        title='Temperature Anomalies Over Time',
        width=800,
        height=400
    )
    st.altair_chart(scatter_plot, use_container_width=True)

    # Pie Chart for Country-wise Temperature Distribution
    st.header("Country-wise Temperature Distribution")
    country_avg = filtered_data.groupby('Country')['AverageTemperature'].mean().reset_index()
    pie_chart = alt.Chart(country_avg).mark_arc().encode(
        theta=alt.Theta(field="AverageTemperature", type="quantitative"),
        color=alt.Color(field="Country", type="nominal"),
        tooltip=['Country', 'AverageTemperature']
    ).properties(
        title='Average Temperature by Country',
        width=400,
        height=400
    )
    st.altair_chart(pie_chart, use_container_width=True)

    # Box Plot for Temperature Variability
    st.header("Temperature Variability by City")
    box_plot = alt.Chart(filtered_data).mark_boxplot().encode(
        x='City:N',
        y='AverageTemperature:Q',
        color='City:N',
        tooltip=['City', 'AverageTemperature']
    ).properties(
        title='Temperature Variability by City',
        width=800,
        height=400
    )
    st.altair_chart(box_plot, use_container_width=True)