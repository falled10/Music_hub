from django.urls import reverse

from lessons.models import Lessons, Likes
from music_hub.test_utils import APITestUser
from lessons.serializers import LessonsSerializer


def create_lesson(user):
    lesson = Lessons.objects.create(title='Test title',
                                    body='Test body',
                                    owner=user)
    return lesson


class TestLikeSystem(APITestUser):

    def setUp(self):
        self.user = self.create_and_authorize('test@gmail.com', 'testpass132')
        self.lesson = create_lesson(self.user)

    def test_like_create_successful(self):
        resp = self.client.post(reverse('lessons-likes',
                                        args=[self.lesson.slug]))
        self.assertEqual(resp.status_code, 201)
        like_exists = Likes.objects.filter(lesson=self.lesson,
                                           liker=self.user).exists()
        self.assertTrue(like_exists)

    def test_like_deleted_successful_if_post_second_time(self):
        Likes.objects.create(lesson=self.lesson, liker=self.user)
        resp = self.client.post(reverse('lessons-likes',
                                        args=[self.lesson.slug]))
        like_exists = Likes.objects.filter(lesson=self.lesson,
                                           liker=self.user).exists()
        self.assertEqual(resp.status_code, 204)
        self.assertFalse(like_exists)

    def test_error_if_anon_try_to_like(self):
        self.logout()
        resp = self.client.post(reverse('lessons-likes',
                                        args=[self.lesson.slug]))
        self.assertEqual(resp.status_code, 401)

    def test_get_all_likes_from_lesson(self):
        self.client.post(reverse('lessons-likes', args=[self.lesson.slug]))
        resp = self.client.get(reverse('lessons-likes',
                                       args=[self.lesson.slug]))
        self.assertEqual(resp.status_code, 200)
        expect = LessonsSerializer(self.lesson).data['likes']
        self.assertEqual(expect, resp.data)

    def test_get_error_if_anon_user_get_likes(self):
        self.logout()
        resp = self.client.get(reverse('lessons-likes',
                                       args=[self.lesson.slug]))
        self.assertEqual(resp.status_code, 401)
