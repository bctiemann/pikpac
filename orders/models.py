import uuid

from django.db import models


def get_design_path(instance, filename):
    extension = filename.split('.')[-1].lower()
    filename = '{0}.{1}'.format(uuid.uuid4(), extension)
    return 'designs/{0}'.format(filename)


class Project(models.Model):
    product = models.ForeignKey('products.Product', null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(blank=True)
    unit_price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    colors = models.IntegerField(null=True, blank=True, default=0)
    design = models.ForeignKey('orders.Design', null=True, blank=True, on_delete=models.SET_NULL, related_name='projects')


class Design(models.Model):
    user = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey('orders.Project', null=True, blank=True, on_delete=models.SET_NULL, related_name='designs')
    date_created = models.DateTimeField(auto_now_add=True)
    template = models.ForeignKey('products.Template', null=True, blank=True, on_delete=models.SET_NULL)
    design_file = models.FileField(blank=True, upload_to=get_design_path)


