# Generated by Django 2.2.2 on 2019-08-13 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20190813_2356'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]