from rest_framework import serializers

from products.models import Product
from orders.models import Project


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'name',
            'id',
        )


class ProjectSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Project
        fields = (
            'id',
            'product',
        )

