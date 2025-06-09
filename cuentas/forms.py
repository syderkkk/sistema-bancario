from django import forms

class TransferenciaForm(forms.Form):
    numero_cuenta_destino = forms.CharField(label="Número de cuenta destino", max_length=20)
    monto = forms.DecimalField(label="Monto a transferir", max_digits=12, decimal_places=2, min_value=0.01)
    descripcion = forms.CharField(label="Descripción", required=False)

class CajeroForm(forms.Form):
    numero_cuenta = forms.CharField(label="Número de cuenta", max_length=20)
    monto = forms.DecimalField(label="Monto", max_digits=12, decimal_places=2, min_value=0.01)

class ClaveSecretaForm(forms.Form):
    clave = forms.CharField(label="Clave secreta", widget=forms.PasswordInput, min_length=4, max_length=32)