from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem, Product
from .serializers import AddToCartSerializer, CartSerializer


class AddToCartView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        product = get_object_or_404(Product, id=product_id)
        if not product.is_available:
            return Response(
                {"error": "Item is not available"}, status=status.HTTP_400_BAD_REQUEST
            )

        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)

        try:
            with transaction.atomic():
                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart, product=product
                )
                cart_item.increase_quantity(quantity)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class MyCartView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer

    def get_object(self):
        return (
            Cart.objects.filter(user=self.request.user, is_active=True)
            .prefetch_related("cartitem_set__product")
            .first()
        )
