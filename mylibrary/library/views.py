from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse

from .forms import AddBookForm
from .models import Genre, Book

menu = [
    {'title': 'Главная', 'url': 'index'},
    {'title': 'Добавить книгу', 'url': 'add_book'},
    {'title': 'О сайте', 'url': 'about'},
    {'title': 'Войти', 'url': 'admin:index'},
]


def index(request):
    genres = Genre.visible.all()
    context = {
        'menu': menu,
        'title': 'Главная',
        'genres': genres,
    }
    return render(request, 'library/index.html', context)


def about(request):
    context = {
        'menu': menu,
        'title': 'О сайте',
    }
    return TemplateResponse(request, 'library/about.html', context)


def show_genre(request, genre_slug):
    genre = get_object_or_404(Genre, slug=genre_slug)
    books = genre.books.all()
    context = {
        'menu': menu,
        'title': genre.name,
        'genre': genre,
        'books': books
    }
    return render(request, 'library/genre.html', context)


def show_book(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    genre = book.genre
    authors = book.author.all()
    context = {
        'menu': menu,
        'title': book.name,
        'genre': genre,
        'book': book,
        'authors': authors,
    }
    return render(request, 'library/book.html', context)


def show_author(request, author_slug):
    return HttpResponse("<h1>author_slug</h1>")


def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = AddBookForm()
    context = {
        'menu': menu,
        'title': 'Добавление книги',
        'form': form,
    }
    return render(request, 'library/addbook.html', context)
