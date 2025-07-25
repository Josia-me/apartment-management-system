from django import forms
from .models import Building

class BuildingForm(forms.ModelForm):
    class Meta:
        model = Building
        fields = ['name', 'location', 'type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }