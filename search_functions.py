from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

"""
function takes title of a movie as input and returns titles of 10 most similar movies
:title: title of the movie searched
:cosine_sim: matrix of similarity scores
:indices: pandas Series with indices of movies as values and titles of movies as indices
"""


def get_recommendations(title, cosine_sim, titles):
    # Get the index of the movie searched
    idx = titles[titles == movie].index[0]
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies by similarity score and get 10 most similar ones
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[0:10]
    # Get indices of 10 most similar movies
    movie_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar movies
    return titles[movie_indices].values
