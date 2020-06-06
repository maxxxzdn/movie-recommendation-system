from flask import Flask, render_template, request
import numpy as np

d = np.load('movie_dict.npy',allow_pickle='TRUE').item()

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('app.html')


@app.route('/send', methods=['POST'])
def send(sum=sum):
    if request.method == 'POST':
        movie = request.form['movie']
        # Check if movie is presented in the database
        if movie in d.keys():
            result = d[movie]
        else:
            result = []

        return render_template('app.html', result=result)


if __name__ == '__main__':
    app.debug = True
    app.run()
