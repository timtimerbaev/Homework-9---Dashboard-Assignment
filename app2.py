import streamlit as st
import pandas as pd
import altair as alt

# Set up Streamlit app layout
st.set_page_config(layout='wide', page_title='Movies Dashboard', initial_sidebar_state='expanded', page_icon=':clipboard:')

# Sidebar configuration
st.sidebar.header('Movies Dashboard')

# Importing the data
movies_df = pd.read_csv('movies.dat', sep='::', header=None, names=['MovieID', 'Title', 'Genres'], engine='python', encoding='latin1')
ratings_df = pd.read_csv('ratings.dat', sep='::', header=None, names=['UserID', 'MovieID', 'Rating', 'Timestamp'], engine='python', encoding='latin1')
users_df = pd.read_csv('users.dat', sep='::', header=None, names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'], engine='python', encoding='latin1')

# Merge dataframes
data = pd.merge(pd.merge(movies_df, ratings_df, on='MovieID'), users_df, on='UserID')

# Create age groups
age_bins = [0, 18, 25, 35, 45, 50, 56, 60, 100]
age_labels = ['0-18', '19-25', '26-35', '36-45', '46-50', '51-56', '57-60', '60+']
data['AgeGroup'] = pd.cut(data['Age'], bins=age_bins, labels=age_labels, right=False)

# Sidebar filters
st.sidebar.subheader('Filter by Rating')
min_rating = st.sidebar.slider('Minimum Rating', 1, 5, 1)
max_rating = st.sidebar.slider('Maximum Rating', 1, 5, 5)

# Filter data based on rating
filtered_data = data[(data['Rating'] >= min_rating) & (data['Rating'] <= max_rating)]

# Genre filter
st.sidebar.subheader('Filter by Genre')
all_genres = sorted(set(genre for sublist in movies_df['Genres'].str.split('|') for genre in sublist))
selected_genre = st.sidebar.multiselect('Select Genre(s)', all_genres, default=all_genres)

# Filter data based on genre
def genre_filter(row):
    genres = row['Genres'].split('|')
    return any(genre in genres for genre in selected_genre)

filtered_data = filtered_data[filtered_data.apply(genre_filter, axis=1)]

# Main layout
st.title(':clipboard: Movies Dashboard')
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)

# Key Metrics
st.markdown('### Key Metrics')
total_movies = movies_df['MovieID'].nunique()
total_users = users_df['UserID'].nunique()
total_ratings = ratings_df['Rating'].count()
average_rating = ratings_df['Rating'].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Movies", total_movies)
col2.metric("Total Users", total_users)
col3.metric("Total Ratings", total_ratings)
col4.metric("Average Rating", f"{average_rating:.2f}")

# Create a container for the charts
with st.container():
    # Genre Distribution

    genre_counts = movies_df['Genres'].str.get_dummies('|').sum().sort_values(ascending=False).reset_index()
    genre_counts.columns = ['Genre', 'Count']
    
    genre_chart = alt.Chart(genre_counts).mark_bar().encode(
        x=alt.X('Count:Q', title='Number of Movies'),
        y=alt.Y('Genre:N', sort='-x')
    ).properties(
        title='Genre Distribution',
        width=400,
        height=300
    )
    
    # Top Rated Movies

    top_rated_movies = filtered_data.groupby('Title').agg({'Rating': 'mean', 'MovieID': 'count'}).reset_index().rename(columns={'MovieID': 'RatingCount'})
    top_rated_movies = top_rated_movies[top_rated_movies['RatingCount'] > 10].sort_values(by='Rating', ascending=False).head(10)
    
    top_rated_chart = alt.Chart(top_rated_movies).mark_bar().encode(
        x=alt.X('Rating:Q', title='Average Rating'),
        y=alt.Y('Title:N', sort='-x')
    ).properties(
        title='Top Rated Movies',
        width=400,
        height=300
    )
    
    # Ratings by Age Group

    age_group_ratings = filtered_data.groupby('AgeGroup').agg({'Rating': 'mean', 'UserID': 'count'}).reset_index().rename(columns={'UserID': 'RatingCount'})
    
    age_group_chart = alt.Chart(age_group_ratings).mark_bar().encode(
        x=alt.X('AgeGroup:N', title='Age Group'),
        y=alt.Y('Rating:Q', title='Average Rating')
    ).properties(
        title='Average Rating by Age Group',
        width=400,
        height=300
    )

    # Place the charts side by side
    left_col, right_col = st.columns(2)
    
    with left_col:
        st.altair_chart(genre_chart, use_container_width=True)
        st.altair_chart(age_group_chart, use_container_width=True)
        
    with right_col:
        st.altair_chart(top_rated_chart, use_container_width=True)
