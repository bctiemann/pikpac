import uuid

from django.db import models


def get_product_image_path(instance, filename):
    extension = filename.split('.')[-1].lower()
    filename = '{0}.{1}'.format(uuid.uuid4(), extension)
    return 'products/{0}'.format(filename)

def get_template_path(instance, filename):
    extension = filename.split('.')[-1].lower()
    filename = '{0}.{1}'.format(uuid.uuid4(), extension)
    return 'templates/{0}'.format(filename)


class Product(models.Model):
    CATEGORY_CHOICES = (
        ('rigid', 'Rigid Boxes',),
        ('setup', 'Setup Boxes',),
    )

    name = models.CharField(max_length=200, blank=True)
    category = models.CharField(choices=CATEGORY_CHOICES, default=CATEGORY_CHOICES[0][0], max_length=40)
    picture = models.ImageField(blank=True, width_field='picture_width', height_field='picture_height', upload_to=get_product_image_path)
    picture_width = models.IntegerField(null=True, blank=True)
    picture_height = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Template(models.Model):
    TYPE_CHOICES = (
        ('preset', 'Preset',),
        ('custom', 'Custom',),
    )

    product = models.ForeignKey('products.Product', null=True, blank=True, on_delete=models.SET_NULL)
    template_file = models.FileField(blank=True, upload_to=get_template_path)
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0], max_length=40)