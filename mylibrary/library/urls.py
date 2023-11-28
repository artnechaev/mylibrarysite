from django.urls import path
from library import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('genre/<slug:genre_slug>', views.show_genre, name='genre'),
    path('book/<slug:book_slug>', views.show_book, name='book'),
    path('author/<slug:author_slug>', views.show_author, name='author'),
]
