from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from .models import Course, Lesson, Subscription

User = get_user_model()


class CourseLessonTestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass123'
        )

        # Создаем модератора (is_staff=True)
        self.moderator = User.objects.create_user(
            email='moderator@example.com',
            password='modpass123',
            is_staff=True
        )

        # Создаем администратора
        self.admin = User.objects.create_user(
            email='admin@example.com',
            password='adminpass123',
            is_staff=True,
            is_superuser=True
        )

        # Создаем курс
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

        # Создаем урок
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            course=self.course,
            owner=self.user,
            video_url='https://www.youtube.com/watch?v=test123'
        )

    def test_lesson_youtube_validation(self):
        """Тестируем валидацию YouTube ссылок"""
        self.client.force_authenticate(user=self.user)

        # Пытаемся создать урок с невалидной ссылкой
        data = {
            'title': 'Invalid URL Lesson',
            'description': 'Test',
            'course': self.course.id,
            'video_url': 'https://vk.com/video123'
        }

        response = self.client.post(
            reverse('lesson-list'),
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('video_url', response.data)

    def test_subscription_flow(self):
        """Тестируем работу подписок"""
        self.client.force_authenticate(user=self.user)

        # Добавляем подписку
        response = self.client.post(
            reverse('subscribe'),
            {'course_id': self.course.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

        # Удаляем подписку
        response = self.client.post(
            reverse('subscribe'),
            {'course_id': self.course.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

    def test_course_list_pagination(self):
        """Тестируем пагинацию"""
        self.client.force_authenticate(user=self.user)

        # Создаем несколько курсов для тестирования пагинации
        for i in range(15):
            Course.objects.create(
                title=f'Course {i}',
                description=f'Description {i}',
                owner=self.user
            )

        response = self.client.get(
            reverse('course-list') + '?page=2&page_size=5'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 5)

    def test_lesson_crud_permissions(self):
        """Тестируем права доступа для уроков"""
        # Анонимный пользователь не может просматривать
        response = self.client.get(reverse('lesson-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Обычный пользователь может просматривать
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('lesson-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Модератор (is_staff) может редактировать
        self.client.force_authenticate(user=self.moderator)
        data = {'title': 'Updated Lesson'}
        response = self.client.patch(
            reverse('lesson-detail', args=[self.lesson.id]),
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )

    def test_subscription_creation(self):
        """Тестируем создание подписки"""
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            reverse('subscribe'),
            {'course_id': self.course.id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )

    def test_subscription_unique(self):
        """Тестируем уникальность подписки"""
        self.client.force_authenticate(user=self.user)

        # Первая подписка
        self.client.post(
            reverse('subscribe'),
            {'course_id': self.course.id}
        )

        # Вторая попытка подписаться - должна удалить подписку
        response = self.client.post(
            reverse('subscribe'),
            {'course_id': self.course.id}
        )

        self.assertEqual(response.data['message'], 'Подписка удалена')
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                course=self.course
            ).exists()
        )


class BasicCourseAPITest(APITestCase):
    """Базовые тесты API курсов для CI/CD"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_course_list_available(self):
        """Тест доступности списка курсов"""
        url = reverse('course-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_course_detail_available(self):
        """Тест доступности детальной информации курса"""
        url = reverse('course-detail', kwargs={'pk': self.course.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class BasicLessonAPITest(APITestCase):
    """Базовые тесты API уроков для CI/CD"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title='Test Lesson',
            description='Test Lesson Description',
            course=self.course,
            owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_list_available(self):
        """Тест доступности списка уроков"""
        url = reverse('lesson-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_lesson_detail_available(self):
        """Тест доступности детальной информации урока"""
        url = reverse('lesson-detail', kwargs={'pk': self.lesson.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SimpleModelTest(TestCase):
    """Простой тест моделей для CI/CD"""

    def test_course_creation(self):
        """Тест создания курса"""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123'
        )
        course = Course.objects.create(
            title='Simple Test Course',
            description='Simple Test Description',
            owner=user
        )
        self.assertEqual(course.title, 'Simple Test Course')
        self.assertEqual(course.owner, user)
