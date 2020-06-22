from django.shortcuts import get_object_or_404
from rest_framework import exceptions, permissions, viewsets

from content.models import Title
from users.models import CustomUser

from .models import Comment, Review
from .permissions import CustomPermissions
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    permission_classes = [CustomPermissions]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))
        author = get_object_or_404(CustomUser, pk=self.request.user.id)

        if Review.objects.filter(author=author, title=title).exists():
            raise exceptions.ValidationError

        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CustomPermissions]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get("review_id"))
        author = get_object_or_404(CustomUser, pk=self.request.user.id)

        serializer.save(author=author, review=review)
