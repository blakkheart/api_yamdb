from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


User = get_user_model()


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    score = models.IntegerField(validators=[MinValueValidator(1),
                                MaxValueValidator(10)],
                                help_text='Введите целое число от 1 до 10')

    class Meta:
        ordering = ('pub_date', )
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = (
            models.UniqueConstraint(
                name='unique_review',
                fields=('author', 'title')
            ),
        )

    def __str__(self):
        return f'{self.title.name} - {self.score}.'


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
        return self.text[:200]
