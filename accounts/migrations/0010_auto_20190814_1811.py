# Generated by Django 2.2.2 on 2019-08-14 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_card_fingerprint'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='exp_month',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AddField(
            model_name='card',
            name='exp_year',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
    ]
