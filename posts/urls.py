from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.home_page, name="home_page"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('search/', views.search, name='search_results'),
    path('like/', views.post_like, name='like'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('book/<str:isbn>/', views.book_detail, name='book_detail'),
    #  user activities panel
    path('user/posts/', views.user_posts, name='user_posts'),
    path('user/comments/', views.user_comments, name='user_comments'),
    path('user/follows/', views.user_follows, name='user_follows'),
    path('user/likes/', views.user_likes, name='user_likes'),
    #  deleting content
    path('comment/delete/<int:comment_id>/', views.comment_delete, name='delete_comment'),
    path('post/delete/<int:post_id>/', views.post_delete, name='delete_post'),
]
