# Generated by Django 5.1.2 on 2024-10-30 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0016_remove_vendor_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='vendorname',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
