import pickle
from flask import Flask, request, send_file, make_response
import requests
import json

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


movies = pickle.load(open('model/movie_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

movie_list = movies['title'].values


app = Flask(__name__)

@app.get('/')
def home():
    return send_file('index.html')

@app.get('/movies')
def movie():
    return make_response(json.dumps(movie_list.tolist()), 200)

@app.post('/recommend')
def recommend_movie():
    movie = request.json['movie']
    recommended_movie_names,recommended_movie_posters = recommend(movie)
    reccomendation = zip(recommended_movie_names,recommended_movie_posters)
    return make_response([{ 'title': movie, 'poster': poster } for movie, poster in reccomendation], 200)
