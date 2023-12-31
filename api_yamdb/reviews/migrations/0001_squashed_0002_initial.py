# Generated by Django 3.2 on 2023-09-05 17:57

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import reviews.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(
                    help_text='Name the category', max_length=256)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'Categories',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name the genre', max_length=256)),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'Genres',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='reviews.genre')),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name the title', max_length=256)),
                ('year', models.IntegerField(
                    validators=[reviews.validators.validate_year])),
                ('description', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True,
                 on_delete=django.db.models.deletion.SET_NULL, related_name='titles', to='reviews.category')),
                ('genre', models.ManyToManyField(related_name='titles',
                 through='reviews.GenreTitle', to='reviews.Genre')),
            ],
            options={
                'verbose_name': 'title',
                'verbose_name_plural': 'Titles',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(
                    auto_now_add=True, verbose_name='Date of publication')),
                ('text', models.TextField()),
                ('score', models.PositiveSmallIntegerField(help_text='Choose the number between 1 and 10', validators=[
                 django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='reviews', to='reviews.title')),
            ],
            options={
                'verbose_name': 'review',
                'verbose_name_plural': 'Reviews',
                'ordering': ('pub_date',),
            },
        ),
        migrations.AddField(
            model_name='genretitle',
            name='title',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='reviews.title'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('pub_date', models.DateTimeField(
                    auto_now_add=True, verbose_name='Date of publication')),
                ('text', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='comments', to='reviews.review')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'Comments',
                'ordering': ('pub_date',),
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(
                fields=('author', 'title'), name='unique_review'),
        ),
    ]
