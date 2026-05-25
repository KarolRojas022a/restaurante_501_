from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Plato, Cliente, Empleado, Mesa, Orden, Factura, Perfil

CODIGOS_PAIS = [
    ('', '— País —'),
    ('+57', '🇨🇴 +57 Colombia'),
    ('+1',  '🇺🇸 +1 EE.UU / Canadá'),
    ('+34', '🇪🇸 +34 España'),
    ('+52', '🇲🇽 +52 México'),
    ('+54', '🇦🇷 +54 Argentina'),
    ('+55', '🇧🇷 +55 Brasil'),
    ('+56', '🇨🇱 +56 Chile'),
    ('+58', '🇻🇪 +58 Venezuela'),
    ('+593','🇪🇨 +593 Ecuador'),
    ('+51', '🇵🇪 +51 Perú'),
]

class IngresoUsuarioForm(AuthenticationForm):
    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': 'Usuario o clave incorrectos. Comprueba los datos e inténtalo de nuevo.',
        'inactive': 'Esta cuenta está desactivada. Contacta al administrador.',
    }

    username = forms.CharField(
        label='Nombre usuario',
        error_messages={'required': 'Indica el nombre de usuario.'},
        widget=forms.TextInput(attrs={'class': 'auth-field-thick', 'autocomplete': 'username'}),
    )
    password = forms.CharField(
        label='Clave usuario',
        error_messages={'required': 'Indica la clave.'},
        widget=forms.PasswordInput(attrs={'class': 'auth-field-thick', 'autocomplete': 'current-password'}),
    )


class RegistroUsuarioForm(UserCreationForm):
    error_messages = {
        **UserCreationForm.error_messages,
        'password_mismatch': 'Las dos claves no coinciden.',
    }

    username = forms.CharField(
        label='Nombre usuario',
        error_messages={
            'required': 'Indica el nombre de usuario.',
        },
        widget=forms.TextInput(attrs={'class': 'auth-field-thick', 'autocomplete': 'username'}),
    )
    password1 = forms.CharField(
        label='Clave usuario',
        error_messages={'required': 'Indica la clave.'},
        widget=forms.PasswordInput(attrs={'class': 'auth-field-thick', 'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label='Confirmar clave',
        error_messages={'required': 'Confirma la clave.'},
        widget=forms.PasswordInput(attrs={'class': 'auth-field-thick', 'autocomplete': 'new-password'}),
    )
    rol = forms.ChoiceField(
        label='Rol usuario',
        choices=[],
        error_messages={
            'required': 'Selecciona un rol de usuario.',
            'invalid_choice': 'Selecciona un rol válido.',
        },
        widget=forms.Select(attrs={'class': 'auth-field-thick'}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].choices = [('', '— Elige un rol —')] + list(Perfil.ROLES)
        for name in ('username', 'password1', 'password2'):
            if name in self.fields:
                self.fields[name].help_text = None

    def save(self, commit=True):
        user = super().save(commit=commit)
        if hasattr(user, 'perfil'):
            user.perfil.rol = self.cleaned_data['rol']
            user.perfil.es_admin = False
            user.perfil.save(update_fields=['rol', 'es_admin'])
        return user

class ClienteForm(forms.ModelForm):
    codigo_pais = forms.ChoiceField(
        choices=CODIGOS_PAIS,
        required=False,
        label='',
        widget=forms.Select(attrs={'class': 'select-codigo-pais'}),
    )

    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'correo']
        widgets = {
            'telefono': forms.TextInput(attrs={
                'inputmode': 'numeric',
                'pattern': '[0-9]*',
                'class': 'input-telefono',
                'placeholder': 'Número local',
            }),
            'correo': forms.EmailInput(attrs={'placeholder': 'usuario@dominio.com'}),
        }

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if correo:
            if '@' not in correo:
                raise forms.ValidationError('El correo debe contener @.')
            _, dominio = correo.rsplit('@', 1)
            from .models import DOMINIOS_ACEPTADOS
            if dominio.lower() not in DOMINIOS_ACEPTADOS:
                raise forms.ValidationError(
                    f'Dominio "{dominio}" no permitido. '
                    f'Dominios aceptados: {", ".join(sorted(DOMINIOS_ACEPTADOS))}.'
                )
        return correo

    def clean_telefono(self):
        tel = self.cleaned_data.get('telefono') or ''
        if tel and not tel.replace(' ', '').isdigit():
            raise forms.ValidationError('El teléfono solo puede contener números.')
        return tel
    

    
class EmpleadoForm(forms.ModelForm):
     codigo_pais = forms.ChoiceField(
        choices=CODIGOS_PAIS,
        required=False,
        label='',
        widget=forms.Select(attrs={'class': 'select-codigo-pais'}),
    )
     
     class Meta:
        model = Empleado
        fields = ['nombre', 'cargo', 'telefono', 'correo']
        widgets = {
            'telefono': forms.TextInput(attrs={
                'inputmode': 'numeric',
                'pattern': '[0-9]*',
                'class': 'input-telefono',
                'placeholder': 'Número local',
            }),
            'correo': forms.EmailInput(attrs={'placeholder': 'usuario@dominio.com'}),
        }
     def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if correo:
            if '@' not in correo:
                raise forms.ValidationError('El correo debe contener @.')
            _, dominio = correo.rsplit('@', 1)
            from .models import DOMINIOS_ACEPTADOS
            if dominio.lower() not in DOMINIOS_ACEPTADOS:
                raise forms.ValidationError(
                    f'Dominio "{dominio}" no permitido. '
                    f'Dominios aceptados: {", ".join(sorted(DOMINIOS_ACEPTADOS))}.'
                )
        return correo

     def clean_telefono(self):
        tel = self.cleaned_data.get('telefono') or ''
        if tel and not tel.replace(' ', '').isdigit():
            raise forms.ValidationError('El teléfono solo puede contener números.')
        return tel
        
    
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

IVA = 0.19  # 19 % — ajusta según tu negocio
class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['orden', 'metodo_pago']
def clean(self):
        cleaned = super().clean()
        orden = cleaned.get('orden')
        if orden:
            subtotal = orden.total                          # ya calculado en DetalleOrden.save()
            impuesto = (subtotal * Decimal(str(IVA))).quantize(Decimal('0.01'))
            total    = subtotal + impuesto
            cleaned['subtotal']      = subtotal
            cleaned['impuesto']      = impuesto
            cleaned['total_factura'] = total
        return cleaned
def save(self, commit=True):
        instance = super().save(commit=False)
        instance.subtotal      = self.cleaned_data['subtotal']
        instance.impuesto      = self.cleaned_data['impuesto']
        instance.total_factura = self.cleaned_data['total_factura']
        if commit:
            instance.save()
            # Marcar la orden como Facturada
            orden = instance.orden
            orden.estado_orden = 'Facturada'
            orden.save(update_fields=['estado_orden'])
        return instance