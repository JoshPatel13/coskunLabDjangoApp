from rest_framework import serializers

from .models import InventoryItem
from .models import Order
from django import forms

# transformation from model to json
class InventoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'