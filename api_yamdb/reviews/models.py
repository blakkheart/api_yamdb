from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_year

User = get_user_model()


class Category(models.Model):
    """Category model.
    Includes name field (str, max length=256),
        slug field (str, max length=50, should be unique).
    Ordered by name field.
    """

    name = models.CharField(max_length=256, help_text='Name the category')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'Categories'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Genre model.
    Includes name field (str, max length=256),
        slug field (str, max length=50, should be unique).
    Ordered by name field.
    """

    name = models.CharField(max_length=256, help_text='Name the genre')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'genre'
        verbose_name_plural = 'Genres'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Title model.
    Includes name field (str, max length=256),
        year field (int),
        category field (Category model,
            on delete=SET_NULL, could be blank and null, related name=titles),
        genre field (Genre model, many to many relation
            through GenreTitle model, related name=titles),
        description field (str, could be blank and null).
    Ordered by name field.
    """

    name = models.CharField(max_length=256, help_text='Name the title')
    year = models.IntegerField(validators=(validate_year,))
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', related_name='titles'
    )
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'Titles'
        ordering = ('name',)

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """GenreTitle model.
    Through model for Title and Genre models releationship.
    Includes genre field(Genre model, on delete=CASCADE),
        title field(Title model, on delete=CASCADE).
    """

    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.genre} - {self.title}.'


class Review(models.Model):
    """Title model.
    Includes author field (User model, on delete=CASCADE,
            related name=reviews),
        pub_date field (DateTimeField, auto now add=True),
        text field (str),
        title field (Title model, on delete=CASCADE, related name=titles),
        score field (int, choise between 1 and 10).
    Ordered by pub_date field.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField('Date of publication', auto_now_add=True)
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text='Choose the number between 1 and 10',
    )

    class Meta:
        verbose_name = 'review'
        verbose_name_plural = 'Reviews'
        ordering = ('pub_date',)
        constraints = (
            models.UniqueConstraint(
                name='unique_review', fields=('author', 'title')
            ),
        )

    def __str__(self):
        return f'{self.title.name}: {self.score}.'


class Comment(models.Model):
    """Comment model.
    Includes author field (User model, on delete=CASCADE,
            related name=comments),
        pub_date field (DateTimeField, auto now add=True),
        review field (Review model, on delete=CASCADE, related name=comments),
        text field (str).
    Ordered by pub_date field.
    """

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    pub_date = models.DateTimeField('Date of publication', auto_now_add=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'Comments'
        ordering = ('pub_date',)

    def __str__(self):
        return self.text[:50]
