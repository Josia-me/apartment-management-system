from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('tenant', 'Tenant'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='tenant')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.name

class Building(models.Model):
    TYPE_CHOICES = (
        ('apartment', 'Apartment'),
        ('house', 'House'),
    )
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Unit(models.Model):
    TYPE_CHOICES = (
        ('studio', 'Studio'),
        ('1-bedroom', '1-Bedroom'),
        ('2-bedroom', '2-Bedroom'),
        ('3-bedroom', '3-Bedroom'),
    )
    STATUS_CHOICES = (
        ('vacant', 'Vacant'),
        ('occupied', 'Occupied'),
    )
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='units')
    unit_number = models.CharField(max_length=50, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='vacant')

    def __str__(self):
        return f"{self.unit_number} - {self.building.name}"

class Tenant(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    id_number = models.CharField(max_length=50, unique=True)
    profile_photo = models.ImageField(upload_to='tenant_photos/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name='tenants')

    def __str__(self):
        return self.name

    def clean(self):
        if self.unit and self.unit.tenants.exclude(id=self.id).exists():
            raise ValidationError(f"Unit '{self.unit.unit_number}' is already occupied by another tenant.")
        super().clean()

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        if self.unit:
            self.unit.status = 'occupied'
            self.unit.save()
        elif self.pk:
            try:
                old_tenant = Tenant.objects.get(pk=self.pk)
                if old_tenant.unit:
                    old_unit = old_tenant.unit
                    old_unit.status = 'vacant'
                    old_unit.save()
            except Tenant.DoesNotExist:
                pass

class RentPayment(models.Model):
    STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('unpaid', 'Unpaid'),
    )
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField(choices=[(i, i) for i in range(1, 13)])
    year = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unpaid')
    payment_date = models.DateField(null=True, blank=True)
    receipt_number = models.CharField(max_length=50, unique=True, blank=True)

    def __str__(self):
        return f"{self.tenant.name} - {self.month}/{self.year}"

    def clean(self):
        if self.tenant.unit != self.unit:
            raise ValidationError("The tenant must be assigned to the selected unit.")
        if self.payment_date and self.status == 'unpaid':
            raise ValidationError("Payment date should be empty for unpaid status.")
        if not self.payment_date and self.status == 'paid':
            raise ValidationError("Payment date is required for paid status.")
        super().clean()

    def save(self, *args, **kwargs):
        if not self.receipt_number and self.status == 'paid':
            self.receipt_number = f"REC-{self.tenant.id}-{self.month}-{self.year}"
        elif self.status == 'unpaid':
            self.receipt_number = ''
        super().save(*args, **kwargs)