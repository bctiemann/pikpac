from django.contrib import admin

from faq import models


class FaqCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_order',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.FaqCategory, FaqCategoryAdmin)


class FaqHeadingAdmin(admin.ModelAdmin):
    list_display = ('title', 'sort_order',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.FaqHeading, FaqHeadingAdmin)


class FaqItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'sort_order',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.FaqItem, FaqItemAdmin)
