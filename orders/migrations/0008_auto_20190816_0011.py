# Generated by Django 2.2.2 on 2019-08-16 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_taxrate'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taxrate',
            old_name='zip',
            new_name='postal_code',
        ),
        migrations.AddField(
            model_name='taxrate',
            name='country',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
