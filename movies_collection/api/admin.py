from django.contrib import admin
from .models import Collection, Movies, Genres


# Register your models here
@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','uuid','user']


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','uuid']



@admin.register(Genres)
class GenresAdmin(admin.ModelAdmin):
    list_display = ['id','genre']
