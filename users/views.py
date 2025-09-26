from rest_framework import viewsets, generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.shortcuts import get_object_or_404

from .models import Payment, CustomUser
from .serializers import PaymentSerializer, UserSerializer, UserRegisterSerializer
from .filters import PaymentFilter
from .permissions import IsOwner
from .services import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_session,
    get_stripe_session_status,
)
from courses.models import Course, Lesson


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PaymentFilter
    ordering_fields = ["payment_date", "amount"]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Payment.objects.all()  # ← ДОБАВЬТЕ ЭТУ СТРОКУ

    def get_queryset(self):
        # Пользователь видит ТОЛЬКО свои платежи
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserRegisterAPIView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreatePaymentAPIView(APIView):
    """Создание платежа и сессии оплаты через Stripe"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        lesson_id = request.data.get("lesson_id")

        if not course_id and not lesson_id:
            return Response(
                {"error": "Необходимо указать course_id или lesson_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Определяем продукт и сумму
        if course_id:
            course = get_object_or_404(Course, id=course_id)
            product_name = course.title
            amount = 10000  # 10000 рублей за курс
        else:
            lesson = get_object_or_404(Lesson, id=lesson_id)
            product_name = lesson.title
            amount = 1000  # 1000 рублей за урок

        # Создаем платеж в нашей системе
        payment = Payment.objects.create(
            user=request.user,
            paid_course_id=course_id,
            paid_lesson_id=lesson_id,
            amount=amount,
            payment_method="stripe",
            payment_status="pending",
        )

        try:
            # Создаем продукт и цену в Stripe
            product_id = create_stripe_product(product_name, f"Оплата {product_name}")
            price_id = create_stripe_price(product_id, amount)

            # Создаем сессию оплаты
            success_url = (
                f"http://localhost:8000/api/payment/success/?payment_id={payment.id}"
            )
            cancel_url = "http://localhost:8000/api/payment/cancel/"
            payment_url, session_id = create_stripe_session(
                price_id, success_url, cancel_url
            )

            # Сохраняем данные Stripe в платеж
            payment.stripe_product_id = product_id
            payment.stripe_price_id = price_id
            payment.stripe_session_id = session_id
            payment.payment_url = payment_url
            payment.save()

            return Response(
                {"payment_id": payment.id, "payment_url": payment_url, "amount": amount}
            )

        except Exception as e:
            payment.delete()  # Удаляем неудачный платеж
            return Response(
                {"error": f"Ошибка создания платежа: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PaymentStatusAPIView(APIView):
    """Проверка статуса платежа"""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id, user=request.user)

        if payment.stripe_session_id:
            try:
                status = get_stripe_session_status(payment.stripe_session_id)
                payment.payment_status = "paid" if status == "paid" else "pending"
                payment.save()

                return Response(
                    {
                        "payment_id": payment.id,
                        "status": payment.payment_status,
                        "stripe_status": status,
                    }
                )
            except Exception as e:
                return Response(
                    {"error": f"Ошибка проверки статуса: {str(e)}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response({"payment_id": payment.id, "status": payment.payment_status})
