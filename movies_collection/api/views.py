from django.shortcuts import render, HttpResponseRedirect
from rest_framework import generics
from .functions import *
from .models import Movies, Genres, Collection
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
import json,requests
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# Create your views here.
import io
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse


"""Register and return JWT """
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cust_data = request.data
        rep_token = requests.post("http://127.0.0.1:8000/api/token/", data=cust_data)
        data_token=rep_token.json()
        access = data_token['access']
        return Response({"Access":access})

class MoviesAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None, **kwargs):
        r=get_movies(id)
        ans=JSONRenderer().render(r)
        return HttpResponse(ans, content_type='appliction/json')

class Collection_Get_APIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format =None):
        coll = Collection.objects.filter(user__username=request.user)
        serializer =  Collection_serializer_A(coll, many=True)
        genres = Genres.objects.filter(movie__collection__user__username=request.user)
        m1=top_three(genres)
        repy={"is_success": True,'data': {"collections": serializer.data,"favourite_genres": m1,}}
        return Response(repy)

    def post(self, request, format =None):
        data=request.body
        stream=io.BytesIO(data)
        python_data=JSONParser().parse(stream)
        movie_data=python_data.pop('movies')
        user=User.objects.get(username=request.user)
        collection=Collection.objects.create(user=user, **python_data)

        for movie in movie_data:
            add_movie(collection_uuid=collection.uuid, **movie)
        return Response({"collection_uuid": collection.uuid}, status=status.HTTP_201_CREATED)

class CollectionAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, uuid=None, format =None):
        collection = Collection.objects.get(uuid=uuid)
        print(collection)
        serializer = Collection_read_Serializer(collection)
        return Response(serializer.data)

    def put(self, request, uuid=None, format =None):
        data = request.body
        stream = io.BytesIO(data)
        python_data = JSONParser().parse(stream)
        movie_data = python_data.pop('movies')
        new_movies_title=[movie['title'] for movie in movie_data]

        updated_collection_1 = Collection.objects.filter(uuid = uuid).update(**python_data)
        updated_collection=Collection.objects.get(uuid=uuid)
        old_movies= Movies.objects.filter(collection__uuid=uuid)
        old_movies_title=[ movie.title for movie in old_movies]

        """Movies Remain in the  updated collection"""
        comman_movies_list = [movie for movie in new_movies_title if movie in old_movies_title]


        """Movies Add in updated collection"""
        uncomman_movies_list= [movie for movie in new_movies_title if movie not in comman_movies_list]
        uncomman_data=[data for data in movie_data if data['title'] in uncomman_movies_list]
        for movie in uncomman_data:
            add_movie(collection_uuid=uuid, **movie)

        """Removing from updated collection or deleted"""
        remove_movies_list=[movie for movie in old_movies_title if movie not in comman_movies_list]
        for movie_1 in remove_movies_list:
            """function remove_movie for removing movies form collection """
            remove_movie(collection_uuid=uuid, movie_title=movie_1)
        serializers=Collection_read_Serializer(updated_collection)
        return Response({"updated collection":serializers.data})

    def delete(self, request, uuid, format =None):
        delete_collection = Collection.objects.get(uuid = uuid)
        movies_list = Movies.objects.filter(collection=delete_collection)
        movies_title=[movie.title for movie in movies_list]
        for movie in movies_title:
            remove_movie(collection_uuid=uuid,movie_title=movie)
        delete_collection.delete()
        return Response({"Deleted": "Successfully"}, status=status.HTTP_201_CREATED)

