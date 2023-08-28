from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CreateJWTTokenView, CreateUserView, UserViewSet


router_v1 = DefaultRouter()
router_v1.register(r'users', UserViewSet)


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', CreateUserView.as_view()),
    path('v1/auth/token/', CreateJWTTokenView.as_view()),
]
