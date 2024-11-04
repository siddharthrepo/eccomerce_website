# Generated by Django 5.1.2 on 2024-10-30 10:47

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('vendor', '0019_delete_vendor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('vendor_name', models.CharField(max_length=200, null=True)),
                ('store_name', models.CharField(blank=True, max_length=200, null=True)),
                ('email', models.EmailField(max_length=200, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('password', models.CharField(max_length=128)),
            ],
        ),
    ]
