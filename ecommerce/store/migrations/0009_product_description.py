# Generated by Django 5.1.2 on 2024-12-08 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_product_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
