from django import forms
from .models import SolicitudPrestamo

class SolicitudPrestamoForm(forms.ModelForm):
    class Meta:
        model = SolicitudPrestamo
        fields = ['monto', 'plazo_meses', 'motivo']
        widgets = {
            'motivo': forms.Textarea(attrs={'rows': 3}),
        }