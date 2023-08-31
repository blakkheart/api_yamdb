from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CreateJWTTokenView, CreateUserView,
                       UserViewSet, CommentViewSet, ReviewViewSet)


router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<title_id>\d+)/comments',
    CommentViewSet, basename='comment')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='review')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', CreateUserView.as_view()),
    path('v1/auth/token/', CreateJWTTokenView.as_view()),
]
