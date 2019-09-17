from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import User, Address, Card
from products.models import ProductCategory, Product, ProductPrice, Template, Pattern, Paper
from orders.models import Project, Order, Design, DesignElement, ShippingOption
from faq.models import FaqCategory, FaqHeading, FaqItem


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = (
            'id',
            'full_name',
            'address_1',
            'address_2',
            'country',
            'city',
            'state',
            'zip',
            'phone',
        )


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = (
            'id',
            'stripe_card',
            'brand',
            'name',
            'last_4',
            'exp_month',
            'exp_year',
            'fingerprint',
        )


class UserSerializer(serializers.ModelSerializer):
    shipping_address = AddressSerializer()
    billing_address = AddressSerializer()
    default_card = CardSerializer()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'is_admin',
            'first_name',
            'last_name',
            'shipping_address',
            'billing_address',
            'default_card',
        )


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


class TemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Template
        fields = (
            'id',
            'template_file',
            'template_file_filename',
            'type',
        )


class ProductSerializer(serializers.ModelSerializer):
    category = ProductCategorySerializer()
    collapsibility = serializers.CharField(source='get_collapsibility_display')
    prices = ProductPriceSerializer(many=True)
    default_template = TemplateSerializer()

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
            'default_template',
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


class DesignElementSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')

    class Meta:
        model = DesignElement
        fields = (
            'id',
            'type',
            'width',
            'height',
            'left',
            'top',
            'angle',
        )


class DesignSerializer(serializers.ModelSerializer):
    # project = ProjectSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(source='project',  queryset=Project.objects.all())
    pattern = PatternSerializer(read_only=False)
    # pattern_id = serializers.PrimaryKeyRelatedField(source='pattern',  queryset=Pattern.objects.all())
    paper = PaperSerializer(read_only=False)
    # paper_id = serializers.PrimaryKeyRelatedField(source='paper',  queryset=Paper.objects.all())
    design_elements = DesignElementSerializer(many=True)

    class Meta:
        model = Design
        fields = (
            'id',
            # 'project',
            'project_id',
            'design_file',
            'pattern',
            # 'pattern_id',
            'paper',
            # 'paper_id',
            'design_elements',
        )


class OrderSerializerForProject(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Order
        fields = (
            'id',
            'order_number',
            'date_created',
            'date_status_changed',
            'status',
            'is_cancelled',
            'is_paid',
        )


class ProjectSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(source='product',  queryset=Product.objects.all())
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    design = DesignSerializer(read_only=True)
    # design_id = serializers.PrimaryKeyRelatedField(source='design', read_only=True)
    order = OrderSerializerForProject(read_only=True)

    class Meta:
        model = Project
        fields = (
            'id',
            'type',
            'type_display',
            'client_fingerprint',
            'title',
            'product',
            'product_id',
            'unit_price',
            'quantity',
            'design',
            'order',
            # 'design_id',
        )


class OrderSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(source='project',  queryset=Project.objects.all(), )
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Order
        fields = (
            'id',
            'order_number',
            'project',
            'project_id',
            'date_created',
            'date_status_changed',
            'status',
            'is_cancelled',
            'is_paid',
        )


class ShippingOptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingOption
        fields = (
            'id',
            'name',
            'price',
            'business_days',
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

