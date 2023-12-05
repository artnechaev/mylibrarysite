from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.generic import ListView

from .forms import AddBookForm
from .models import Genre, Book

menu = [
    {'title': 'Главная', 'url': 'index'},
    {'title': 'Добавить книгу', 'url': 'add_book'},
    {'title': 'О сайте', 'url': 'about'},
]


# def index(request):
#     genres = Genre.visible.all()
#     context = {
#         'menu': menu,
#         'title': 'Главная',
#         'genres': genres,
#     }
#     return render(request, 'library/index.html', context)


class ShowGenres(ListView):
    model = Genre
    template_name = 'library/index.html'
    context_object_name = 'genres'
    extra_context = {
        'title': 'Главная',
    }

    def get_queryset(self):
        return Genre.visible.all()


def about(request):
    context = {
        'title': 'О сайте',
    }
    return TemplateResponse(request, 'library/about.html', context)


# def show_genre(request, genre_slug):
#     genre = get_object_or_404(Genre, slug=genre_slug)
#     books = genre.books.all()
#     context = {
#         'menu': menu,
#         'title': genre.name,
#         'genre': genre,
#         'books': books
#     }
#     return render(request, 'library/genre.html', context)


class ShowGenre(ListView):
    model = Book
    template_name = 'library/genre.html'
    context_object_name = 'books'
    paginate_by = 3

    def get_queryset(self):
        return Book.visible.filter(genre__slug=self.kwargs['genre_slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context['books']:
            genre = context['books'][0].genre
        else:
            genre = Genre.visible.get(slug=self.kwargs['genre_slug'])
        context['title'] = genre.name
        context['genre'] = genre
        return context


def show_book(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    genre = book.genre
    authors = book.author.all()
    context = {
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
        'title': 'Добавление книги',
        'form': form,
    }
    return render(request, 'library/addbook.html', context)
