from django.shortcuts import render, redirect
from .models import Book
from django.contrib.auth.decorators import login_required
import requests


@login_required
def bookshelf(request):
    user = request.user
    user_books = Book.objects.filter(user=user)
    books = []
    for book in user_books:
        response = requests.get(f'https://api.itbook.store/1.0/books/{book.isbn}')
        single_book = response.json()
        books.append(single_book)
    return render(request, 'books/bookshelf.html', {'books': books})


@login_required
def save_book(request, isbn):

    # get isbn values of books of user
    user_books = Book.objects.filter(user=request.user)
    books = []
    for book in user_books:
        books.append(book.isbn)

    # check if book with given isbn doesn't already exist in user's collection
    if isbn not in books:
        # create new book object
        book = Book(user=request.user, isbn=isbn)
        book.save()
    return redirect('books:bookshelf')


@login_required
def delete_book(request, isbn):
    user_books = Book.objects.filter(user=request.user)
    for book in user_books:
        if book.isbn == isbn:
            book.delete()
    return redirect('books:bookshelf')

