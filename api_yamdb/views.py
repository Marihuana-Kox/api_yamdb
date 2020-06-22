from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from users.models import CustomUser


class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField()


@api_view(["POST"])
def send_confirmation_code(request):
    serializer = SendEmailSerializer(data=request.data)

    if serializer.is_valid():
        username = serializer.data["username"]
        email = serializer.data["email"]
        try:
            user = CustomUser.objects.get(username=username, email=email)
        except ObjectDoesNotExist:
            user = CustomUser.objects.create_user(
                username=username, email=email, password="password3"
            )

        confirmation_code = default_token_generator.make_token(user)
        mail_subject = "Код подтверждения"
        message = f"Ваш код подтверждения: {confirmation_code}"
        send_mail(
            mail_subject,
            message,
            "Yamdb.ru <admin@yamdb.ru>",
            [email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    confirmation_code = serializers.CharField(required=True)


@api_view(["POST"])
def get_token(request):
    serializer = ConfirmationCodeSerializer(data=request.data)

    if serializer.is_valid():
        confirmation_code = serializer.data["confirmation_code"]
        email = serializer.data["email"]
        user = get_object_or_404(CustomUser, email=email)

        if default_token_generator.check_token(user, confirmation_code):
            token = AccessToken.for_user(user)
            return Response({"token": f"{token}"}, status=status.HTTP_200_OK)
        return Response(
            {"confirmation_code": "Неверный код подтверждения"},
            status=status.HTTP_400_BAD_REQUEST,
        )
