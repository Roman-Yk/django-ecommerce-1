# Generated by Django 4.1 on 2022-09-20 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_alter_customer_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='avatar',
            field=models.ImageField(blank=True, default='placeholder.png', null=True, upload_to='profilePictures'),
        ),
    ]