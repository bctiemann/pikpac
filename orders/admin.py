from django.contrib import admin

from orders import models


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_created', 'user', 'type', 'product',)
    list_filter = ()
    readonly_fields = ()
    search_fields = ('user__email',)
admin.site.register(models.Project, ProjectAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'project', 'user', 'date_created', 'status', 'date_status_changed',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.Order, OrderAdmin)


class DesignAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'pattern', 'paper',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.Design, DesignAdmin)


class TaxRateAdmin(admin.ModelAdmin):
    list_display = ('postal_code', 'total_rate', 'date_updated',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.TaxRate, TaxRateAdmin)


class ShippingOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'business_days',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.ShippingOption, ShippingOptionAdmin)
