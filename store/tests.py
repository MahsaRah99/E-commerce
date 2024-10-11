from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from users.models import User

from .models import Cart, CartItem, Product


class CartTotalPriceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            full_name="testuser", phone_number="09111111111"
        )

        self.cart = Cart.objects.create(
            user=self.user,
            total_price=0,
            expiry_time=timezone.now() + timedelta(minutes=30),
        )

        self.product1 = Product.objects.create(
            name="Product 1", price=1000000, inventory=50
        )
        self.product2 = Product.objects.create(
            name="Product 2", price=200000, inventory=30
        )

    def test_cart_total_price_with_one_item(self):
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.cart.refresh_from_db()

        self.assertEqual(self.cart.total_price, 2000000)

    def test_cart_total_price_with_multiple_items(self):
        CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.product2, quantity=1)
        self.cart.refresh_from_db()

        self.assertEqual(self.cart.total_price, 2200000)

    def test_cart_total_price_after_updating_quantity(self):
        cart_item = CartItem.objects.create(
            cart=self.cart, product=self.product1, quantity=2
        )
        self.cart.refresh_from_db()

        cart_item.quantity = 3
        cart_item.save()
        self.cart.refresh_from_db()

        self.assertEqual(self.cart.total_price, 3000000)

    def test_cart_total_price_with_zero_items(self):
        self.cart.refresh_from_db()

        self.assertEqual(self.cart.total_price, 0)
