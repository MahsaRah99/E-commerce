from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Sum
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    name = models.CharField(_("Name"), max_length=150)
    inventory = models.PositiveIntegerField(_("Inventory"))
    price = models.PositiveIntegerField(_("Price"))

    def __str__(self):
        return self.name

    def is_available(self) -> bool:
        return self.inventory > 0

    def reduce_inventory(self, quantity: int) -> None:
        """Reduces the inventory of the product."""
        affected_rows = Product.objects.filter(
            id=self.id, inventory__gte=quantity
        ).update(inventory=F("inventory") - quantity)

        if affected_rows == 0:
            raise ValidationError("Not enough inventory available")


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField(_("Total price"), default=0)
    created_at = models.DateTimeField(_("Updated at"), auto_now_add=True)
    is_active = models.BooleanField(_("Is active"), default=True)
    expiry_time = models.DateTimeField(_("Expiry time"), null=True, db_index=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.expiry_time = timezone.now() + timedelta(minutes=30)
        self.calculate_total_price()
        super().save(*args, **kwargs)

    def calculate_total_price(self):
        if self.pk:
            self.total_price = (
                self.items.annotate(
                    item_total=F("product__price") * F("quantity")
                ).aggregate(total=Sum("item_total"))["total"]
                or 0
            )


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="cart_items", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(_("Quantity"), default=0)

    def increase_quantity(self, quantity: int) -> None:
        """Incrementing quantity and reducing inventory atomically."""
        self.product.reduce_inventory(quantity)

        self.quantity += quantity
        self.save(update_fields=["quantity"])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.cart.save()
