from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Collection(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Collection'

class Movies(models.Model):
    collection = models.ManyToManyField(Collection, related_name="movies")
    title = models.CharField(max_length=200)
    description = models.TextField()
    uuid = models.UUIDField(default='')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Movies'

class Genres(models.Model):
    movie = models.ManyToManyField(Movies, related_name="genres")
    genre =models.CharField(max_length=100)

    def __str__(self):
        return self.genre

    class Meta:
        db_table = 'Genres'


