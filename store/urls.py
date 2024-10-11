from django.urls import path

from . import views

app_name = "store"

urlpatterns = [
    path("cart/add/", views.AddToCartView.as_view(), name="add_item_to_cart"),
    path("cart/checkout/", views.MyCartView.as_view(), name="my_cart"),
    path("carts/report/", views.DailyCartReportView.as_view(), name="carts_report"),
]
