from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CreateJWTTokenView, CreateUserView,
                       UserViewSet, CommentViewSet, ReviewViewSet,
                       CategoryViewSet, GenreViewSet, TitleViewSet)


router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='review')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', CreateUserView.as_view()),
    path('v1/auth/token/', CreateJWTTokenView.as_view()),
]
