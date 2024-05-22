import pandas as pd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Sidebar filters
st.sidebar.subheader('Filter by Rating')
min_rating = st.sidebar.slider('Minimum Rating', 1, 5, 1)
max_rating = st.sidebar.slider('Maximum Rating', 1, 5, 5)

# Filter data based on rating
filtered_data = data[(data['Rating'] >= min_rating) & (data['Rating'] <= max_rating)]

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

# Genre Distribution
st.markdown('### Genre Distribution')
genre_counts = movies_df['Genres'].str.get_dummies('|').sum().sort_values(ascending=False).reset_index()
genre_counts.columns = ['Genre', 'Count']

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Count', y='Genre', data=genre_counts, ax=ax)
ax.set_title('Genre Distribution')
ax.set_xlabel('Number of Movies')
ax.set_ylabel('Genre')
st.pyplot(fig)

# Top Rated Movies
st.markdown('### Top Rated Movies')
top_rated_movies = filtered_data.groupby('Title').agg({'Rating': 'mean', 'MovieID': 'count'}).reset_index().rename(columns={'MovieID': 'RatingCount'})
top_rated_movies = top_rated_movies[top_rated_movies['RatingCount'] > 10].sort_values(by='Rating', ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Rating', y='Title', data=top_rated_movies, ax=ax)
ax.set_title('Top Rated Movies')
ax.set_xlabel('Average Rating')
ax.set_ylabel('Movie Title')
st.pyplot(fig)

# Ratings by Age Group
st.markdown('### Ratings by Age Group')
age_group_ratings = filtered_data.groupby('Age').agg({'Rating': 'mean', 'UserID': 'count'}).reset_index().rename(columns={'UserID': 'RatingCount'})

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Age', y='Rating', data=age_group_ratings, ax=ax)
ax.set_title('Average Rating by Age Group')
ax.set_xlabel('Age Group')
ax.set_ylabel('Average Rating')
st.pyplot(fig)