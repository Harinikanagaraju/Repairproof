from django import forms
from .models import Appliance


class ApplianceForm(forms.ModelForm):

    class Meta:
        model = Appliance

        fields = [
            'name',
            'brand',
            'model_number',
            'category',
            'purchase_date',
            'warranty_months',
            'price',
            'bill',
            'notes',
        ]

        widgets = {
            'purchase_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'notes': forms.Textarea(
                attrs={'rows': 3}
            ),
        }