from django.urls import path
from .views import (
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderItemCreateView,
    OrderItemDeleteView,
)

urlpatterns = [
    path("orders/", OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("order-items/create/", OrderItemCreateView.as_view(), name="orderitem_create"),
    path("order-items/<int:pk>/delete/", OrderItemDeleteView.as_view(), name="orderitem_delete"),
]
