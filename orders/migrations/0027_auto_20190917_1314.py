# Generated by Django 2.2.2 on 2019-09-17 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0026_designelement'),
    ]

    operations = [
        migrations.AddField(
            model_name='designelement',
            name='scaleX',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='designelement',
            name='scaleY',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='designelement',
            name='angle',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='designelement',
            name='design',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='design_elements', to='orders.Design'),
        ),
        migrations.AlterField(
            model_name='designelement',
            name='height',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='designelement',
            name='left',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='designelement',
            name='top',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='designelement',
            name='width',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
