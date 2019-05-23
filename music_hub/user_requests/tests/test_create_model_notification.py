from unittest.mock import patch

from django.urls import reverse

from music_hub.test_utils import APITestUser
from user_requests.tasks import notify_recipient


class TestRequestNotification(APITestUser):

    def setUp(self):
        self.user = self.create_and_authorize('test@gmail.com', 'testpass123')

    @patch('user_requests.tasks.notify_recipient.delay')
    def test_recipient_get_notify_if_request_create(self, delay):
        data = {
            'title': 'Some new title',
            'body': 'Some new body',
            'recipient': self.user.id
        }
        resp = self.client.post(reverse('requests-list'), data)
        self.assertEqual(resp.status_code, 201)
        delay.assert_called_once()

    @patch('django.core.mail.EmailMultiAlternatives.send')
    def test_notify_will_called(self, send):
        notify_recipient("some title", "some body", self.user.id, self.user.id)
        send.assert_called_once()

    @patch('user_requests.tasks.notify_recipient.delay')
    def test_get_error_anon_user_try_create_request(self, send):
        self.logout()
        data = {
            'title': 'Some new title',
            'body': 'Some new body',
            'recipient': self.user.id
        }
        resp = self.client.post(reverse('requests-list'), data=data)
        self.assertEqual(resp.status_code, 401)

    @patch('user_requests.tasks.notify_recipient.delay')
    def test_get_error_if_user_try_to_create_invalid_request(self, send):
        data = {
            'title': '',
            'body': '',
            'recipient': self.user.id
        }
        resp = self.client.post(reverse('requests-list'), data=data)
        self.assertEqual(resp.status_code, 400)
