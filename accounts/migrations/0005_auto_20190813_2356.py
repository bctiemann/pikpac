# Generated by Django 2.2.2 on 2019-08-13 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190813_1915'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='address',
            name='phone',
            field=models.CharField(blank=True, max_length=10),
        ),
    ]
