from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostCreateForm, CommentCreateForm
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
import requests
from django.core.paginator import Paginator
from books.models import Book


def home_page(request):
    if request.user.is_authenticated:
        return redirect('posts:dashboard')
    else:
        return render(request, 'home_page.html')


@login_required
def dashboard(request):
    following_ids = request.user.following.values_list('id', flat=True)
    post_objects = Post.objects.order_by('-created')
    posts = []

    # add matching 'Post' objects to list 'posts'
    if following_ids:
        for post in list(post_objects):
            if post in Post.objects.filter(user_id__in=following_ids):
                posts.append(post)

    # pagination
    paginated_posts = Paginator(posts, 8)
    page_number = request.GET.get('page')
    page_obj = paginated_posts.get_page(page_number)

    # handling creating post form
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('posts:dashboard')
    else:
        form = PostCreateForm()

        return render(request, 'posts/dashboard.html', {'paginated_posts': paginated_posts,
                                                        'page_obj': page_obj,
                                                        'form': form})


@login_required
def search(request):
    query = request.GET.get('search')

    # search for users
    if request.method == 'GET':
        search_list = User.objects.filter(username__contains=query).exclude(id=request.user.id)

    # cleaning the query for api request
    cleaned = query.partition('/')
    query = cleaned[0]
    page = cleaned[2]
    if page == '':
        page = 0
    page = int(page) + 1
    query = query + '/' + str(page)

    if request.method == 'GET':
        # search for books using itbook.store api
        books_list = []
        response = requests.get(f'https://api.itbook.store/1.0/search/{query}')
        response_json = response.json()

        if response.status_code == 200:
            for book in response_json['books']:
                books_list.append(book)

        elif response.status_code == 404:
            books_list = []

        return render(request, 'posts/search_results.html', {'search_list': search_list,
                                                             'books_list': books_list,
                                                             'query': query,
                                                             'response_json': response_json
                                                             })


@login_required
def post_like(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            post_id = data.get('id')
            action = data.get('action')
            post = Post.objects.get(id=post_id)
            if action == 'like':
                post.users_like.add(request.user)
                return JsonResponse({'status': 'liked'})
            else:
                post.users_like.remove(request.user)
                return JsonResponse({'status': 'unliked'})
        return JsonResponse({'status': 'error-1'})
    else:
        return JsonResponse({'status': 'error-2'})


@login_required
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        comment_form = CommentCreateForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
            return redirect('posts:post_detail', slug)
    else:
        comment_form = CommentCreateForm()
        return render(request, 'posts/post_detail.html', {'post': post,
                                                          'comment_form': comment_form})


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.author:
        comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.user:
        post.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def user_posts(request):
    posts = Post.objects.filter(user=request.user).order_by('-created')
    return render(request, 'posts/user_posts.html', {'posts': posts})


@login_required
def user_comments(request):
    comments = Comment.objects.filter(author=request.user)
    return render(request, 'posts/user_comments.html', {'comments': comments})


@login_required
def user_follows(request):
    follows = request.user.following.all()
    return render(request, 'posts/user_follows.html', {'follows': follows})


@login_required
def user_likes(request):
    posts = request.user.posts_liked.all()
    return render(request, 'posts/user_likes.html', {'posts': posts})


@login_required
def book_detail(request, isbn):
    user_books = Book.objects.filter(user=request.user)
    isbn_list = []
    for book in user_books:
        isbn_list.append(book.isbn)

    # get detail of book
    response = requests.get(f'https://api.itbook.store/1.0/books/{isbn}')
    response_json = response.json()

    if response.status_code == 200:
        book = response_json

    elif response.status_code == 404:
        book = 'No book found!'

    return render(request, 'posts/book_detail.html', {'book': book,
                                                      'isbn_list': isbn_list})
