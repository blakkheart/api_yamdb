from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.filters import SearchFilter
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
)
from rest_framework.viewsets import GenericViewSet

from api.permissions import IsAdminOrReadOnly

User = get_user_model()


class CreateListDestroyMixin(
    CreateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    """Mixin including Create, Destroy and List methods.
    Has permission class checks if {request.user} is admin or read only.
    Has search option with {name} field.
    Set lookup field to {slug} field.
    """

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class UserMixinSerializer(serializers.ModelSerializer):
    """Serializer base to be inheriteted in {UserCreate},
        {UserEdit} and {UserAdminEdit} serializers.
    """

    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)

    def validate(self, data):
        """Validates username and email not allowing to get accesses to data
            via someone elses username and email."""
        if User.objects.filter(
            username=data.get('username'), email=data.get('email')
        ):
            return data
        elif User.objects.filter(username=data.get('username')):
            raise serializers.ValidationError(
                'Username has already been taken'
            )
        elif User.objects.filter(email=data.get('email')):
            raise serializers.ValidationError(
                'Email adress has already been taken'
            )
        return data
