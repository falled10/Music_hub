from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            'admin@mail.com',
            'adminpass123'
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email='test@mail.com',
            password='testpass123'
        )

    def test_users_listed(self):
        url = reverse('admin:authorization_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.email)

    def test_user_page_change(self):
        url = reverse('admin:authorization_user_change', args=[self.user.id])
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_create_user_page(self):
        url = reverse('admin:authorization_user_add')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
