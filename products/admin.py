from django.contrib import admin

from products import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.Product, ProductAdmin)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.Template, TemplateAdmin)
