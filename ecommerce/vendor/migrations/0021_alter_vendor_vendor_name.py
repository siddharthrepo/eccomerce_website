# Generated by Django 5.1.2 on 2024-11-04 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0020_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vendor_name',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
