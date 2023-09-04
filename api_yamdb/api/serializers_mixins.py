from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


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
