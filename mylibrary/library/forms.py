from django import forms

from .models import Book


class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'slug', 'synopsis', 'is_visible', 'genre', 'author']
        labels = {'slug': 'URL'}