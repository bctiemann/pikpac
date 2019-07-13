from django.contrib import admin

from products import models


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'sort_order',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.ProductCategory, ProductCategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku', 'name', 'category', 'pieces', 'collapsibility',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.Product, ProductAdmin)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.Template, TemplateAdmin)
