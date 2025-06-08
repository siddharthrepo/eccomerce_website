from rest_framework import serializers
from store.models import OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    vendor_name = serializers.CharField(source="product.vendor.vendor_name", read_only=True)
    order_status = serializers.CharField(source="order.status", read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product_name', 'vendor_name', 'order_status', 'quantity', 'date_added']
