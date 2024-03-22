import streamlit as st
import pickle
import requests
import pandas as pd

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list=movies['title'].values

st.header("Movie Recommender System")
selectvalue =st.selectbox("Select movie from dropdown", movies_list)

# Define a function to display the last 5 years' top 3 highest-rated movies (yearwise)
def display_top_movies(movies):
    movies['release_date'] = pd.to_datetime(movies['release_date'])
    current_year = pd.Timestamp.now().year
    last_5_years_movies = movies[movies['release_date'].dt.year.between(current_year - 4, current_year)]
    top_movies = last_5_years_movies.groupby(last_5_years_movies['release_date'].dt.year).apply(lambda x: x.nlargest(3, 'vote_average')).reset_index(drop=True)
    top_movies['release_date'] = pd.to_datetime(top_movies['release_date'])
    # Extract the year
    top_movies['year'] = top_movies['release_date'].dt.year
    st.title('Top 3 Highest-Rated Movies of Last 5 Years (Yearwise)')
    st.dataframe(top_movies[['year', 'title', 'vote_average']],hide_index=True)

# Define a function to display the top 5 directors with the highest average ratings
def display_top_directors(movies):
    director_avg_ratings = movies.groupby('title')['vote_average'].mean()
    top_directors = director_avg_ratings.sort_values(ascending=False)
    top_5_directors = top_directors.head(5)
    st.title('Top 5 Directors movie with the Highest Average Ratings')
    st.dataframe(top_5_directors)

# Define a function to display the top 2 highest-rated movies for each of the top 5 genres
def display_top_movies_by_genre(movies):
    genre_avg_ratings = movies.groupby('genre')['vote_average'].mean()
    top_genres = genre_avg_ratings.sort_values(ascending=False)
    top_5_genres = top_genres.head(5)
    top_movies_by_genre = {}
    for genre in top_5_genres.index:
        genre_movies = movies[~movies['genre'].isna()]
        genre_movies = genre_movies[genre_movies['genre'].str.contains(genre)]
        top_movies = genre_movies.nlargest(2, 'vote_average')
        top_movies_by_genre[genre] = top_movies[['title', 'vote_average']]
    for genre, top_movies in top_movies_by_genre.items():
        st.subheader(f"Top 2 Highest-Rated Movies in {genre}:")
        st.dataframe(top_movies, hide_index = 'True')


def recommend(movie):
    index=movies[movies['title']==movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector:vector[1])
    recommend_movie=[]
    recommend_poster=[]
    for i in distance[1:6]:
        movies_id =movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
    return recommend_movie, recommend_poster



if st.button("Show Recommend"):
    movie_name, movie_poster = recommend(selectvalue)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.text(movie_name[0])

    with col2:
        st.text(movie_name[1])

    with col3:
        st.text(movie_name[2])

    with col4:
        st.text(movie_name[3])

    with col5:
        st.text(movie_name[4])


movies_data = pd.read_csv('dataset.csv')
display_top_movies(movies_data)
display_top_directors(movies_data)
display_top_movies_by_genre(movies_data)

