# Generated by Django 5.1.2 on 2024-10-30 07:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0015_remove_vendor_vendorname_vendor_vendor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='password',
        ),
    ]