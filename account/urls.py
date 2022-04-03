from django.urls import path, include
from . import views


urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('register/', views.register, name="register"),
    path('edit/', views.edit, name="edit"),
    path('users/follow/', views.user_follow, name='user_follow'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('users/<username>/comments/', views.user_comments, name='view_user_comments'),
    path('users/<username>/books/', views.user_books, name='view_user_books'),
]
