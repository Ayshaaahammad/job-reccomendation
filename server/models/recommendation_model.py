import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def preprocess_data():
    df = pd.read_csv('data/jobs.csv')
    df['skills'] = df['skills'].str.lower().str.replace(',', ' ')
    df['description'] = df['description'].str.lower()
    df['location'] = df['location'].str.lower()
    return df

def get_recommendations(user_data):
    df = preprocess_data()
    
    # Process user input
    user_skills = user_data.get('skills', '').lower().replace(',', ' ')
    user_experience = float(user_data.get('experience', 0))
    user_location = user_data.get('location', '').lower()
    
    # Combine job features
    df['combined_features'] = df['skills'] + ' ' + df['description']
    
    # Create TF-IDF vectors
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['combined_features'])
    
    # Create user profile vector
    user_profile = user_skills + ' ' + user_location
    user_vector = tfidf.transform([user_profile])
    
    # Calculate similarity scores
    cosine_sim = cosine_similarity(user_vector, tfidf_matrix).flatten()
    
    # Filter by experience and location
    experience_mask = (df['min_experience'] <= user_experience) & (user_experience <= df['max_experience'])
    if user_location:
        location_mask = df['location'].str.contains(user_location, case=False, na=False)
    else:
        location_mask = pd.Series([True] * len(df))
    
    # Combine filters
    final_mask = experience_mask & location_mask
    filtered_indices = np.where(final_mask)[0]
    
    # Get top recommendations
    if len(filtered_indices) > 0:
        filtered_scores = cosine_sim[filtered_indices]
        top_indices = filtered_indices[filtered_scores.argsort()[-5:][::-1]]
    else:
        top_indices = cosine_sim.argsort()[-5:][::-1]
    
    # Prepare recommendations
    recommendations = df.iloc[top_indices][['title', 'company', 'location', 'description', 'skills']].to_dict('records')
    return recommendations