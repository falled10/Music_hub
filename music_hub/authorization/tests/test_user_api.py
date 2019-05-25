import json
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from music_hub.test_utils import APITestUser

CREATE_USER_URL = reverse('authorization:auth-register')


@patch('authorization.tasks.send_verification_email.delay')
def create_user(delay, **kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()

    @patch('authorization.tasks.send_verification_email.delay')
    def test_create_valid_user_success(self, delay):
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
        return self.client.post(url, {
            'email': email,
            'password': password
        })

    @patch('authorization.tasks.send_verification_email.delay')
    def setUp(self, delay):
        self.user = get_user_model().objects.create_superuser(
            email="test@mail.com",
            password="testpass123",
        )

    def test_login_user_with_valid_credentials(self):
        self.client.get(reverse('authorization:verify',
                                args=[self.user.verification_uuid]))
        resp = self.login_a_user('test@mail.com', 'testpass123')

        self.assertIn('access', resp.data)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_login_user_with_invalid_credentials(self):
        resp = self.login_a_user(email='anonymous@mail.com', password='pass')

        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)


class UserTests(APITestUser):

    def setUp(self):
        self.client = APIClient()
        self.user = self.create_and_authorize('test@gmail.com', 'testpass123')

    def test_get_user_successful(self):
        resp = self.client.get(reverse('authorization:auth-user'))
        self.assertEqual(self.user.email, resp.data['email'])
        self.assertEqual(resp.status_code, 200)

    def test_get_all_user_successful(self):
        resp = self.client.get(reverse('authorization:users-list'))
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('authorization:users-detail',
                                       args=[self.user.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['email'], self.user.email)

    def test_unsafe_methods_error(self):
        resp = self.client.post(reverse('authorization:users-list'), {
            'email': 'test@gmail.com',
            'name': 'test user',
            'password': 'testpass123'
        })
        self.assertEqual(resp.status_code, 403)
        resp = self.client.delete(reverse('authorization:users-detail',
                                          args=[self.user.id]))
        self.assertEqual(resp.status_code, 403)
        resp = self.client.put(reverse('authorization:users-detail',
                                       args=[self.user.id]),
                               {
                                   'email': 'test@gmail.com',
                                   'name': 'somename',
                                   'password': 'somepass'
                               })
        self.assertEqual(resp.status_code, 403)
