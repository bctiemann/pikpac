import django_filters

from products.models import ProductCategory, Product
from faq.models import FaqCategory, FaqHeading, FaqItem


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(field_name="category__name",
                                            to_field_name="slug",
                                            queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('category',)


class FaqHeadingFilter(django_filters.FilterSet):

    class Meta:
        model = FaqHeading
        fields = ('category',)
