# Generated by Django 4.1 on 2022-09-10 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Outfit', 'Outfit'), ('Watch', 'Watch'), ('Digital', 'Digital'), ('Books', 'Books'), ('Gadjets', 'Gadjets')], max_length=100, null=True),
        ),
    ]