import django_filters

from products.models import ProductCategory, Product


class ProductFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(field_name="category__name",
                                            to_field_name="slug",
                                            queryset=ProductCategory.objects.all())

    class Meta:
        model = Product
        fields = ('category',)