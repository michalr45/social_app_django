from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from .models import Follow
from posts.models import Comment
from books.models import Book
import requests
import json


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # creating profile
            profile = Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/edit.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def user_detail(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, 'account/user/user_detail.html', {'user': user})


@login_required
def user_comments(request, username):
    user = get_object_or_404(User, username=username)
    comments = Comment.objects.filter(author=user)
    return render(request, 'account/user/view_user_comments.html', {'user': user,
                                                                    'comments': comments})


@login_required
def user_books(request, username):
    user = get_object_or_404(User, username=username)
    get_books = Book.objects.filter(user=user)
    books = []
    for book in get_books:
        response = requests.get(f'https://api.itbook.store/1.0/books/{book.isbn}')
        single_book = response.json()
        books.append(single_book)
    return render(request, 'account/user/view_user_books.html', {'user': user,
                                                                 'books': books})


@login_required
def user_follow(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        if request.method == 'POST':
            data = json.load(request)
            user_id = data.get('id')
            action = data.get('action')
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Follow.objects.get_or_create(user_from=request.user, user_to=user)
                return JsonResponse({'status': 'followed'})
            else:
                Follow.objects.filter(user_from=request.user, user_to=user).delete()
                return JsonResponse({'status': 'unfollowed'})
        return JsonResponse({'status': 'error-1'})
    else:
        return JsonResponse({'status': 'error-2'})
