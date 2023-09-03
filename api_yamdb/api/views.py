from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from api.filters import TitleFilter
from api.mixins import CreateListDestroyMixin
from api.permissions import (
    IsAdminModeratorSuperUserAuthorOrReadOnly,
    IsAdminOrReadOnly,
    IsAdminOrSuperUser,
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    GetTitleSerializer,
    ReviewSerializer,
    TitleSerializer,
    TokenSerializer,
    UserAdminEditSerializer,
    UserCreateSerializer,
    UserEditSerializer,
)
from reviews.models import Category, Genre, Review, Title


User = get_user_model()


class CreateUserView(CreateAPIView):
    """ViewSet allows only POST method.
    Allows any user to register providing {username} and {email}.
    Create {User} model and sending an email to {email} adress with
        generated {token}.
    """

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        token = default_token_generator.make_token(user)
        send_mail(
            subject='Confirm your registration on YaMDB',
            message=f'Your confirmation code: {token}',
            from_email='yamdb_registration@yandex.ru',
            recipient_list=[user.email],
            fail_silently=True,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateJWTTokenView(CreateAPIView):
    """ViewSet allows only POST method.
    Allows any user to get access token
        providing {username} and {cofirmation_token}.
    Create {AccessToken} for particular user.
    """

    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return get_object_or_404(User, username=self.kwargs['username'])

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data['username']
        )
        token = serializer.validated_data['confirmation_code']
        if default_token_generator.check_token(user, token):
            token = AccessToken.for_user(user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet that allows admin or superuser to register users
        and allows authenticated users to change
        their profile with PATCH method to users/me/ adress.
    PUT method is restricted.
    Allows to filter results via {username} field.
    Redefines lookup field with {username} field.
    Contains {PageNumberPagination}.
    """

    queryset = User.objects.all()
    serializer_class = UserAdminEditSerializer
    permission_classes = (IsAdminOrSuperUser,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    search_fields = ('username',)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'delete', 'patch']

    @action(
        methods=['get', 'patch'],
        permission_classes=(permissions.IsAuthenticated,),
        detail=False,
        serializer_class=UserEditSerializer,
        url_path='me',
    )
    def me(self, request):
        """Allows authenticated users to change
            their profile with PATCH method to users/me/ adress.
        """
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet that allows to create, delete, edit and view comments.
    PUT method is restricted.
    Permission class {IsAdminModeratorSuperUserAuthorOrReadOnly}
    """

    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorSuperUserAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet that allows to create, delete, edit and view reviews.
    PUT method is restricted.
    Permission class {IsAdminModeratorSuperUserAuthorOrReadOnly}
    """

    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorSuperUserAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.select_related('author')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CategoryViewSet(CreateListDestroyMixin):
    """ViewSet that allows to view categories.
    Allows admin to create, edit and delete categories.
    Allows to filter results via {name} field.
    Redefines lookup field with {slug} field.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CreateListDestroyMixin):
    """ViewSet that allows to view genres.
    Allows admin to create, edit and delete genres.
    Allows to filter results via {name} field.
    Redefines lookup field with {slug} field.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet that allows to view titles.
    Allows admin to create, edit and delete titles.
    PUT method is restricted.
    Allows to filter results via {TitleFilter} FilterSet.
    Contains {PageNumberPagination}.
    """

    queryset = Title.objects.prefetch_related('genre', 'category').annotate(
        rating=Avg('reviews__score')
    )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetTitleSerializer
        return TitleSerializer

    def perform_create(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre)

    def perform_update(self, serializer):
        category = get_object_or_404(
            Category, slug=self.request.data.get('category')
        )
        genre = Genre.objects.filter(
            slug__in=self.request.data.getlist('genre')
        )
        serializer.save(category=category, genre=genre, partial=True)
