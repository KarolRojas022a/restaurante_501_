from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import Cliente, Empleado, Mesa, Plato, Orden, Factura
from .forms import ClienteForm, EmpleadoForm, MesaForm, PlatoForm, OrdenForm, FacturaForm
from .permisos import ACCESO_POR_ROL, MODULO_POR_MODELO, tiene_acceso, requiere_rol


# 1. Dashboard Inicial
@login_required
def inicio(request):
    perfil = getattr(request.user, 'perfil', None)
    acceso = ACCESO_POR_ROL.get(perfil.rol, set()) if perfil else set()

    context = {}
    if 'clientes' in acceso:
        context['total_clientes'] = Cliente.objects.count()
    if 'empleados' in acceso:
        context['total_empleados'] = Empleado.objects.count()
    if 'mesas' in acceso:
        context['total_mesas'] = Mesa.objects.count()
    if 'platos' in acceso:
        context['total_platos'] = Plato.objects.count()
    if 'ordenes' in acceso:
        context['total_ordenes'] = Orden.objects.count()
    if 'facturas' in acceso:
        context['total_facturas'] = Factura.objects.count()

    return render(request, 'gestion/inicio.html', context)


# 2. Listados (Read)
@login_required
@requiere_rol('clientes')
def lista_clientes(request):
    return render(request, 'gestion/clientes.html', {'clientes': Cliente.objects.all()})


@login_required
@requiere_rol('empleados')
def lista_empleados(request):
    return render(request, 'gestion/empleados.html', {'empleados': Empleado.objects.all()})


@login_required
@requiere_rol('mesas')
def lista_mesas(request):
    return render(request, 'gestion/mesas.html', {'mesas': Mesa.objects.all()})


@login_required
@requiere_rol('platos')
def lista_platos(request):
    return render(request, 'gestion/platos.html', {'platos': Plato.objects.all()})


@login_required
@requiere_rol('ordenes')
def lista_ordenes(request):
    return render(request, 'gestion/ordenes.html', {'ordenes': Orden.objects.all()})


@login_required
@requiere_rol('facturas')
def lista_facturas(request):
    return render(request, 'gestion/facturas.html', {'facturas': Factura.objects.all()})


# 3. El Motor del CRUD (Create & Update)
@login_required
def gestionar_registro(request, modelo, pk=None):
    config = {
        'cliente': (Cliente, ClienteForm, 'lista_clientes'),
        'plato': (Plato, PlatoForm, 'lista_platos'),
        'empleado': (Empleado, EmpleadoForm, 'lista_empleados'),
        'mesa': (Mesa, MesaForm, 'lista_mesas'),
        'orden': (Orden, OrdenForm, 'lista_ordenes'),
        'factura': (Factura, FacturaForm, 'lista_facturas'),
    }

    if modelo not in config:
        return redirect('inicio')

    perfil = getattr(request.user, 'perfil', None)
    if not tiene_acceso(perfil, MODULO_POR_MODELO.get(modelo)):
        return redirect('acceso_denegado')

    model_class, form_class, redirect_url = config[modelo]
    instance = get_object_or_404(model_class, pk=pk) if pk else None

    if request.method == 'POST':
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(redirect_url)
    else:
        form = form_class(instance=instance)

    return render(request, 'gestion/form_generico.html', {
        'form': form,
        'titulo': f'{"Editar" if pk else "Nuevo"} {modelo.capitalize()}'
    })


# Función para Eliminar
@login_required
def eliminar_registro(request, modelo, pk):
    config = {
        'cliente': (Cliente, 'lista_clientes'),
        'plato': (Plato, 'lista_platos'),
        'empleado': (Empleado, 'lista_empleados'),
        'mesa': (Mesa, 'lista_mesas'),
        'orden': (Orden, 'lista_ordenes'),
        'factura': (Factura, 'lista_facturas'),
    }

    if modelo not in config:
        return redirect('inicio')

    perfil = getattr(request.user, 'perfil', None)
    if not tiene_acceso(perfil, MODULO_POR_MODELO.get(modelo)):
        return redirect('acceso_denegado')

    model_class, redirect_url = config[modelo]
    objeto = get_object_or_404(model_class, pk=pk)

    if request.method == 'POST':
        objeto.delete()
        return redirect(redirect_url)

    return render(request, 'gestion/confirmar_eliminar.html', {'objeto': objeto, 'modelo': modelo})


@login_required
def acceso_denegado(request):
    return render(request, 'gestion/acceso_denegado.html', {}, status=403)
