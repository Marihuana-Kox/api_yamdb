from django.core import mail
from django.shortcuts import get_object_or_404
from django.test import Client, TestCase

from .models import CustomUser


# Пользователь регистрируется и ему отправляется письмо с подтверждением регистрации
class SendEmail(TestCase):
    def test_send_email(self):
        self.client = Client()
        self.client.post(
            "api/v1/auth/email/",
            {"username": "testverytest", "email": "testtest@test.me"},
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].email, "testtest@test.me")
