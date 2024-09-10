import streamlit as st
import pickle
import pandas as pd
import requests

# Recommendation function
def recommend(drama_name):
    drama_index = drama[drama['Name'] == drama_name].index[0]
    distances = similarity[drama_index]
    drama_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in drama_list:
        drama_id = drama.iloc[i[0]].Id
        recommended_movies.append(drama.iloc[i[0]].Name)
        recommended_posters.append(fetch_poster(drama_id))
    return recommended_movies, recommended_posters

# Function to fetch poster
def fetch_poster(drama_id):
    poster_url = poster.loc[drama_id, 'Img_url']
    return poster_url

# Load data
poster = pd.read_pickle('poster_data.pkl')
drama_list = pickle.load(open('drama_dict.pkl', 'rb'))
drama = pd.DataFrame(drama_list)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title("KDrama Recommendation System ⭐️")

selected_drama_name = st.selectbox(
    "Select Drama Name",
    drama['Name'].values
)

if st.button('Recommend'):
    recommendations, posters = recommend(selected_drama_name)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.write(recommendations[idx])
            st.image(posters[idx])
