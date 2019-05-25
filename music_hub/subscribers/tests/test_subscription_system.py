from unittest.mock import patch

from django.urls import reverse

from music_hub.test_utils import APITestUser


class SubscribeTest(APITestUser):

    @patch('authorization.tasks.send_verification_email.delay')
    def setUp(self, delay):
        self.user = self.create_and_authorize('test@gmail.com', 'testpass132')
        self.other_user = self.create_user('other_user@gmail.com',
                                           'testpass123')

    def test_subscribe_successful(self):
        resp = self.client.post(reverse('authorization:subscribe',
                                        args=[self.other_user.id]))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual({'user': self.other_user.id,
                          'subscriber': self.user.id}, resp.data)

    def test_unsubscribe_successful(self):
        self.client.post(reverse('authorization:subscribe',
                                 args=[self.other_user.id]))
        resp = self.client.post(reverse('authorization:subscribe',
                                        args=[self.other_user.id]))
        self.assertEqual(resp.status_code, 400)
        resp = self.client.post(reverse('authorization:unsubscribe',
                                        args=[self.other_user.id]))
        self.assertEqual(resp.status_code, 204)

    def test_subscribe_to_self_unsuccessful(self):
        resp = self.client.post(reverse('authorization:subscribe',
                                        args=[self.user.id]))
        self.assertEqual(resp.status_code, 400)

    def test_anon_subscribe_unsuccessful(self):
        self.logout()
        resp = self.client.post(reverse('authorization:subscribe',
                                        args=[self.other_user.id]))
        self.assertEqual(resp.status_code, 401)

    def test_anon_unsubscribe_unsuccessful(self):
        self.logout()
        resp = self.client.post(reverse('authorization:unsubscribe',
                                        args=[self.other_user.id]))
        self.assertEqual(resp.status_code, 401)
