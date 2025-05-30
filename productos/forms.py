from django import forms

class DatosClienteForm(forms.Form):
    nombre = forms.CharField(max_length=50, label="Nombre")
    apellido = forms.CharField(max_length=40, label="Apellido")
    correo = forms.EmailField(max_length=35, label="Correo electrónico")
