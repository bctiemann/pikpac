import uuid
import json
from client import AvataxClient
import random

from django.conf import settings
from django_extensions.db.fields import ShortUUIDField
from django.utils.timezone import now

from django.db import models


def get_design_path(instance, filename):
    extension = filename.split('.')[-1].lower()
    filename = '{0}.{1}'.format(uuid.uuid4(), extension)
    return 'designs/{0}'.format(filename)

def get_proof_path(instance, filename):
    extension = filename.split('.')[-1].lower()
    filename = '{0}.{1}'.format(uuid.uuid4(), extension)
    return 'proofs/{0}'.format(filename)


class Project(models.Model):
    TYPE_CHOICES = (
        ('template', 'Predefined Template'),
        ('custom', 'Custom Design'),
    )

    id = ShortUUIDField(primary_key=True, editable=False)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES, null=True, blank=True)
    product = models.ForeignKey('products.Product', null=True, blank=True, on_delete=models.SET_NULL)
    user = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL)
    client_fingerprint = models.UUIDField(null=True, blank=True, db_index=True)
    title = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(null=True, blank=True)
    unit_price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    colors = models.IntegerField(null=True, blank=True, default=0)
    design = models.ForeignKey('orders.Design', null=True, blank=True, on_delete=models.SET_NULL, related_name='projects')

    @property
    def order(self):
        return self.order_set.first()

    def __str__(self):
        return '{0} {1}'.format(self.pk, self.user)

    class Meta:
        ordering = ('-date_created',)


class Design(models.Model):
    user = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey('orders.Project', null=True, blank=True, on_delete=models.SET_NULL, related_name='designs')
    date_created = models.DateTimeField(auto_now_add=True)
    template = models.ForeignKey('products.Template', null=True, blank=True, on_delete=models.SET_NULL)
    design_file = models.FileField(blank=True, upload_to=get_design_path)
    pattern = models.ForeignKey('products.Pattern', null=True, blank=True, on_delete=models.SET_NULL)
    paper = models.ForeignKey('products.Paper', null=True, blank=True, on_delete=models.SET_NULL)


class DesignElement(models.Model):
    TEXT = 'text'
    IMAGE = 'image'

    TYPE_CHOICES = (
        (TEXT, 'Text'),
        (IMAGE, 'Image'),
    )

    design = models.ForeignKey('orders.Design', null=True, blank=True, on_delete=models.CASCADE, related_name='design_elements')
    type = models.CharField(choices=TYPE_CHOICES, max_length=20, blank=True, default=TYPE_CHOICES[0][0])
    width = models.FloatField(null=True, blank=True, default=0)
    height = models.FloatField(null=True, blank=True, default=0)
    left = models.FloatField(null=True, blank=True, default=0)
    top = models.FloatField(null=True, blank=True, default=0)
    angle = models.FloatField(null=True, blank=True, default=0)
    scaleX = models.FloatField(null=True, blank=True, default=0)
    scaleY = models.FloatField(null=True, blank=True, default=0)


class Order(models.Model):
    OPEN = 'open'
    SUBMITTED = 'submitted'
    PROOF = 'proof'
    APPROVED = 'approved'
    PRODUCTION = 'production'
    SHIPPED = 'shipped'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (OPEN, 'Open'),
        (SUBMITTED, 'Submitted'),
        (PROOF, 'Awaiting customer approval'),
        (APPROVED, 'Approved'),
        (PRODUCTION, 'In production'),
        (SHIPPED, 'Shipped'),
        (CANCELLED, 'Cancelled'),
    )

    order_number = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey('accounts.User', null=True, blank=True, on_delete=models.SET_NULL)
    project = models.ForeignKey('orders.Project', null=True, blank=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_status_changed = models.DateTimeField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=30, blank=True, default=STATUS_CHOICES[0][0])
    is_cancelled = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.order_number:
            random.seed(self.project.id)
            self.order_number = str(random.randint(0, settings.MAX_ORDER_NUMBER)).rjust(8, '0')
            self.save()

    def __str__(self):
        return '#{0} {1}'.format(self.order_number, self.user.email)


class Proof(models.Model):
    project = models.ForeignKey('orders.Project', null=True, blank=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('accounts.user', null=True, blank=True, on_delete=models.SET_NULL)
    proof_file = models.FileField(blank=True, upload_to=get_proof_path)
    comments = models.TextField(blank=True)


class TaxRate(models.Model):
    postal_code = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=20, default='us')
    total_rate = models.DecimalField(max_digits=10, decimal_places=5, null=True, blank=True)
    detail = models.TextField(blank=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{0}: {1}'.format(self.postal_code, self.total_rate)

    def update(self):
        client = AvataxClient(
            'Pikpac',
            'v0.1',
            'Backend server 001',
            'production'
        )
        client.add_credentials(settings.AVALARA_ACCOUNT_ID, settings.AVALARA_LICENSE_KEY)
        response = client.tax_rates_by_postal_code(include={'country': self.country, 'postalCode': self.postal_code})
        response.raise_for_status()
        result = response.json()
        self.total_rate = result['totalRate']
        self.detail = json.dumps(result['rates'])
        self.date_updated = now()
        self.save()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.total_rate:
            self.update()


class ShippingOption(models.Model):
    name = models.CharField(max_length=30, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    business_days = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering: ('-price')