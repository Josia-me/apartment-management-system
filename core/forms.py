from django import forms
from .models import Building, Unit

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
            'rent_amount': forms.NumberInput(attrs={'step': '0.01'}),
        }