# Generated by Django 4.1 on 2022-09-10 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='category',
        ),
    ]