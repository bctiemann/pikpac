# Generated by Django 2.2.2 on 2019-08-04 00:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0004_auto_20190728_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='faqitem',
            name='heading',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='items', to='faq.FaqHeading'),
        ),
    ]
