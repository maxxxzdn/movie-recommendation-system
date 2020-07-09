from flask import Flask, render_template, request
from itertools import permutations
# Pre-calculated dictionary with top 10 similar movies for each movie in database

with open('dict.txt') as f:
    indices = f.read().splitlines()
    indices = [list(map(int,x.split())) for x in indices]

# List of movie titles
with open('titles.txt') as f:
    titles = f.read().splitlines()
    titles = [x.strip('"') for x in titles]

with open('origtitles.txt') as f:
    origtitles = f.read().splitlines()
    origtitles = [x.strip('"') for x in origtitles]

# List of strings with data for each movie including actors 
# (each lowercased and combined into one word), directors (same), genre, keywords    
with open('metadata.txt') as f:
    metadata = f.read().splitlines()
    metadata = [x.strip('"') for x in metadata]

"""
search by keywords
It iteratively creates matrix of token counts for keyword-string and 
metadata for each movie. Then cosine similarity for those 2 vectors 
is calculated. Top 10 scores is stored in dictionary.

:keywords: string with given keywords separated by comma
e.g. 'Joseph Gordon-Levitt, love, summer'
:metadata: list of strings with data for each movie including 
actors (each lowercased and combined into one word), directors (same), genre, keywords
:titles: list of movie titles
"""
def mistake(title, origtitles, titles):
    result = 0
    index = 0
    if ',' in title:
    	return -2
    if len(title.split()) > 3:
        title = ' '.join(title.split()[0:3])
    for i in range(len(origtitles)):
            a = title.lower()
            b = origtitles[i].lower()
            new_result = NW(a, b)
            if new_result > result:
                result = new_result
                index = i
    # Sort by count value
    if result != 0:
        return index
    else:
    	return -1

def Diagonal(n1,n2,pt):
    if(n1 == n2):
        return pt['MATCH']
    else:
        return pt['MISMATCH']
    
def NW(s1,s2,match = 100,mismatch = -100, gap = -100):
    penalty = {'MATCH': match, 'MISMATCH': mismatch, 'GAP': gap} #A dictionary for all the penalty valuse.
    n = len(s1) + 1 #The dimension of the matrix columns.
    m = len(s2) + 1 #The dimension of the matrix rows.
    al_mat = [[0 for i in range(n)] for i in range(m)] #Initializes the alighment matrix with zeros.
    #Scans all the first rows element in the matrix and fill it with "gap penalty"
    for i in range(m):
        al_mat[i][0] = penalty['GAP'] * i
    #Scans all the first columns element in the matrix and fill it with "gap penalty"
    for j in range (n):
        al_mat[0][j] = penalty['GAP'] * j
    #Fill the matrix with the correct values.

    for i in range(1,m):
        for j in range(1,n):
            di = al_mat[i-1][j-1] + Diagonal(s1[j-1],s2[i-1],penalty) #The value for match/mismatch -  diagonal.
            ho = al_mat[i][j-1] + penalty['GAP'] #The value for gap - horizontal.(from the left cell)
            ve = al_mat[i-1][j] + penalty['GAP'] #The value for gap - vertical.(from the upper cell)
            al_mat[i][j] = max(di,ho,ve) #Fill the matrix with the maximal value.(based on the python default maximum)
    return al_mat[m-1][n-1]

def search_keywords(keywords, metadata, titles):
    # Unification of keywords: all words in lower case, all names combined into one word
    keywords = list(map(lambda x: x.replace(' ', '').lower(), keywords.split(',')))
    results = []
    indices = []
    for i in range(len(metadata)):
            result = len(set(keywords).intersection(metadata[i].split()))
            if len(indices) < 10:
                results.append(result)
                indices.append(i)
            else:
                if result > min(results):
                    results.pop(results.index(min(results)))
                    indices.pop(results.index(min(results)))
                    indices.append(i)
                    results.append(result)
    if len(indices) != 0:
        results, indices  = zip(*sorted(zip(results, indices), reverse = True))
        return indices
    else:
        return []
        
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
                return render_template('app.html', result=['no movie'])

            # Check if movie is presented in the database
            else:
                if movie.lower() in list(map(str.lower, titles)):
                    movie_idx = list(map(str.lower, titles)).index(movie.lower())
                    idx = indices[movie_idx]
                    result = list(map(titles.__getitem__, idx))

                else:
                    if len(movie.split()) < 2:
                        idx = [x[0] for x in list(enumerate(map(str.lower, titles))) if movie.lower() in x[1].split()]
                    else:
                        idx = [x[0] for x in list(enumerate(map(str.lower, titles))) if tuple(movie.lower().split()) in list(permutations(x[1].split(), len(movie.split())))]
                    if len(idx) == 0:
                        idx = mistake(movie, origtitles, titles)
                        if idx == -1:
                            return render_template('app.html', result=['empty'])
                        if idx == -2:
                            return render_template('app.html', result=['empty', 'keywords'])
                    else:
                        idx = idx[0]

                    
                    idxs = indices[idx]
                    result = list(map(titles.__getitem__, idxs))
                    result.insert(0,'empty')
                    result.insert(1,titles[idx])

            return render_template('app.html', result=result)

        # If user uses search by keywords
        elif operation == 'keywords':

            # If no keywords typed
            if len(movie) == 0:
                result = ['no keywords']
            else:
                idx = search_keywords(movie, metadata, titles)
                result = list(map(titles.__getitem__, idx))
            return render_template('app.html', result=result)


if __name__ == '__main__':

    app.debug = True
    app.run()
