from rest_framework import serializers

from products.models import ProductCategory, Product, ProductPrice, Pattern, Paper
from orders.models import Project, Order
from faq.models import FaqCategory, FaqHeading, FaqItem


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
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(source='product',  queryset=Product.objects.all(), )

    class Meta:
        model = Project
        fields = (
            'id',
            'title',
            'product',
            'product_id',
            'unit_price',
            'quantity',
        )


class OrderSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = Project
        fields = (
            'id',
            'project',
            'date_created',
        )


class FaqCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FaqCategory
        fields = (
            'id',
            'name',
            'sort_order',
        )


class FaqItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = FaqItem
        fields = (
            'id',
            'title',
            'body',
            'sort_order',
        )


class FaqHeadingSerializer(serializers.ModelSerializer):
    items = FaqItemSerializer(many=True)

    class Meta:
        model = FaqHeading
        fields = (
            'id',
            'title',
            'sort_order',
            'items',
        )

