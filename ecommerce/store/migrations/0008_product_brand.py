# Generated by Django 5.1.2 on 2024-12-05 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_product_catgory_product_discounted_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Brand',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
