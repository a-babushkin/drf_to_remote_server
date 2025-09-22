import django_filters

from users.models import Payment


class PaymentFilter(django_filters.FilterSet):
    payment_date = django_filters.DateFromToRangeFilter(field_name="payment_date")
    payment_method = django_filters.ChoiceFilter(
        choices=(("cash", "Наличные"), ("transfer", "Перевод"))
    )

    class Meta:
        model = Payment
        fields = ["payment_method"]
