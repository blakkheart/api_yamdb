import csv

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

User = get_user_model()

list_of_csv = [
    'users',
    'category',
    'genre',
    'titles',
    'genre_title',
    'review',
    'comments',
]

csv_models_dict = {
    'category': Category,
    'comments': Comment,
    'genre_title': GenreTitle,
    'genre': Genre,
    'review': Review,
    'titles': Title,
    'users': User,
    'author': User,
}


class Command(BaseCommand):
    """CSV parser that imports data to models.
    Django command that allows to parse csv filedir
        and import data to each model.
    """

    def handle(self, *args, **options) -> None:
        for csv_file_name in list_of_csv:
            print(f'loading {csv_file_name} ', end='')
            with open(
                str(settings.CSV_DATA_DIR) + '/' + csv_file_name + '.csv',
                encoding='utf-8',
            ) as file:
                for model_data in csv.DictReader(file):
                    for key, value in model_data.items():
                        if key in csv_models_dict:
                            model_data[key] = csv_models_dict[key].objects.get(
                                pk=value
                            )
                    model = csv_models_dict.get(csv_file_name)(**model_data)
                    model.save()
                    print('.', end='')
            print('.. DONE')
