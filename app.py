import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Set page title and icon
st.set_page_config(page_title="Movie Recommender", page_icon="🎬")

# App title
st.title("🎬 Movie Recommendation System")

# Info
st.markdown("""
Welcome to the movie recommender!  
Enter a movie name below to get similar movie suggestions.  
Try movies like **Avatar**, **The Dark Knight**, etc.
""")

# Load dataset
movies_df = pd.read_csv("movie_dataset.csv")  # Make sure this file is in the same folder

# Replace missing descriptions with empty string
movies_df['description'] = movies_df['description'].fillna('')

# Convert descriptions to feature vectors
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(movies_df['description'])

# Compute similarity scores
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# Recommendation function
def recommend_movie(title):
    try:
        idx = movies_df[movies_df['title'].str.lower() == title.lower()].index[0]
    except IndexError:
        return ["❌ Movie not found. Please try another title."]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    return movies_df['title'].iloc[movie_indices].tolist()

# Input box
movie_input = st.text_input("Enter a Movie Title:")

# Show recommendations
if movie_input:
    st.subheader("🎯 Recommended Movies:")
    for movie in recommend_movie(movie_input):
        st.write("🎥", movie)
