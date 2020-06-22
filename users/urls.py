from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUsersViewSet, ProfileView

router = DefaultRouter()
router.register("api/v1/users", CustomUsersViewSet, basename="users")

urlpatterns = [
    path("api/v1/users/me/", ProfileView.as_view()),
    path("", include(router.urls)),
]
