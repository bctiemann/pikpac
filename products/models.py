import uuid
import os

from django.db import models


def get_product_image_path(instance, filename):
    extension = filename.split('.')[-1].lower()
    filename = '{0}.{1}'.format(uuid.uuid4(), extension)
    return 'products/{0}'.format(filename)

def get_pattern_image_path(instance, filename):
    extension = filename.split('.')[-1].lower()
    filename = '{0}.{1}'.format(uuid.uuid4(), extension)
    return 'patterns/{0}'.format(filename)

def get_paper_image_path(instance, filename):
    extension = filename.split('.')[-1].lower()
    filename = '{0}.{1}'.format(uuid.uuid4(), extension)
    return 'papers/{0}'.format(filename)

def get_template_path(instance, filename):
    dir_name = uuid.uuid4()
    return 'templates/{0}/{1}'.format(dir_name, filename)


class ProductCategory(models.Model):
    slug = models.CharField(max_length=40, blank=True)
    name = models.CharField(max_length=40, blank=True)
    sort_order = models.IntegerField(null=True, blank=True)
    picture = models.ImageField(blank=True, width_field='picture_width', height_field='picture_height', upload_to=get_product_image_path)
    picture_width = models.IntegerField(null=True, blank=True)
    picture_height = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('sort_order',)
        verbose_name_plural = 'product categories'


class Product(models.Model):
    COLLAPSIBILITY_CHOICES = (
        ('c', 'Collapsible'),
        ('nc', 'Non-collapsible'),
    )

    category = models.ForeignKey('products.ProductCategory', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=200, blank=True)
    picture = models.ImageField(blank=True, width_field='picture_width', height_field='picture_height', upload_to=get_product_image_path)
    picture_width = models.IntegerField(null=True, blank=True)
    picture_height = models.IntegerField(null=True, blank=True)
    pieces = models.IntegerField(null=True, blank=True)
    collapsibility = models.CharField(choices=COLLAPSIBILITY_CHOICES, default=COLLAPSIBILITY_CHOICES[0][0], max_length=10)
    default_template = models.ForeignKey('products.Template', null=True, blank=True, on_delete=models.SET_NULL, related_name='current_products')

    def __str__(self):
        return self.name


class ProductPrice(models.Model):
    product = models.ForeignKey('products.Product', null=True, blank=True, on_delete=models.SET_NULL, related_name='prices')
    quantity = models.IntegerField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ('quantity',)


class Template(models.Model):
    TYPE_CHOICES = (
        ('preset', 'Preset',),
        ('custom', 'Custom',),
    )

    product = models.ForeignKey('products.Product', null=True, blank=True, on_delete=models.SET_NULL)
    template_file = models.FileField(blank=True, upload_to=get_template_path)
    type = models.CharField(choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0], max_length=40)

    @property
    def template_file_filename(self):
        return os.path.basename(self.template_file.name)


class Pattern(models.Model):
    sku = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=200, blank=True)
    picture = models.ImageField(blank=True, width_field='picture_width', height_field='picture_height', upload_to=get_pattern_image_path)
    picture_width = models.IntegerField(null=True, blank=True)
    picture_height = models.IntegerField(null=True, blank=True)


class Paper(models.Model):
    sku = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=200, blank=True)
    picture = models.ImageField(blank=True, width_field='picture_width', height_field='picture_height', upload_to=get_paper_image_path)
    picture_width = models.IntegerField(null=True, blank=True)
    picture_height = models.IntegerField(null=True, blank=True)
