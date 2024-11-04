from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid

class Vendor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor_name = models.CharField(max_length=200, null=True)
    store_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=200, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(null=True, blank=True)
    password = models.CharField(max_length=128)  # Store hashed password here

    def __str__(self):
        return self.vendor_name or "Unnamed Vendor"

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
