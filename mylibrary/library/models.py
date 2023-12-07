from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse


class VisibleManager(models.Manager):
    """Менеджер моделей, возвращающий записей с is_visible == True"""

    def get_queryset(self):
        return super().get_queryset().filter(is_visible=True)


class Genre(models.Model):
    """Жанр книг"""

    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')
    is_visible = models.BooleanField(default=True, verbose_name='Видимость')

    objects = models.Manager()
    visible = VisibleManager()

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('library:genre', kwargs={'genre_slug': self.slug})


class Author(models.Model):
    """Автор"""

    name = models.CharField(max_length=100, verbose_name='Имя')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')
    fullname = models.TextField(blank=True, null=True, verbose_name='Полное имя')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('author', kwargs={'author_slug': self.slug})


class Book(models.Model):
    """Отдельная книга"""

    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='URL')
    synopsis = models.TextField(blank=True, null=True, verbose_name='Описание')
    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    is_visible = models.BooleanField(default=True, verbose_name='Видимость')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='books', verbose_name='Жанр')
    author = models.ManyToManyField(Author, related_name='books', verbose_name='Автор')
    added_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='books',
                                 verbose_name='Добавил', null=True, default=None)

    objects = models.Manager()
    visible = VisibleManager()

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('book', kwargs={'book_slug': self.slug})
