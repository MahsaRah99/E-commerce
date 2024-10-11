from rest_framework import serializers

from .models import Cart, CartItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "price")


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = CartItem
        fields = ("product", "quantity")


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ("cart_items", "total_price")


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(min_value=1)
