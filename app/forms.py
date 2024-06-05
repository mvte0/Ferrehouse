from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Contacto, Producto, Boleta

#FORMULARIOS
class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'rut', 'motivo', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'rut': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rut'}),
            'motivo': forms.Select(attrs={'class': 'form-select'}),
            'mensaje': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Mensaje', 'rows': 4}),
        }
        
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        
class BoletaForm(forms.ModelForm):
    class Meta:
        model = Boleta
        fields = ['id_boleta', 'cliente', 'monto', 'fecha']