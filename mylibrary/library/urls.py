from django.urls import path, re_path
from library import views

urlpatterns = [
    path('', views.ShowGenres.as_view(), name='index'),
    re_path(r'^about/*$', views.about, name='about'),
    path('genre/<slug:genre_slug>/', views.ShowGenre.as_view(), name='genre'),
    path('book/<slug:book_slug>/', views.show_book, name='book'),
    path('author/<slug:author_slug>/', views.show_author, name='author'),
    path('addbook/', views.add_book, name='add_book'),
]
