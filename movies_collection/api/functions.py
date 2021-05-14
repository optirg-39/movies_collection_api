import requests
from requests.auth import HTTPBasicAuth
import json
from .models import *
from django.db.models import Q

"""Function for geting movies from movies api """
def get_movies(id=None):
    if id is None:
        URL = "https://demo.credy.in/api/v1/maya/movies"
    else:
        URL = f"https://demo.credy.in/api/v1/maya/movies/?page={id}"
    abc = "iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0"
    pww = "Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1"
    response_1 = requests.get(url=URL, auth=HTTPBasicAuth(username=abc, password=pww))
    if response_1.status_code == 200:
        response = response_1.text
        response_2 = json.loads(response)
        if id is None:
            response_2['next'] = f"http://localhost:8000/movies/2/"
            response_2['previous'] = f"None"
        if id:
            response_2['next'] = f"http://localhost:8000/movies/{id + 1}/"
            if id - 1 == 1:
                response_2['previous'] = "http://localhost:8000/movies/"
            else:
                response_2['previous'] = f"http://localhost:8000/movies/{id - 1}/"
        old_key = "results"
        new_key = "data"
        response_2[new_key] = response_2.pop(old_key)
    else:
        response_2=None
    return response_2

"""Top three genres of user"""
def top_three(genres):
    l = [getattr(i, 'genre') for i in genres]
    d = {i: l.count(i) for i in l}
    m1 = []
    m = 0
    while m < 3:
        max_key = max(d, key=d.get)
        if max_key == '':
            d.pop(max_key)
            continue
        m1.append(max_key)
        d.pop(max_key)
        m += 1
    return m1


def remove_movie(collection_uuid,movie_title):
    movie_inst = Movies.objects.get(title=movie_title)
    other_coll = Collection.objects.filter(Q(movies=movie_inst) & ~Q(uuid=collection_uuid))
    collection_inst=Collection.objects.get(uuid=collection_uuid)
    if other_coll.exists():
        """Dont delete the movie just remove relation"""
        movie_inst.collection.remove(collection_inst)
    else:
        genres = Genres.objects.filter(movie=movie_inst)
        for genre in genres:
            remove_genre(genre, movie_inst)
        movie_inst.delete()

def add_movie(collection_uuid,**movie_data):
    genres_data = movie_data.pop('genres')
    genres_list = genres_data.split(',')
    movie_exist, movie_created = Movies.objects.get_or_create(**movie_data)
    collection_inst=Collection.objects.get(uuid=collection_uuid)
    movie_inst = Movies.objects.get(title=movie_data['title'])
    movie_inst.collection.add(collection_inst)
    if movie_created:
        """Add genres"""
        for genre in genres_list:
            add_genres(genre, movie_inst)

def remove_genre(genre, movie_inst):
    M2 = Movies.objects.filter(Q(genres=genre) & ~Q(title=movie_inst.title))
    genre_inst = Genres.objects.get(genre=genre.genre)
    if M2.exists():
        genre_inst.movie.remove(movie_inst)
    else:
        genre_inst.delete()

def add_genres(genre,movie_inst):
    genre_exist, genre_create = Genres.objects.get_or_create(genre=genre)
    genre_inst = Genres.objects.get(genre=genre)
    genre_inst.movie.add(movie_inst)

