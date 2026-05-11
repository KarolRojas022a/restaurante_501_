from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Plato, Cliente, Empleado, Mesa, Orden, Factura, Perfil


class IngresoUsuarioForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre usuario',
        widget=forms.TextInput(attrs={'class': 'auth-field-thick', 'autocomplete': 'username'}),
    )
    password = forms.CharField(
        label='Clave usuario',
        widget=forms.PasswordInput(attrs={'class': 'auth-field-thick', 'autocomplete': 'current-password'}),
    )


class RegistroUsuarioForm(UserCreationForm):
    username = forms.CharField(
        label='Nombre usuario',
        widget=forms.TextInput(attrs={'class': 'auth-field-thick', 'autocomplete': 'username'}),
    )
    password1 = forms.CharField(
        label='Clave usuario',
        widget=forms.PasswordInput(attrs={'class': 'auth-field-thick', 'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='Confirmar clave',
        widget=forms.PasswordInput(attrs={'class': 'auth-field-thick', 'autocomplete': 'new-password'}),
    )
    rol = forms.ChoiceField(
        label='Rol usuario',
        choices=Perfil.ROLES,
        widget=forms.Select(attrs={'class': 'auth-field-thick'}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def save(self, commit=True):
        user = super().save(commit=commit)
        if hasattr(user, 'perfil'):
            user.perfil.rol = self.cleaned_data['rol']
            user.perfil.es_admin = False
            user.perfil.save(update_fields=['rol', 'es_admin'])
        return user

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo']

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'cargo', 'telefono', 'correo']

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['numero_mesa', 'capacidad', 'estado_mesa']

class PlatoForm(forms.ModelForm):
    class Meta:
        model = Plato
        fields = ['nombre_plato', 'descripcion', 'precio', 'categoria', 'disponible']

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['cliente', 'empleado', 'mesa', 'estado_orden']

class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['orden', 'metodo_pago', 'subtotal', 'impuesto', 'total_factura']