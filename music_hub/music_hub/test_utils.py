from unittest.mock import patch

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken


class APITestUser(APITestCase):

    @patch('authorization.tasks.send_verification_email.delay')
    def create_user(self, email, password, delay):
        user = get_user_model().objects.create_user(email, password)
        user.is_active = True
        user.save()
        return user

    def authorize(self, user, **additional_headers):
        token = AccessToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'{api_settings.AUTH_HEADER_TYPES[0]} {token}',
            **additional_headers
        )

    def create_and_authorize(self, email, password, **additional_headers):
        user = self.create_user(email, password)
        self.authorize(user, **additional_headers)
        return user

    def logout(self, **additional_headers):
        self.client.credentials(**additional_headers)
