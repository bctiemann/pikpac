from rest_framework import serializers

from products.models import ProductCategory, Product, ProductPrice, Pattern, Paper
from orders.models import Project


class ProductCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCategory
        fields = (
            'id',
            'slug',
            'name',
            'picture',
        )


class ProductPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductPrice
        fields = (
            'product',
            'quantity',
            'unit_price',
        )


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    collapsibility = serializers.CharField(source='get_collapsibility_display')
    prices = ProductPriceSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'sku',
            'category',
            'pieces',
            'collapsibility',
            'picture',
            'prices',
        )


class PatternSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pattern
        fields = (
            'id',
            'name',
            'sku',
            'picture',
        )


class PaperSerializer(serializers.ModelSerializer):

    class Meta:
        model = Paper
        fields = (
            'id',
            'name',
            'sku',
            'picture',
        )


class ProjectSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Project
        fields = (
            'id',
            'product',
        )

