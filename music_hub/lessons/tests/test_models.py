from django.urls import reverse

from lessons.models import Lessons
from music_hub.test_utils import APITestUser


def create_lesson(user):
    lesson = Lessons.objects.create(title='New title', body='New body',
                                    owner=user)
    return lesson


class LessonModelsTests(APITestUser):

    def setUp(self):
        self.user = self.create_and_authorize('test@gmail.com', 'testpass123')
        self.lesson = create_lesson(self.user)

    def test_lesson_create_with_user_owner(self):
        lesson_data = {
            'title': 'New Lesson',
            'body': 'Body for test lesson'
        }
        resp = self.client.post(reverse('lessons-list'), lesson_data)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.data['owner']['id'], self.user.id)

    def test_lesson_not_create_with_anonymous_user(self):
        self.logout()
        lesson_data = {
            'title': 'New Lesson',
            'body': 'Body for test lesson'
        }
        resp = self.client.post(reverse('lessons-list'), lesson_data)
        self.assertEqual(resp.status_code, 401)

    def test_lesson_not_create_bad_data(self):
        lesson_data = {
            'title': '',
            'body': ''
        }
        resp = self.client.post(reverse('lessons-list'), lesson_data)
        self.assertEqual(resp.status_code, 400)

    def test_lesson_update_success(self):
        lesson_new_data = {
            'title': 'Updated title',
            'body': 'Updated body'
        }
        resp = self.client.put(reverse('lessons-detail',
                                       args=[self.lesson.slug]),
                               lesson_new_data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['title'], lesson_new_data['title'])

    def test_anonym_user_lesson_update_error(self):
        self.logout()
        lesson_new_data = {
            'title': 'Updated title'
        }
        resp = self.client.put(reverse('lessons-detail',
                                       args=[self.lesson.id]),
                               lesson_new_data)
        self.assertEqual(resp.status_code, 401)

    def test_not_owner_user_lesson_update_error(self):
        self.user = self.create_and_authorize('another@gmail.com', 'another')
        lesson_new_data = {
            'title': 'Updated title'
        }
        resp = self.client.put(reverse('lessons-detail',
                                       args=[self.lesson.slug]),
                               lesson_new_data)
        self.assertEqual(resp.status_code, 403)

    def test_lesson_delete_success(self):
        resp = self.client.delete(reverse('lessons-detail',
                                          args=[self.lesson.slug]))
        resp = self.client.get(reverse('lessons-detail',
                                       args=[self.lesson.slug]))

        self.assertEqual(resp.status_code, 404)

    def test_anon_user_delete_error(self):
        self.logout()
        resp = self.client.delete(reverse('lessons-detail',
                                          args=[self.lesson.slug]))

        self.assertEqual(resp.status_code, 401)

    def test_other_user_delete_error(self):
        self.user = self.create_and_authorize('another@gmail.com', 'another')
        resp = self.client.delete(reverse('lessons-detail',
                                          args=[self.lesson.slug]))

        self.assertEqual(resp.status_code, 403)
