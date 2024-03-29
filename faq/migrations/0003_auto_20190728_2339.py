# Generated by Django 2.2.2 on 2019-07-28 23:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('faq', '0002_auto_20190728_2337'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faqcategory',
            options={'ordering': ('sort_order',), 'verbose_name_plural': 'FAQ categories'},
        ),
        migrations.AlterModelOptions(
            name='faqitem',
            options={'ordering': ('sort_order',), 'verbose_name': 'FAQ item'},
        ),
        migrations.AddField(
            model_name='faqitem',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='faq.FaqCategory'),
        ),
    ]
