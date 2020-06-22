from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from .views import CategoryViewSet, GenreViewSet, TitleViewSet

router = DefaultRouter()
router.register("titles", TitleViewSet, basename="titles")
router.register("categories", CategoryViewSet, basename="categories")
router.register("genres", GenreViewSet, basename="genres")

urlpatterns = [
    path("api/v1/", include(router.urls)),
]
