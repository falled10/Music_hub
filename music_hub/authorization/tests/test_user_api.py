import json

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from music_hub.test_utils import APITestUser


CREATE_USER_URL = reverse('authorization:auth-register')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        resp = self.client.post(CREATE_USER_URL, data=json.dumps({
            'email': 'test@mail.com',
            'password': 'testpass123',
            'name': 'Test_user'
        }), content_type='application/json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(**resp.data)

        self.assertTrue(user.check_password('testpass123'))
        self.assertNotIn('password', resp.data)

    def test_user_exists(self):
        payload = {
            'email': 'test@mail.com',
            'password': 'testpass123',
            'name': 'TestName'
        }
        create_user(**payload)
        resp = self.client.post(CREATE_USER_URL, data=json.dumps(payload),
                                content_type='application/json')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        payload = {
            'email': 'test@mail.com',
            'password': 'pw'
        }

        resp = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()

        self.assertFalse(user_exist)


class AuthLoginUserTest(TestCase):

    client = APIClient()

    def login_a_user(self, email='', password=''):
        url = reverse('authorization:auth-login')
        return self.client.post(url, data=json.dumps({
            'email': email,
            'password': password
        }), content_type='application/json')

    def setUp(self):
        self.user = get_user_model().objects.create_superuser(
            email="test@mail.com",
            password="testpass123",
        )

    def test_login_user_with_valid_credentials(self):
        resp = self.login_a_user('test@mail.com', 'testpass123')

        self.assertIn('access', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        resp = self.login_a_user('anonymous', 'pass')

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class UserTests(APITestUser):

    def setUp(self):
        self.client = APIClient()
        self.user = self.create_and_authorize('test@gmail.com', 'testpass123')

    def test_get_user_successful(self):
        resp = self.client.get(reverse('authorization:auth-user'))
        self.assertEqual(self.user.email, resp.data['email'])
        self.assertEqual(resp.status_code, 200)
