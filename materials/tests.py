from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import AccessToken

from materials.models import Course, Lesson, Subscription
from users.models import User


# ===== Секция курсов ===============================================
class CourseTestCase(APITestCase):

    def setUp(self):
        """Установка и создание начальных параметров для тестов"""
        self.user = User.objects.create(email="user@mail.ru", is_staff=True)
        self.course = Course.objects.create(
            title="test_course_title",
            owner=self.user,
            description="tst_course_description",
        )
        self.lesson = Lesson.objects.create(
            title="test_lesson_title",
            course=self.course,
            owner=self.user,
            description="tst_lesson_description",
        )
        self.subscribed = Subscription.objects.create(
            course=self.course, user=self.user
        )

        self.access_token = str(AccessToken.for_user(self.user))
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_course_retrieve(self):
        """Тест на получение отдельной записи курса"""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.course.title)

    def test_course_create(self):
        """Тест на создание новой записи курса"""
        url = reverse("materials:course-list")
        data = {
            "title": "Название курса",
            "description": "Описание курса",
            "owner": self.user,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_update(self):
        """Тест на изменение отдельной записи курса"""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {"title": "Новое название курса"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Новое название курса")

    def test_course_delete(self):
        """Тест на удаление отдельной записи курса"""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        """Тест на получение списка курсов"""
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()
        result = data["results"]
        server_answer = [
            {
                "id": self.course.pk,
                "title": self.course.title,
                "description": self.course.description,
                "lessons_count": 1,
                "lessons": [
                    {
                        "id": self.lesson.pk,
                        "title": self.lesson.title,
                        "description": self.lesson.description,
                    }
                ],
                "is_subscribed": True,
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result, server_answer)

    def test_subscription(self):
        """Тест на проверку работы установки/удалении подписки"""
        url = reverse("materials:subscription", args=(self.course.pk,))
        print(url)
        data = {"id": self.course.pk}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Подписка удалена.")


# ===== Секция уроков ===============================================
class LessonTestCase(APITestCase):

    def setUp(self):
        """Установка и создание начальных параметров для тестов"""
        self.user = User.objects.create(email="user@mail.ru", is_staff=True)
        self.course = Course.objects.create(
            title="test_course_title",
            owner=self.user,
            description="tst_course_description",
        )
        self.lesson = Lesson.objects.create(
            title="test_lesson_title",
            course=self.course,
            owner=self.user,
            description="tst_lesson_description",
        )
        self.access_token = str(AccessToken.for_user(self.user))
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_lesson_retrieve(self):
        """Тест на получение отдельной записи урока"""
        url = reverse("materials:lesson-retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        """Тест на создание новой записи урока"""
        url = reverse("materials:lesson-create")
        data = {
            "title": "Название урока",
            "course": self.course.pk,
            "video": "www.rutube.ru",
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        """Тест на изменение отдельной записи урока"""
        url = reverse("materials:lesson-update", args=(self.lesson.pk,))
        data = {"title": "Новое название урока"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Новое название урока")

    def test_lesson_delete(self):
        """Тест на удаление отдельной записи урока"""
        url = reverse("materials:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        """Тест на получение списка уроков"""
        url = reverse("materials:lesson-list")
        response = self.client.get(url)
        data = response.json()
        result = data["results"]
        print(result)
        server_answer = [
            {
                "id": self.lesson.pk,
                "video": self.lesson.video,
                "title": self.lesson.title,
                "description": self.lesson.description,
                "image": None,
                "course": self.course.pk,
                "owner": self.user.pk,
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(result, server_answer)
