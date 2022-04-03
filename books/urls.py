from django.urls import path, include
from . import views

app_name = 'books'

urlpatterns = [
    path('save/<str:isbn>/', views.save_book, name='save_book'),
    path('delete/<str:isbn>/', views.delete_book, name='delete_book'),
    path('user/bookshelf/', views.bookshelf, name='bookshelf'),
]

