from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError('Cannot use "me" as a name')
        return value

    def validate(self, data):
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


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    confirmation_code = serializers.CharField(required=True)


class UserEditSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)

    def validate(self, data):
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


class UserAdminEditSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(regex=r'^[\w.@+-]+\Z', max_length=150)
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

    def validate(self, data):
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
