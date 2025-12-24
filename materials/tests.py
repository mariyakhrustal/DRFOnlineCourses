from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.moderator = User.objects.create(email="moder@test.ru")
        self.moderator.groups.create(name="moders")
        self.course = Course.objects.create(name="Курс Python", owner=self.user)
        self.lesson = Lesson.objects.create(
            name="Урок 1", course=self.course, owner=self.user
        )

    def test_lesson_retrieve(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["name"], self.lesson.name)

    def test_lesson_retrieve_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lessons_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["name"], self.lesson.name)

    def test_lesson_create(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_create")
        data = {"name": "Новый урок", "course": self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_create_moderator_forbidden(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lessons_create")
        response = self.client.post(
            url, {"name": "Запрещено", "course": self.course.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_update(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"name": "Новый урок 123", "course": self.course.pk}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["name"], "Новый урок 123")

    def test_lesson_update_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        response = self.client.patch(url, {"name": "Исправлено модератором"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data["name"], "Исправлено модератором")

    def test_lesson_update_not_owner_forbidden(self):
        other_user = User.objects.create(email="other@test.ru")
        self.client.force_authenticate(user=other_user)
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        response = self.client.patch(url, {"name": "Запрещено"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_lesson_delete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_lesson_delete_moderator_forbidden(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_lesson_delete_not_owner_forbidden(self):
        other_user = User.objects.create(email="other@test.ru")
        self.client.force_authenticate(user=other_user)
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_lesson_list(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": None,
                    "image": None,
                    "video_link": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(data, result)

    def test_lesson_list_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": None,
                    "image": None,
                    "video_link": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(data, result)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email="test@test.ru")
        self.course = Course.objects.create(name="Python", owner=self.user)
        self.url = reverse("materials:subscription")
        self.moderator = User.objects.create(email="moder@test.ru")
        self.moderator.groups.create(name="moders")

    def test_create_subscription(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {"course_id": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
        self.assertEqual(response.data["message"], "Подписка добавлена")

    def test_delete_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {"course_id": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            Subscription.objects.filter(user=self.user, course=self.course).exists()
        )
        self.assertEqual(response.data["message"], "Подписка удалена")

    def test_subscription_without_course_id(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "course_id обязателен")

    def test_subscription_unauthorized(self):
        response = self.client.post(self.url, {"course_id": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_subscription_moderator(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(self.url, {"course_id": self.course.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
