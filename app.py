from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from scipy import spatial
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy import spatial
from search_functions import get_recommendations

"""
:metadata: pandas Series with metadata for each movie including keywords, genres, country of production, directors and actors
:titles: pandas Seriies with title for each movie
"""
metadata = pd.read_csv('metadata.csv', squeeze=True)
titles = pd.read_csv('titles.csv', squeeze=True)
cosine_sim_path = 'cosine_sim2.txt'

# Count number of word occurences in metadata string for every movie
#count = CountVectorizer(stop_words='english')
#count_matrix = count.fit_transform(metadata)
# Calculate cosine similarity to know how close metadata-vectors in word space to each other
#cosine_sim = cosine_similarity(count_matrix, count_matrix)

# Create an instance of the Flask class for our web app
app = Flask(__name__)


@app.route('/')
def main():
    return render_template('app.html')


@app.route('/send', methods=['POST'])
def send(sum=sum):
    if request.method == 'POST':
        movie = request.form['movie']
        # Check if movie is presented in the database
        if movie in titles.values:
            result = get_recommendations(movie, titles, cosine_sim_path)
        else:
            result = 'We dont have this movie in database'

        return render_template('app.html', result=result)


if __name__ == '__main__':
    app.debug = True
    app.run()
