from django.contrib.auth.decorators import login_required
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


@login_required
def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            w = form.save(commit=True)
            w.added_by = request.user
            slug = w.slug
            w.save()
            return redirect('book', slug)
    else:
        form = AddBookForm()
    context = {
        'title': 'Добавление книги',
        'form': form,
    }
    return render(request, 'library/addbook.html', context)
