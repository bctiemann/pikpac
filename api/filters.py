import django_filters

from orders.models import Project, Order
from products.models import ProductCategory, Product
from faq.models import FaqCategory, FaqHeading, FaqItem


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(field_name="category__name",
                                            to_field_name="slug",
                                            queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('category',)


class ProjectTypeFilter(django_filters.FilterSet):

    class Meta:
        model = Project
        fields = ('type',)


class OrderStatusFilter(django_filters.FilterSet):
    status = django_filters.MultipleChoiceFilter(choices=Order.STATUS_CHOICES)

    class Meta:
        model = Order
        fields = ('status',)


class FaqHeadingFilter(django_filters.FilterSet):

    class Meta:
        model = FaqHeading
        fields = ('category',)
