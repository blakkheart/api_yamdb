# Generated by Django 3.2 on 2023-09-03 12:11

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={
                'ordering': ('name',),
                'verbose_name': 'category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={
                'ordering': ('pub_date',),
                'verbose_name': 'comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.AlterModelOptions(
            name='genre',
            options={
                'ordering': ('name',),
                'verbose_name': 'genre',
                'verbose_name_plural': 'Genres',
            },
        ),
        migrations.AlterModelOptions(
            name='review',
            options={
                'ordering': ('pub_date',),
                'verbose_name': 'review',
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.AlterModelOptions(
            name='title',
            options={
                'ordering': ('name',),
                'verbose_name': 'title',
                'verbose_name_plural': 'Titles',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(
                help_text='Name the category', max_length=256
            ),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(
                auto_now_add=True, verbose_name='Date of publication'
            ),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Name the genre', max_length=256),
        ),
        migrations.AlterField(
            model_name='genre',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='review',
            name='pub_date',
            field=models.DateTimeField(
                auto_now_add=True, verbose_name='Date of publication'
            ),
        ),
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(
                help_text='Choose the number between 1 and 10',
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(10),
                ],
            ),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='titles',
                to='reviews.category',
            ),
        ),
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(
                related_name='titles',
                through='reviews.GenreTitle',
                to='reviews.Genre',
            ),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(help_text='Name the title', max_length=256),
        ),
        migrations.AlterField(
            model_name='title', name='year', field=models.IntegerField(),
        ),
    ]
