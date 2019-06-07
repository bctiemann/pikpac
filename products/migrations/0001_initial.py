# Generated by Django 2.2.2 on 2019-06-07 17:45

from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('category', models.CharField(choices=[('rigid', 'Rigid Boxes'), ('setup', 'Setup Boxes')], default='rigid', max_length=40)),
                ('picture', models.ImageField(blank=True, height_field='picture_height', upload_to=products.models.get_product_image_path, width_field='picture_width')),
                ('picture_width', models.IntegerField(blank=True, null=True)),
                ('picture_height', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('template_file', models.FileField(blank=True, upload_to=products.models.get_template_path)),
                ('type', models.CharField(choices=[('preset', 'Preset'), ('custom', 'Custom')], default='preset', max_length=40)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.Product')),
            ],
        ),
    ]
