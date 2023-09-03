from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    """CustomUser model.
    Inherited from AbstractUser, redefining default user model.
    Includes username field (str, max length=150, unique=True),
        email field (str, max length=254, unique=True),
        first_name field (str, max length=254, could be blank and null),
        last_name field (str, max length=254, could be blank and null),
        bio field (str, could be blank and null),
        role field (str, choise between user,
            moderator and admin, default=user).
    Has is_admin property, checks, if user.role == admin,
        is_moderator property, checks, if user.role == moderator.
    """

    class Role(models.TextChoices):
        USER = 'user', 'User'
        ADMIN = 'admin', 'Admin'
        MODERATOR = 'moderator', 'Moderator'

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')],
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        choices=Role.choices, default=Role.USER, max_length=10
    )

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.Role.MODERATOR
