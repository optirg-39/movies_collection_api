from django.contrib import admin
from django.urls import path
from api import views
from rest_framework_simplejwt import views as jwt_views
import uuid

urlpatterns = [
    path('admin/', admin.site.urls),
    path('collection/',views.Collection_Get_APIView.as_view() ),
    path('collection/<uuid:uuid>/',views.CollectionAPI.as_view() ),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.RegisterApi.as_view()),
    path('movies/', views.MoviesAPI.as_view()),
    path('movies/<int:id>/', views.MoviesAPI.as_view())
]
