from django.contrib import admin

from .models import Cart, CartItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "inventory")
    search_fields = ("name",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "total_price",
        "created_at",
        "is_active",
        "expiry_time",
    )
    search_fields = ("user__full_name",)
    list_filter = ("is_active",)


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "product", "quantity")
