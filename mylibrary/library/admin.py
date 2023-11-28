from django.contrib import admin

from .models import Book, Genre, Author


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'is_visible')
    list_display_links = ('id', 'name')
    list_editable = ('is_visible',)
    list_filter = ('is_visible',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'date_added', 'date_updated', 'genre', 'is_visible')
    list_display_links = ('id', 'name')
    list_editable = ('is_visible',)
    list_filter = ('is_visible', 'date_added')
    search_fields = ('name', 'slug', 'synopsis')
    prepopulated_fields = {"slug": ("name",)}
