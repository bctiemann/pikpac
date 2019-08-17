# Generated by Django 2.2.2 on 2019-08-17 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_shippingoption_business_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingoption',
            name='name',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AlterField(
            model_name='shippingoption',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
