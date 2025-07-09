from django import forms

class ContactoForm(forms.Form):
    nombre = forms.CharField(max_length=100)
    apellido = forms.CharField(max_length=100)
    correo = forms.EmailField()
    telefono = forms.CharField(max_length=15)
