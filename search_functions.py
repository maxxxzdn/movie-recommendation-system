from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

"""
function takes title of a movie as input and returns titles of 10 most similar movies
:title: title of the movie searched
:cosine_sim_path: path to file where cosine_sim matrix is stored
:indices: pandas Series with indices of movies as values and titles of movies as indices
"""

def get_recommendations(title, titles, cosine_sim_path):
    # Get the index of the movie searched
    idx = titles[titles == title].index[0]
    # Get the idx string from file and convert it to array 
    with open(cosine_sim_path) as f:
        for position, line in enumerate(f):
            if position == idx:
                break
    line = np.fromstring(line, np.float64, sep = ' ')
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(line))
    # Sort the movies by similarity score and get 10 most similar ones
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:11]
    # Get indices of 10 most similar movies
    movie_indices = [i[0] for i in sim_scores]
    # Return the top 10 most similar movies
    return titles[movie_indices].values