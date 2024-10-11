from celery import shared_task
from django.db import transaction
from django.utils import timezone

from .models import Cart, Product


@shared_task
def deactive_expired_carts():
    now = timezone.now()
    expired_carts = Cart.objects.filter(
        is_active=True, expiry_time__lt=now
    ).prefetch_related("items__product")

    with transaction.atomic():
        for cart in expired_carts:
            for item in cart.items.all():
                item.product.inventory += item.quantity

            Product.objects.bulk_update(
                [item.product for item in cart.items.all()], ["inventory"]
            )

            cart.is_active = False
            cart.save()
