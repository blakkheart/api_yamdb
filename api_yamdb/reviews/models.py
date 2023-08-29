from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    text = models.TextField()
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                              related_name='reviews')
    # score =


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    pub_date = models.DateTimeField('Дата добавления', auto_now_add=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
