from django_filters import rest_framework as filters
from users.models import Payment


class PaymentFilter(filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            'paid_course': ['exact'],
            'paid_lesson': ['exact'],
            'payment_method': ['exact'],
            'payment_date': ['gte', 'lte'],
        }
