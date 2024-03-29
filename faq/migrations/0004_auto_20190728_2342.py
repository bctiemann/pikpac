# Generated by Django 2.2.2 on 2019-07-28 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0003_auto_20190728_2339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faqitem',
            name='category',
        ),
        migrations.CreateModel(
            name='FaqHeading',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('sort_order', models.IntegerField(blank=True, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='faq.FaqCategory')),
            ],
            options={
                'verbose_name': 'FAQ heading',
                'ordering': ('sort_order',),
            },
        ),
        migrations.AddField(
            model_name='faqitem',
            name='heading',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='faq.FaqHeading'),
        ),
    ]
