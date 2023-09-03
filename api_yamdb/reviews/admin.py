from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Register Comment model in Admin panel with all fields."""

    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Register Category model in Admin panel with all fields."""

    pass


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    """Register Title model in Admin panel with all fields."""

    pass


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Register Genre model in Admin panel with all fields."""

    pass


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Register Review model in Admin panel with all fields."""

    pass
