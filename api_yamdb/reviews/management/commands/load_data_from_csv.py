import csv

from django.core.management import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings


from reviews.models import Category, Genre, Comment, Review, Title, GenreTitle

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
    def handle(self, *args, **options) -> str | None:
        for csv_file in list_of_csv:
            # print(csv_file)
            with open(
                str(settings.CSV_DATA_DIR) + '/' + csv_file + '.csv',
                encoding='utf-8',
            ) as file:
                for model_data in csv.DictReader(file):
                    # print(model_data)
                    # print(csv_models_dict.get(csv_file))
                    for key, value in model_data.items():
                        if key in csv_models_dict:
                            model_data[key] = csv_models_dict[key].objects.get(
                                pk=value
                            )
                    model = csv_models_dict.get(csv_file)(**model_data)
                    model.save()
        return
