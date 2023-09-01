from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название',
                            help_text='Выберите категорию')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название',
                            help_text='Выберите жанр')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256, verbose_name='Название',
                            help_text='Выберите название произведения')
    year = models.IntegerField(verbose_name='Год')
    category = models.ForeignKey(Category, verbose_name='Категория',
                                 on_delete=models.SET_NULL, null=True,
                                 blank=True, related_name='titles')
    genre = models.ManyToManyField(Genre, blank=True, verbose_name='Жанр',
                                   related_name='titles')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    score = models.IntegerField(validators=[MinValueValidator(1),
                                MaxValueValidator(10)],
                                help_text='Введите целое число от 1 до 10')

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date', )
        constraints = (
            models.UniqueConstraint(
                name='unique_review',
                fields=('author', 'title')
            ),
        )

    def __str__(self):
        return f'{self.title.name}: {self.score}.'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date', )

    def __str__(self):
        return self.text[:50]
