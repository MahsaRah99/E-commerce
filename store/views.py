from django.core.exceptions import ValidationError
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Cart, CartItem, Product
from .pagination import CustomPagination
from .report import daily_cart_statistics
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

        cart, _ = Cart.objects.get_or_create(user=request.user, is_active=True)

        try:
            with transaction.atomic():
                cart_item, _ = CartItem.objects.get_or_create(
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
            .prefetch_related("items__product")
            .first()
        )


class DailyCartReportView(generics.ListAPIView):
    pagination_class = CustomPagination

    def get_queryset(self):
        start_date = self.request.query_params.get("start_date", None)
        end_date = self.request.query_params.get("end_date", None)

        queryset = daily_cart_statistics(start_date, end_date)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(self.format_report(page))

        return Response(self.format_report(queryset))

    def format_report(self, queryset):
        """
        Format the queryset into the required report structure.
        """
        report = {}
        for item in queryset:
            date = item["created_at__date"].strftime("%Y-%m-%d")
            full_name = item["user__full_name"]
            total_sum = item["total_sum"]

            if date not in report:
                report[date] = []

            report[date].append(f"{full_name} -> {total_sum}")

        return report
