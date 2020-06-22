from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import exceptions, filters, permissions, viewsets

from .filters import TitleFilter
from .models import Category, Genre, Title
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]

    def get_queryset(self):
        slug = self.kwargs.get("slug", None)

        if slug is not None:
            queryset = Category.objects.filter(slug=slug)

            if len(queryset) == 0:
                raise exceptions.MethodNotAllowed(self.request.method)

        return Category.objects.all()


class GenreViewSet(viewsets.ModelViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = "slug"
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ["=name"]

    def get_queryset(self):
        slug = self.kwargs.get("slug", None)

        if slug is not None:
            queryset = Genre.objects.filter(slug=slug)

            if len(queryset) == 0:
                raise exceptions.MethodNotAllowed(self.request.method)

        return Genre.objects.all()
