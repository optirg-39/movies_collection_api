from rest_framework import serializers
from . models import Movies, Collection, Genres
from django.contrib.auth.models import User

"""Ok tested for registration"""
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], password = validated_data['password'])
        return user


""" for Collection_Get_APIView get"""
class Collection_serializer_A(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['title', 'uuid', 'description']

"""Ok tested for get api """
class Movies_read_Serializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Movies
        fields = ['title', 'description', 'genres', 'uuid']

class Collection_read_Serializer(serializers.ModelSerializer):
    movies = Movies_read_Serializer(many=True, read_only=True)

    class Meta:
        model = Collection
        fields = ['title','description','movies']







