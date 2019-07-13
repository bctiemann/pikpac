from rest_framework import serializers

from products.models import ProductCategory, Product
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

class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    collapsibility = serializers.CharField(source='get_collapsibility_display')

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
        )


class ProjectSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Project
        fields = (
            'id',
            'product',
        )

