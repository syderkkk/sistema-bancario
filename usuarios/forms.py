from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Profile

class RegistroUsuarioForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre', max_length=150, required=True)
    last_name = forms.CharField(label='Apellido', max_length=150, required=True)
    fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento', widget=forms.DateInput(attrs={'type': 'date'}))
    direccion = forms.CharField(label='Dirección', max_length=255, required=False)
    telefono = forms.CharField(label='Teléfono', max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'fecha_nacimiento', 'direccion', 'telefono')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2                                                                

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = user.profile
            profile.fecha_nacimiento = self.cleaned_data['fecha_nacimiento']
            profile.direccion = self.cleaned_data['direccion']
            profile.telefono = self.cleaned_data['telefono']
            profile.save()
        return user

class EditarPerfilForm(forms.ModelForm):
    first_name = forms.CharField(label='Nombre', max_length=150, required=True)
    last_name = forms.CharField(label='Apellido', max_length=150, required=True)
    email = forms.EmailField(label='Correo electrónico', required=True)

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'email', 'fecha_nacimiento', 'direccion', 'telefono']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile.save()
        return profile