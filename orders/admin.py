from django.contrib import admin

from orders import models


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.Project, ProjectAdmin)


class DesignAdmin(admin.ModelAdmin):
    list_display = ('id',)
    list_filter = ()
    readonly_fields = ()
admin.site.register(models.Design, DesignAdmin)
