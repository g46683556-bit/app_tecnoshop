from rest_framework import serializers
from .models import Catalog

class CatalogSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()
    has_discount = serializers.SerializerMethodField()

    class Meta:
        model = Catalog
        fields = [
            'id',
            'name',
            'description',
            'price',
            'final_price',
            'discount_percent',
            'discount_price',
            'has_discount',
            'stock',
            'image_url',
            'category',
        ]

    def get_final_price(self, obj):
        return obj.final_price

    def get_has_discount(self, obj):
        return obj.final_price < obj.price
