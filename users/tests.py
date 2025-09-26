from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import Payment
from courses.models import Course, Lesson

CustomUser = get_user_model()


class CustomUserModelTests(TestCase):
    """Тесты для модели CustomUser"""

    def test_create_user(self):
        """Тест создания обычного пользователя"""
        user = CustomUser.objects.create_user(
            email="test@example.com", password="testpass123"
        )

        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("testpass123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        superuser = CustomUser.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )

        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)


class PaymentModelTests(TestCase):
    """Тесты для модели Payment"""

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        # ✅ Добавлен owner
        self.course = Course.objects.create(title="Test Course", owner=self.user)

    def test_create_payment(self):
        """Тест создания платежа"""
        payment = Payment.objects.create(
            user=self.user,
            paid_course=self.course,
            amount=10000,
            payment_method="transfer",
        )

        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.paid_course, self.course)
        self.assertEqual(payment.amount, 10000)
        self.assertEqual(payment.payment_method, "transfer")


class UserAPITests(APITestCase):
    """Тесты API для пользователей"""

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="testpass123"
        )

    def test_user_registration(self):
        """Тест регистрации пользователя"""
        url = reverse("user-register")
        data = {
            "email": "newuser@example.com",
            "password": "newpass123",
            "phone": "+79991234567",
            "city": "Москва",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что пользователь создан
        self.assertTrue(CustomUser.objects.filter(email="newuser@example.com").exists())

    def test_user_list_authenticated(self):
        """Тест получения списка пользователей"""
        self.client.force_authenticate(user=self.user)
        url = reverse("user-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_detail_authenticated(self):
        """Тест получения деталей пользователя"""
        self.client.force_authenticate(user=self.user)
        url = reverse("user-detail", kwargs={"pk": self.user.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_user_update_authenticated(self):
        """Тест обновления пользователя"""
        self.client.force_authenticate(user=self.user)
        url = reverse("user-update", kwargs={"pk": self.user.pk})
        data = {"phone": "+79998887766", "city": "Казань"}

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertEqual(self.user.phone, "+79998887766")


class PaymentAPITests(APITestCase):
    """Тесты API для платежей"""

    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        self.other_user = CustomUser.objects.create_user(
            email="other@example.com", password="otherpass123"
        )

        # ✅ Добавлен owner
        self.course = Course.objects.create(title="Test Course", owner=self.user)
        self.payment = Payment.objects.create(
            user=self.user,
            paid_course=self.course,
            amount=10000,
            payment_method="transfer",
        )

    def test_payment_list_authenticated(self):
        """Тест получения списка платежей"""
        self.client.force_authenticate(user=self.user)
        url = reverse("payment-list")

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payment_create_authenticated(self):
        """Тест создания платежа"""
        self.client.force_authenticate(user=self.user)
        url = reverse("payment-list")
        data = {
            "paid_course": self.course.id,
            "amount": 15000,
            "payment_method": "cash",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 2)

    def test_payment_detail_owner(self):
        """Тест получения деталей платежа владельцем"""
        self.client.force_authenticate(user=self.user)
        url = reverse("payment-detail", kwargs={"pk": self.payment.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payment_detail_not_owner(self):
        """Тест получения деталей платежа не владельцем"""
        self.client.force_authenticate(user=self.other_user)
        url = reverse("payment-detail", kwargs={"pk": self.payment.pk})

        response = self.client.get(url)
        # Должен вернуть 404, так как платеж принадлежит другому пользователю
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
