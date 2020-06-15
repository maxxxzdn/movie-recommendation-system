from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def search_keywords(keywords, metadata, titles):
    top = {}
    keywords = ' '.join((map(lambda x: x.replace(' ', '').lower(), keywords.split(','))))
    for i in range(len(metadata)):
        count = CountVectorizer(stop_words='english')
        count_matrix = count.fit_transform([keywords, metadata[i]])
        result = cosine_similarity(count_matrix, count_matrix)[1,0]
        if len(top) < 10:
            top[result] = i
        else: 
            if result > min(top.keys()):
                del top[min(top.keys())]
                top[result] = i
    top = [top[x] for x in sorted(top, reverse=True)]
    return titles[top].values  

d = np.load('movie_dict.npy',allow_pickle='TRUE').item()
metadata = pd.read_csv('metadata.csv', squeeze=True)
titles = pd.read_csv('titles.csv', squeeze = True)

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('app.html')


@app.route('/send', methods=['POST'])
def send(sum=sum):
    if request.method == 'POST':
        movie = request.form['movie']

        operation = request.form['operation']

        if operation == 'movie':
            if len(movie) == 0:
                result = ['no movie']
        # Check if movie is presented in the database
            else:
                if movie in d.keys():
                    result = d[movie]
                else:
                    result = ['empty']

            return render_template('app.html', result=result)
        
        elif operation == 'keywords':
            if len(movie) == 0:
                result = ['no keywords']
            else:
                result = search_keywords(movie, metadata, titles)
            return render_template('app.html', result=result)


if __name__ == '__main__':
    app.debug = True
    app.run()
