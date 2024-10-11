from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F
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
