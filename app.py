from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# pre-calculated dictionary with top 10 similar movies for each movie in database
d = np.load('movie_dict.npy', allow_pickle='TRUE').item()

# list of strings with data for each movie including
metadata = pd.read_csv('metadata.csv', squeeze=True)

# list of movie titles
titles = pd.read_csv('titles.csv', squeeze=True)

"""
search by keywords
It iteratively creates matrix of token counts for keyword-string and 
metadata for each movie. Then cosine similarity for those 2 vectors 
is calculated. Top 10 scores is stored in dictionary.

:keywords: string with given keywords separated by comma
e.g. 'war, James McAvoy, Keira Knightley, drama'
:metadata: list of strings with data for each movie including 
actors (each lowercased and combined into one word), directors (same), genre, keywords
:titles: list of movie titles
"""


def search_keywords(keywords, metadata, titles):
    top = {}
    # Unification of keywords: all words in lower case, all names combined into one word
    keywords = ' '.join(
        (map(lambda x: x.replace(' ', '').lower(), keywords.split(','))))
    for i in range(len(metadata)):
        # Matrix of token counts
        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform([keywords, metadata[i]])
        # Cosine similarity is calculated, result is stored in [1,0] cell of whole matrix
        result = cosine_similarity(count_matrix, count_matrix)[1, 0]

        if len(top) < 10:
            top[result] = i
        else:
            # Compare similarity score is stored as keys, movie index as value
            if result > min(top.keys()):
                del top[min(top.keys())]
                top[result] = i
    # Sort by count value
    top = [top[x] for x in sorted(top, reverse=True)]
    return titles[top].values


app = Flask(__name__)


@app.route('/')
def main():
    return render_template('app.html')


@app.route('/send', methods=['POST'])
def send(sum=sum):
    if request.method == 'POST':
        movie = request.form['movie']

        # Ask user for search type
        operation = request.form['operation']

        # If user uses search for similar movies
        if operation == 'movie':

            # If no title typed
            if len(movie) == 0:
                result = ['no movie']

            # Check if movie is presented in the database
            else:
                if movie in d.keys():
                    result = d[movie]
                else:
                    result = ['empty']

            return render_template('app.html', result=result)

        # If user uses search by keywords
        elif operation == 'keywords':

            # If no keywords typed
            if len(movie) == 0:
                result = ['no keywords']
            else:
                result = search_keywords(movie, metadata, titles)
            return render_template('app.html', result=result)


if __name__ == '__main__':
    app.debug = True
    app.run()
