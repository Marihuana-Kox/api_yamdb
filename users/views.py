from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets

from .models import CustomUser
from .permissions import IsAdminOrReadOnly
from .serializers import CustomUserSerializer


class CustomUsersViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    lookup_field = "username"

    def get_queryset(self):
        username = self.kwargs.get("username", None)

        if username is None:
            return CustomUser.objects.all()

        return CustomUser.objects.filter(username=username)


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(CustomUser, username=self.request.user.username)
        return obj
