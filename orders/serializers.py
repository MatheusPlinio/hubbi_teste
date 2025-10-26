from rest_framework import serializers
from .models import Order, OrderItem
from inventory.models import Part
from inventory.serializers import PartSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    piece = PartSerializer(read_only=True)
    piece_id = serializers.PrimaryKeyRelatedField(
        queryset=Part.objects.all(),
        source="piece",
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "piece",
            "piece_id",
            "quantity",
            "unit_price",
            "subtotal",
        ]
        read_only_fields = ["subtotal"]


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "status",
            "total_price",
            "created_at",
            "updated_at",
            "items",
        ]
        read_only_fields = ["total_price", "created_at", "updated_at"]
