from django.db import models
from django.contrib.auth.models import User
import uuid

class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE , null=True , blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor_name = models.CharField(max_length=200, null=True, unique=True)
    store_name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True) 
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.vendor_name or "Unnamed Vendor"
