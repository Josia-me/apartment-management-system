from django import forms
from .models import Building, Unit, Tenant, RentPayment

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'location', 'type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['building', 'unit_number', 'type', 'rent_amount', 'status']
        widgets = {
            'building': forms.Select(),
            'rent_amount': forms.NumberInput(attrs={'step': '0.0'}),
        }

class TenantForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['name', 'phone', 'email', 'email', 'id_number', 'profile_photo', 'status', 'unit']
        widgets = {
            'unit': forms.Select(),
        }

class TenantAssignForm(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = ['unit']
        widgets = {
            'unit': forms.Select(),
        }

class RentPaymentForm(forms.ModelForm):
    class Meta:
        model = RentPayment
        fields = ['tenant', 'unit', 'amount', 'year', 'month', 'status', 'payment_date']
        widgets = {
            'tenant': forms.Select(),
            'unit': forms.Select(),
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
            'month': forms.Select(),
        }