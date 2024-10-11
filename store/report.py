from datetime import timedelta

from django.db.models import Sum
from django.utils import timezone

from .models import Cart


def daily_cart_statistics(start_date, end_date):
    if not start_date:
        start_date = timezone.now() - timedelta(days=3)
    if not end_date:
        end_date = timezone.now()

    queryset = (
        Cart.objects.filter(created_at__date__range=[start_date, end_date])
        .values(
            "created_at__date",
            "user__full_name",
        )
        .annotate(total_sum=Sum("total_price"))
        .order_by("created_at__date", "-total_sum")
    )

    return queryset
